import json
from fc_units import *


class MCVMove(object):
    def __init__(self):
        pass


class FlowChart(object):
    def __init__(self, replay, player_index=0):
        self.pi = player_index
        self.replay = replay
        self.p_info = replay.players[0]
        self.p_faction = self.p_info.decode_faction()

        self.check_faction()

        self.json_data = [

        ]
        self.root = {}
        self.structures = []
        self.queue_units = {}
        self.queue_factory = []  # list of factory id
        self.queue_factory_tc = []  # time code for the factory first produce unit
        self.has_wall = False
        self.on_building_structure = {
            1: {},  # Production Structure
            2: {},  # Production Structure
        }

        self.structure_pa = []
        self.structure_dict = {}

        self.pack_list = []  # pack mcv
        self.deploy_list = []  # mcv deployed

    def check_faction(self):
        # Confirm the faction(camp) first,
        # faction:'Obs', 'E', 'PostCommentator', 'A', 'f4', 'f5', 'Rnd', 'S'
        if self.p_faction not in ['E', 'A', 'Rnd', 'S']:
            return -2  # The faction is not supported
        if self.p_faction == 'E':
            return -1  # "At present, the flow chart does not support the Empire camp"
        if self.p_faction == 'Rnd':
            for chunk in self.replay.replay_body.chunks:
                for cmd in chunk.commands:
                    if cmd.cmd_id == 7:
                        faction = cmd.info["building_type"][0]
                        if faction in ['E', 'A', 'S']:
                            self.p_faction = faction
                            return self.check_faction()
                    if cmd.cmd_id == 5:
                        faction = cmd.info["unit_ty"][0]
                        if faction in ['E', 'A', 'S']:
                            self.p_faction = faction
                            return self.check_faction()
            return 0  # The player's camp cannot be resolved
        else:
            return 1

    def parse_a_chunks(self):
        # for allied
        for ci, chunk in enumerate(self.replay.replay_body.chunks):
            for cmd in chunk.commands:
                chunk.decode_cmd(cmd)
                if cmd.cmd_id == 7:  # Start building
                    parent = cmd.info.get("parent", -1)
                    name = cmd.info["building_type"]
                    if name == "A Allied Fortress Walls":
                        continue

                    k = get_k_by_name(name)
                    unit = self.on_building_structure[k].get(parent, None)
                    # If there's a building under pausing construction, Start building is continue
                    if unit and unit.name == name:
                        if unit.status == 1:
                            continue
                        elif unit.status != 0:
                            raise Exception("Inconsistent construction data in chunk %s" % ci)
                        else:
                            unit.status += 1
                    else:
                        if unit and unit.status == 1:  # structure built done before and don't need to place
                            unit = self.on_building_structure[k][parent]
                            unit.end_time = unit.get_end_time()
                            self.structures.append(unit)
                        unit = Unit(name, chunk.time_code, parent)
                        self.on_building_structure[k][parent] = unit
                elif cmd.cmd_id == 8:  # pause building or stop building
                    parent = cmd.info.get("parent", -1)
                    name = cmd.info["building_type"]
                    if name == "A Allied Fortress Walls":
                        continue

                    k = get_k_by_name(name)
                    unit = self.on_building_structure[k].get(parent, None)
                    # If there's a building under pausing construction, Start building is continue
                    if unit:
                        if unit.status == -1:
                            raise Exception("Inconsistent construction data")
                        else:
                            unit.status -= 1
                    else:
                        raise Exception("Inconsistent construction data")
                elif cmd.cmd_id == 9:  # Place building
                    parent = cmd.info.get("parent", -1)
                    name = cmd.info["building_type"]
                    if name == "A Allied Fortress Walls":
                        continue

                    k = get_k_by_name(name)
                    unit = self.on_building_structure[k].get(parent, None)
                    if unit is None:
                        raise Exception("Structure 1 Data inconsistency")
                    else:
                        unit = self.on_building_structure[k][parent]
                        unit.end_time = chunk.time_code
                        self.structures.append(unit)
                        self.on_building_structure[k][parent] = None

                elif cmd.cmd_id == 5:  # Queue units
                    unit_ty = cmd.info["unit_ty"]
                    factory = cmd.info["factory"]
                    queue_line = self.queue_units.get(factory, [])
                    paste_unit = get_prev_one(queue_line, unit_ty)
                    if paste_unit and paste_unit.status == 0:
                        # It was suspended before. Now it's on
                        paste_unit.start_time = chunk.time_code
                        paste_unit.status = 1
                    else:
                        unit = Unit(unit_ty, chunk.time_code, factory)
                        unit.count = cmd.info["cnt"]
                        cost_time = cmd.info["cost"][1]
                        unit.cost_time = [cost_time] * unit.count
                        if factory in self.queue_units:
                            self.queue_units[factory].append(unit)
                        else:
                            self.queue_units[factory] = [unit]

                        if factory not in self.queue_factory:
                            self.queue_factory.append(factory)
                            self.queue_factory_tc.append(chunk.time_code)
                elif cmd.cmd_id == 6:  # Hold/Cancel queue units
                    unit_ty = cmd.info["unit_ty"]
                    factory = cmd.info["factory"]
                    queue_line = self.queue_units.get(factory, [])
                    paste_unit = get_prev_one(queue_line, unit_ty)
                    if paste_unit is None or paste_unit.status == -1:
                        raise QueueInconsistency()
                    elif paste_unit == 1:
                        dt = (chunk.time_code - paste_unit.start_time) // 15  # time it has been in production
                        born_count, left_t = get_born_count(dt, paste_unit.cost_time)
                        if born_count > 0:
                            new_unit = Unit(unit_ty, chunk.time_code, factory)
                            new_unit.count = paste_unit.count - born_count
                            new_unit.cost_time = paste_unit.cost_time[born_count:]
                            new_unit.cost_time[born_count] = left_t
                            new_unit.status = 0

                            # reset of start_time is done in cmd id 5
                            paste_unit.cost_time = paste_unit.cost_time[:born_count]
                            paste_unit.end_time = sum(paste_unit.cost_time)
                            paste_unit.count = born_count
                        else:
                            paste_unit.cost_time[0] = left_t
                            paste_unit.status = 0

                    elif paste_unit.status == 0:
                        paste_unit.status = -1

                elif cmd.cmd_id == 254 and str(cmd) == "Pack MCV":  #pack mcv
                    unit_id = cmd.info["unit_id"]
                    st = chunk.time_code
                    pack_mcv = PackMCV(chunk.time_code, unit_id)
                    self.pack_list.append(pack_mcv)
                    for j in range(ci, len(self.replay.replay_body.chunks)):
                        chunk_j = self.replay.replay_body.chunks[j]
                        if len(chunk_j.commands) >= 2 and chunk_j.time_code - st <= PACK_TIME * 15:
                            find_cmd_246 = False
                            for j_cmd in chunk.commands:
                                if j_cmd.cmd_id == 249 and unit_id in j_cmd.info["remove_uids"]:
                                    find_cmd_246 = True
                                    break
                            if find_cmd_246:
                                for j_cmd in chunk.commands:
                                    if j_cmd.cmd_id == 246:
                                        pack_mcv.next_ids = j_cmd.info["generate_uids"]
                                        break
                elif cmd.cmd_id == 0:  # "Deploy Core/MCV"
                    unit_id = cmd.info["unit_id"]
                    deploy_mcv = DeployMCV(chunk.time_code, unit_id)

                    for pack_mcv in self.pack_list[::-1]:
                        if pack_mcv.depoly is None and unit_id in pack_mcv.next_ids:
                            pack_mcv.depoly = deploy_mcv
                            deploy_mcv.prev = pack_mcv
                    self.deploy_list.append(deploy_mcv)

                elif cmd.cmd_id == 3:  # upgrade, same like Start building
                    parent = cmd.info["unit_id"]
                    name = cmd.info["upgrade"]

                    k = 1
                    unit = self.on_building_structure[k].get(parent, None)
                    # If there's a building under pausing construction, Start building is continue
                    if unit:
                        if unit.status == 1:
                            continue
                        elif unit.status != 0:
                            raise Exception("Inconsistent construction data in chunk %s" % ci)
                        else:
                            unit.start_time = chunk.time_code
                            unit.status += 1
                    else:
                        unit = Unit(name, chunk.time_code, parent)
                        unit.cost_time = [cmd.info["cost"][1]]
                        self.on_building_structure[k][parent] = unit

                elif cmd.cmd_id == 4:  # hold or cancel upgrade, same like pause building or stop building
                    name = cmd.info["hold_upgrade"]
                    parent = cmd.info["unit_id"]

                    k = 1
                    unit = self.on_building_structure[k].get(parent, None)

                    # If there's a building under pausing construction, Start building is continue
                    if unit and unit.name == name:
                        if unit.status == -1:
                            raise Exception("Inconsistent construction data")
                        else:
                            if unit.status == 1:
                                dt = (chunk.time_code - unit.start_time) // 15  # time it has been in production
                                born_count, left_t = get_born_count(dt, paste_unit.cost_time)
                                unit.cost_time = [left_t]
                            unit.status -= 1
                    else:
                        raise Exception("Inconsistent construction data")

    def bind_structures_and_units(self):
        # for allied
        for i, factory in enumerate(self.queue_factory):
            start_time = self.queue_factory_tc[i]
            queue_kind = get_unit_kind(self.queue_units[factory])
            if queue_kind == "":
                raise QueueInconsistency()
            factory_structure = get_queue_factory(start_time, queue_kind, self.structures)
            if factory_structure is None:
                continue

            factory_structure.uid = factory

        # Classify structures according to their MCV
        for s in self.structures:
            pa = s.pa
            if pa not in self.structure_pa:
                self.structure_pa.append(pa)
                self.structure_dict[pa] = [s]
            else:
                self.structure_dict[pa].append(s)

        unit_mcv_list = []
        for q_i in self.queue_units:
            for unit in self.queue_units[q_i]:
                if unit.name in ["A Allied MCV", "A Allied MCV (NavYd)"] and unit.status == 1:
                    unit_mcv_list.append(unit)

        # sort by end time
        unit_mcv_list.sort(key=lambda unit_mcv: unit_mcv.get_end_time())

        # find unit mcv for deploy
        for deploy_mcv in self.deploy_list:
            if deploy_mcv.prev is None:
                for unit_mcv in unit_mcv_list:
                    if unit_mcv.uid < 0 and unit_mcv.get_end_time() <= deploy_mcv.command_time:
                        unit_mcv.uid = deploy_mcv.cur_uid
                        unit_mcv.details["deploy"] = deploy_mcv
                        deploy_mcv.prev = unit_mcv
                        break
            # not find mcv from units
            if deploy_mcv.prev is None:
                for pack_mcv in self.pack_list:
                    if pack_mcv.depoly is None and len(pack_mcv.next_ids) == 0:
                        if pack_mcv.start_time < deploy_mcv.command_time:
                            pack_mcv.depoly = deploy_mcv
                            deploy_mcv.prev = pack_mcv
                            break

        # remove all deploy mcv that can not find prev unit or packed one
        self.deploy_list = [deploy_mcv for deploy_mcv in self.deploy_list if deploy_mcv.prev is not None]
        # set deploy mcv for all Classified structures
        for sp in self.structure_pa[1:]:
            structures = self.structure_dict[sp]
            first_time = structures[0].start_time
            for deploy_mcv in self.deploy_list:
                if deploy_mcv.next_id < 0 and deploy_mcv.command_time < first_time:
                    deploy_mcv.next_id = sp
                    deploy_mcv.cal_deploy_time(first_time)
                    break

    def get_json_from_root(self):
        pass

    def add_unit_row_json(self, factory, nr):
        factory_id = factory.uid
        units = self.queue_units[factory_id]
        # delete paste and refresh order
        units = [unit for unit in units if unit.status == 1]
        units.sort(key=lambda unit: unit.start_time)

        last_time_second = factory.get_end_time() // 15
        last_time = factory.get_end_time()

        for ui, unit in enumerate(units):
            # if ui >= 5:
            #     print("debug")

            st = unit.start_time // 15
            if st > last_time_second:
                unused = {
                    "kind": "unused",
                    "duration": st - last_time_second,
                    "type": "line"
                }
                self.json_data[nr].append(unused)
            elif st < last_time_second:
                unit.start_time = last_time
            if unit.count > 1:
                for i in range(unit.count):
                    unit_json = unit.get_json(i)
                    self.json_data[nr].append(unit_json)
            else:
                unit_json = unit.get_json()
                self.json_data[nr].append(unit_json)
            last_time = unit.get_end_time()
            last_time_second = last_time // 15

            if unit.uid > 0 and unit.details.get("deploy"):
                unit_nr = len(self.json_data)
                new_row = [None] * (len(self.json_data[nr]) - 1)
                new_json = unit.get_unit_json(nr)
                new_row.append(new_json)
                self.json_data.append(new_row)
                self.add_struc_row_json(unit, unit_nr)

    def add_struc_row_json(self, parent, nr):
        last_time_second = parent.details["deploy"].deploy_time // 15
        move = {
            "kind": "move",
            "duration": last_time_second - parent.get_end_time() // 15,
            "type": "line"
        }
        self.json_data[nr].append(move)
        sp = parent.details["deploy"].next_id
        used_sps = []
        while sp not in used_sps and sp in self.structure_dict:
            structure_list = self.structure_dict[sp]
            for s in structure_list:
                if s.name not in STRUCTURES[1]:
                    continue

                st = s.start_time // 15
                if st > last_time_second:
                    unused = {
                        "kind": "unused",
                        "duration": st - last_time_second,
                        "type": "line"
                    }
                    self.json_data[nr].append(unused)
                unit_json = s.get_json()

                if s.uid >= 0 and s.uid in self.queue_units:
                    s_nr = len(self.json_data)
                    new_row = [None] * len(self.json_data[0])
                    new_json = s.get_unit_json(nr)
                    new_row.append(new_json)
                    self.json_data.append(new_row)
                    self.add_unit_row_json(s, s_nr)

                self.json_data[nr].append(unit_json)
                last_time_second = s.get_end_time() // 15

            used_sps.append(sp)

            for pack_mcv in self.pack_list:
                if pack_mcv.cur_id == sp and pack_mcv.depoly is not None and pack_mcv.depoly.deploy_time > 0:
                    move = {
                        "kind": "move",
                        "duration": pack_mcv.depoly.deploy_time // 15 - pack_mcv.start_time // 15,
                        "type": "line"
                    }
                    self.json_data[nr].append(move)
                    sp = pack_mcv.depoly.next_id
                    last_time_second = pack_mcv.depoly.deploy_time // 15
                    break

    def get_allied_json(self):
        root = {
            "country": "Allied",
            "kind": "Production",
            "name": "RA3 Allied Construction Yard Icons",
            "type": "unit",
        }

        self.json_data.append([root])

        last_time_second = 0
        if len(self.structure_pa) == 0:
            return
        sp = self.structure_pa[0]
        used_sps = []
        while sp not in used_sps and sp in self.structure_dict:
            structure_list = self.structure_dict[sp]
            for s in structure_list:
                if s.name not in STRUCTURES[1]:
                    continue

                st = s.start_time // 15
                if st > last_time_second:
                    unused = {
                        "kind": "unused",
                        "duration": st - last_time_second,
                        "type": "line"
                    }
                    self.json_data[0].append(unused)
                unit_json = s.get_json()

                if s.uid >= 0 and s.uid in self.queue_units:
                    nr = len(self.json_data)
                    new_row = [None] * len(self.json_data[0])
                    new_json = s.get_unit_json(0)
                    new_row.append(new_json)
                    self.json_data.append(new_row)
                    self.add_unit_row_json(s, nr)

                self.json_data[0].append(unit_json)
                last_time_second = s.get_end_time() // 15

            used_sps.append(sp)

            for pack_mcv in self.pack_list:
                if pack_mcv.cur_id == sp and pack_mcv.depoly is not None and pack_mcv.depoly.deploy_time > 0:
                    move = {
                        "kind": "move",
                        "duration": pack_mcv.depoly.deploy_time // 15 - pack_mcv.start_time // 15,
                        "type": "line"
                    }
                    self.json_data[0].append(move)
                    sp = pack_mcv.depoly.next_id
                    last_time_second = pack_mcv.depoly.deploy_time // 15
                    break

    def save_json(self, save_path):
        total = {
            "camp": FACTION[self.p_faction],
            "root": "r0c0",
            "data": self.json_data
        }

        with open(save_path, 'w') as f:
            json.dump(total, f)