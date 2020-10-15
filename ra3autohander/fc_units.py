# some constants
PACK_TIME = 1

STRUCTURES = {
    # Production structure
    1: [
        "A Power Plant", "A Boot Camp", "A Allied Ore Refinery", "A Armor Facility", "A Seaport", "A Airbase", "A Defense Bureau", "A Clearance I", "A Clearance II",
        "S Crane", "S Reactor", "S Barracks", "S Soviet Ore Refinery", "S War Factory", "S Super Reactor", "S Battle Lab", "S Airfield", "S Naval Yard",
    ],
    # Defense structure
    2: [
        "A Allied Fortress Walls", "A Multigunner Turret", "A Spectrum Tower", "A Chronosphere", "A Proton Collider",
        "S Soviet Fortress Wall", "S Iron Curtain", "S Vaccum Imploder", "S Tesla Coil", "S Sentry Gun", "S Flak Cannon",
    ]
}
UNITS = {
    "Infantry": [
        "A Attack Dog", "A Peacekeeper", "A Javelin Soldier", "A Tanya", "A Spy", "A Allied Engineer",
        "S War Bear", "S Conscript", "S Flak Trooper", "S Combat Engineer", "S Tesla Trooper", "S Natasha",
        ],
    "Vehicles": [
        "A Prospecter", "A Riptide ACV", "A Multigunner IFV", "A Guardian Tank", "A Athena Cannon", "A Mirage Tank", "A Allied MCV",
        "S Ore Collector", "S Sputnik", "S Terror Drone", "S Sickle", "S Bullfrog", "S Hammer Tank", "S V4 Rocket Launcher", "S Apocalypse Tank", "S Soviet MCV",
        ],
    "Aircraft": [
        "A Vindicator", "A Apollo Fighter", "A Cryocopter", "A Century Bomber",
        "S Twinblade", "S Mig", "S Kirov Airship",
        ],
    "Vessels": [
        "A Prospecter (NavYd)", "A Dolphin", "A Riptide ACV (NavYd)", "A Hydrofoil", "A Assault Destroyer", "A Aircraft Carrier","A Allied MCV (NavYd)",
        "S Ore Collector (NavYd)", "S Sputnik (NavYd)", "S Stingray", "S Bullfrog (NavYd)", "S Akula Submarine", "S Dreadnought", "S Soviet MCV (NavYd)",
    ]
}

UNIT_FACTORY = {
    "Infantry": ["A Boot Camp", "S Barracks"],
    "Vehicles": ["A Armor Facility", "S War Factory"],
    "Aircraft": ["A Airbase", "S Airfield"],
    "Vessels": ["A Seaport", "S Naval Yard"],
}

FACTION = {
    "S": "Soviet",
    "E": "Empire",
    "A": "Allied",
}


IMAGEPATHMAP = {
    "Clearance I": "RA3_Heightened_Clearance_Icons",
    "Clearance II": "RA3_Maximum_Clearance_Icons",
    "Crane": "RA3 Crusher Crane Icons"
}


class QueueInconsistency(Exception):
    pass


class StructureInconsistency(Exception):
    pass


def get_k_by_name(name):
    for k in [1, 2]:
        if name in STRUCTURES[k]:
            return k

    return 0


def get_prev_one(queue_line, unit_ty):
    for unit in queue_line[::-1]:
        if unit.name == unit_ty:
            return unit
    return None


def get_born_count(dt, cost_times):  # and count the last one remaining cost time
    born_count = 0
    for t in cost_times[:-1]:
        if dt > t:
            born_count += 1
            dt -= t
        else:
            return born_count, t - dt

    return born_count, max(1, cost_times[-1] - dt)


def get_unit_kind(queue_line):
    for unit in queue_line:
        for k in UNITS:
            if unit.name in UNITS[k]:
                return k

    return ""


def get_queue_factory(sart_time, queue_kind, structures):
    for s in structures:
        if s.name in UNIT_FACTORY[queue_kind] and s.uid < 0:
            if s.end_time <= sart_time:  # end_time
                return s
            else:
                return None

    return None


def get_first_unit(queue, unit_name):
    for unit in queue:
        if unit.name in unit_name and unit.status == 1:
            return unit

    return None


class Unit(object):
    def __init__(self, name, start_time, parent):
        self.name = name
        self.start_time = start_time
        self.pa = parent

        self.count = 1
        self.cost_time = -1  # cost time
        self.base_cost = -1  # cost time by one unit
        self.end_time = -1
        # 1: building, 0: pause, -1: stop
        self.status = 1
        self.uid = -1
        self.details = {}

    def get_end_time(self, index = -1):
        if self.end_time > 0:
            return self.end_time
        elif index >= 0:
            # TODO
            pass
        elif isinstance(self.cost_time, list):
            return self.start_time + sum(self.cost_time) * 15
        else:
            return self.start_time + self.cost_time * 15

    def get_img_name(self):
        img_name = self.name[2:]
        if img_name in IMAGEPATHMAP:
            return IMAGEPATHMAP[img_name]
        else:
            return "RA3 %s Icons" % img_name

    def get_json(self, index=-1):
        json_data = {}
        json_data["type"] = "line"
        if index < 0:
            json_data["duration"] = (self.get_end_time() - self.start_time) // 15
        else:
            json_data["duration"] = self.cost_time[index]

        if self.status == 1:
            json_data["kind"] = "success"
        else:
            json_data["kind"] = "fail"

        json_data["unit"] = {}
        json_data["unit"]["country"] = FACTION[self.name[0]]
        json_data["unit"]["kind"] = ""
        if self.name in STRUCTURES[1]:
            json_data["unit"]["kind"] = "Production"
        elif self.name in STRUCTURES[2]:
            json_data["unit"]["kind"] = "Defenses"
        else:
            for k in UNITS:
                if self.name in UNITS[k]:
                    json_data["unit"]["kind"] = k

        if json_data["unit"]["kind"]:
            json_data["unit"]["name"] = self.get_img_name()

        return json_data

    def get_unit_json_from_row_prev(self, row_prev):
        """
        :return: example: {
            "country": "Soviet",
            "kind": "Production",
            "name": "RA3 Crusher Crane Icons",
            "type": "unit",
            "row_prev": 0
        }
        """
        json_data = {}
        json_data["type"] = "unit"
        json_data["row_prev"] = row_prev
        json_data["country"] = FACTION[self.name[0]]
        json_data["kind"] = ""
        if self.name in STRUCTURES[1]:
            json_data["kind"] = "Production"
        elif self.name in STRUCTURES[2]:
            json_data["kind"] = "Defenses"
        else:
            for k in UNITS:
                if self.name in UNITS[k]:
                    json_data["kind"] = k

        if json_data["kind"]:
            json_data["name"] = self.get_img_name()
        return json_data

    def __str__(self):
        return self.name


class PackMCV(object):
    def __init__(self, start_time, uid):
        self.start_time = start_time
        self.cur_id = uid

        self.next_ids = []
        self.deploy = None

    def __str__(self):
        s = "cur id: %s" % self.cur_id
        if self.deploy:
            s += " -> new id: %s" % self.deploy.cur_uid
        return s


class DeployMCV(object):
    def __init__(self, command_time, uid):
        self.prev = None
        self.command_time = command_time
        self.cur_uid = uid

        self.deploy_time = -1
        self.next_id = -1

    def cal_deploy_time(self, build_structure_time):
        # 9 : 1
        self.deploy_time = (self.command_time + 9 * build_structure_time) // 10
        print("cal_deploy_time: ",self.command_time, build_structure_time, self.deploy_time)


class MCVMove(object):
    def __init__(self):
        pass