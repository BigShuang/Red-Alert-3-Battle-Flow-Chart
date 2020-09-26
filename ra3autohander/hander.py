# usr/bin/env python
# -*- coding:utf-8- -*-
from ra3replay import KWReplayWithCommands
import os
from flowchart import FlowChart





def get_replaybody_json(filename, output = ""):
    replay = KWReplayWithCommands(fname=filename, verbose=False )
    replay.show_header()
    chunk_str = ""
    chunk_str += "{\n"
    for ci, chunk in enumerate(replay.replay_body.chunks):
        if ci in [106]:
            print("Debug")

        cdict = chunk.__dict__
        chunk_str += '  "%s":{"commands": [' % ci
        for ci, cmd in enumerate(cdict["commands"]):
            if ci == 0:
                chunk_str += "{"
            else:
                chunk_str += "    {"
            chunk.decode_cmd(cmd)
            chunk_str += '"name": "%s", ' % cmd
            cmdict = cmd.__dict__

            for ck in cmdict:

                cv = cmdict[ck]
                if isinstance(cv, int):
                    chunk_str += '"%s": %s, ' % (ck, cv)
                elif isinstance(cv, bytes):
                    cv_str = " ".join(hex(cvv)[2:] for cvv in cv)
                    chunk_str += '"%s": "%s", ' % (ck, cv_str)
                elif isinstance(cv, list):
                    chunk_str += '"%s": %s, ' % (ck, cv)
                else:
                    chunk_str += '"%s": "%s", ' % (ck, cv)
            chunk_str = chunk_str[: -2]

            chunk_str += "}"
            if ci < len(cdict["commands"]) - 1:
                chunk_str += ",\n"
        chunk_str += "],\n    "

        for bk in ["data", "payload"]:
            if bk in cdict:
                bv = cdict[bk]
                if bv:
                    bv_str = " ".join(hex(bvv)[2:] for bvv in bv)
                    chunk_str += '"%s": "%s",\n    ' % (bk, bv_str)
                else:
                    chunk_str += '"%s": "%s", ' % (bk, bv)

        for k in cdict:
            if k not in ["commands", "data", "payload"]:
                v = cdict[k]
                if v is None:
                    chunk_str += '"%s": "%s", ' % (k, v)
                elif isinstance(v, bytes):
                    v_str = " ".join(hex(vv)[2:] for vv in v)
                    chunk_str += '"%s": "%s", ' % (k, v_str)
                else:
                    chunk_str += '"%s": %s, ' % (k, v)
        chunk_str = chunk_str[: -2]
        chunk_str += "},\n"
        if ci > 2000:
            break
    chunk_str = chunk_str[:-2] + "\n}"
    if not output:
        output = os.path.splitext(filename)[0] + ".json"
    with open(output, "w") as f:
        f.write(chunk_str)


def get_chartflow_data(filename, output=""):
    replay = KWReplayWithCommands(fname=filename, verbose=False )

    fc = FlowChart(replay)

    res = fc.check_faction()
    if res <= 0:
        print("invalid faction")
        return

    fc.parse_a_chunks()
    fc.bind_structures_and_units()
    fc.get_allied_json()

    print()
    if not output:
        output = os.path.splitext(filename)[0] + "_fc.json"
    fc.save_json(output)


def main(filename):
    replay = KWReplayWithCommands(fname=filename, verbose=False )
    # replay.replay_body.print_bo()
    # print("====================")
    # replay.replay_body.dump_commands()
    # print("Dump of commands")
    # print("Time\tPlayer\tcmd_id\tparams")
    chunk_str = ""
    chunk_str += "{\n"
    for ci, chunk in enumerate(replay.replay_body.chunks):
        # print(ci, "(-%s-)" % chunk.time_code, end=": ")
        # chunk.dump_commands()
        cdict = chunk.__dict__
        # cmds = [cmd.__dict__ for cmd in cdict["commands"]]
        chunk_str += '  "%s":{"commands": [' % ci
        for ci, cmd in enumerate(cdict["commands"]):
            if ci == 0:
                chunk_str += "{"
            else:
                chunk_str += "    {"
            cmdict = cmd.__dict__
            for ck in cmdict:
                cv = cmdict[ck]
                if isinstance(cv, int):
                    chunk_str += '"%s": %s, ' % (ck, cv)
                elif isinstance(cv, bytes):
                    cv_str = " ".join(hex(cvv)[2:] for cvv in cv)
                    chunk_str += '"%s": "%s", ' % (ck, cv_str)
                else:
                    chunk_str += '"%s": "%s", ' % (ck, cv)
            chunk_str = chunk_str[: -2]

            chunk_str += "}"
            if ci < len(cdict["commands"]) - 1:
                chunk_str += ",\n"
        chunk_str += "],\n    "

        for bk in ["data", "payload"]:
            if bk in cdict:
                bv = cdict[bk]
                if bv:
                    bv_str = " ".join(hex(bvv)[2:] for bvv in bv)
                    chunk_str += '"%s": "%s",\n    ' % (bk, bv_str)
                else:
                    chunk_str += '"%s": "%s", ' % (bk, bv)

        for k in cdict:
            if k not in ["commands", "data", "payload"]:
                v = cdict[k]
                if v is None:
                    chunk_str += '"%s": "%s", ' % (k, v)
                else:
                    chunk_str += '"%s": %s, ' % (k, v)
        chunk_str = chunk_str[: -2]
        chunk_str += "},\n"
        # print(chunk.__dict__)
        if ci > 2000:
            break
    chunk_str += "}"
    print(chunk_str)

if __name__ == "__main__":

    fname = "../replays/yj1601.RA3Replay"
    fname2 = "../replays/33nd.RA3Replay"
    fname3 = "../replays/yj1902.RA3Replay"
    fname4 = "../replays/yj2102.RA3Replay"
    fname5 = "../replays/yj2103.RA3Replay"
    fname6 = "../replays/yj2201.RA3Replay"
    fname7 = "../replays/学习垄断哥苏联.RA3Replay"
    fname8 = "../replays/yj2401.RA3Replay"

    fname9 = "../replays/盟军vs欧列格.RA3Replay"
    fname10 = "../replays/yj2501.RA3Replay"

    # get_replaybody_json(fname9)
    get_chartflow_data(fname9)