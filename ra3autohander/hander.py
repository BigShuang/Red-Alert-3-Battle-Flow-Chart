# usr/bin/env python
# -*- coding:utf-8- -*-
from chunks import KWReplayWithCommands


def main(filename):
    replay = KWReplayWithCommands(fname=filename, verbose=False )
    # print(fname)
    replay.replay_body.print_bo()
    print("====================")
    # replay.replay_body.dump_commands()
    print("Dump of commands")
    print("Time\tPlayer\tcmd_id\tparams")
    for ci, chunk in enumerate(replay.replay_body.chunks):
        print(ci, "-%s-"%chunk.time_code, end=": ")
        if ci in [25, 41]:
            print("pause")
        chunk.dump_commands()


if __name__ == "__main__" :

    fname = "../replays/yj1601.RA3Replay"
    main(fname)