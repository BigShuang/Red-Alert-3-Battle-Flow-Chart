# usr/bin/env python
# -*- coding:utf-8- -*-
from ra3replay import KWReplayWithCommands
import os


def get_replaybody_json(filename, output = ""):
    replay = KWReplayWithCommands(fname=filename, verbose=False )
    chunk_str = ""
    chunk_str += "{\n"
    for ci, chunk in enumerate(replay.replay_body.chunks):
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
    fname2 = "../replays/盟军vs欧列格.RA3Replay"
    fname3 = "../replays/yj1801.RA3Replay"
    fname4 = "../replays/yj2102.RA3Replay"
    fname5 = "../replays/yj2103.RA3Replay"

    get_replaybody_json(fname5)