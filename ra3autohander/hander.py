# usr/bin/env python
# -*- coding:utf-8- -*-
from ra3replay import KWReplayWithCommands
import os
from flowchart import FlowChart


def get_replay(filename):
    replay = KWReplayWithCommands(fname=filename, verbose=False)
    replay.players = [p for p in replay.players if not p.is_commentator()]
    return replay


def get_replaybody_json(filename, pi=-1, replay=None, output=""):
    if replay is None:
        replay = get_replay(filename)
    replay.show_header()
    chunks_str = ""
    chunks_str += "{\n"
    for i, chunk in enumerate(replay.replay_body.chunks):
        if i in [106]:
            print("Debug")
        has_p = False
        cdict = chunk.__dict__
        chunk_str = '  "%s":{"commands": [' % i
        for ci, cmd in enumerate(cdict["commands"]):
            if ci == 0:
                chunk_str += "{"
            else:
                chunk_str += "    {"
            chunk.decode_cmd(cmd)
            if cmd.player_id == pi:
                has_p = True
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
        if pi < 0:
            chunks_str += chunk_str
        elif has_p:
            chunks_str += chunk_str

    chunks_str = chunks_str[:-2] + "\n}"
    if not output:
        suffix = ".json"
        if pi >= 0:
            suffix = "_%s.json" % (pi+1)
        output = os.path.splitext(filename)[0] + suffix
    with open(output, "w") as f:
        f.write(chunks_str)

    return output


def get_chartflow_data(filename, pi=0, replay=None, output=""):
    if replay is None:
        replay = get_replay(filename)

    if replay.players[pi].is_ai:
        return "No Support"

    fc = FlowChart(replay, pi)

    res = fc.check_faction()
    if res <= 0:
        return "Invalid Faction"
    if fc.p_faction == "A":
        fc.parse_a_chunks()
        fc.bind_structures_and_units()
        fc.get_json_from_root()
    elif fc.p_faction == "S":
        fc.parse_s_chunks()
        fc.bind_structures_and_units()
        fc.get_json_from_root()

    if not output:
        output = os.path.splitext(filename)[0] + "_%s_fc.json" % (pi+1)
    fc.save_json(output)

    return output


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
    fname10 = "../replays/yj2801.RA3Replay"
    fname11 = "../replays/这都能翻？.RA3Replay"

    get_replaybody_json(fname11)
    # r = get_chartflow_data(fname7, 0)

    # replay = get_replay(fname2)
    # print(len(replay.replay_body.chunks))