#!/usr/bin/python3
# coding: utf8
"""

http://www.gamereplays.org/community/index.php?showtopic=706067&st=0&p=7863248&#entry7863248
The decoding of the replays format is credited to R Schneider.

This original code file is from https://github.com/forcecore/KWReplayAutoSaver
I made some changes here to adapt to my project
"""


from kwreplay import KWReplay
from utils import *
import ra3chunks


class ReplayBody:
    def __init__(self, f, game="KW"):
        self.chunks = []
        self.game = game
        self.loadFromStream(f)

    
    def read_chunk(self, f):

        chunk = ra3chunks.RA3Chunk()

        chunk.time_code = read_uint32(f)
        if chunk.time_code == 0x7FFFFFFF:
            return None

        chunk.ty = read_byte(f)
        chunk.size = read_uint32(f)
        chunk.data = f.read(chunk.size)
        # unknown = read_uint32(f) # mostly 0, but not always.
        chunk.unknown_data = f.read(4)
        # chunk debugging stuff:
        #print("chunk pos: 0x%08X" % f.tell())
        #print("read_chunk.time_code: 0x%08X" % chunk.time_code)
        #print("read_chunk.ty: 0x%02X" % chunk.ty)
        #print("read_chunk.size:", chunk.size)
        #print("chunk.data:")
        #print_bytes(chunk.data)
        #print()
    
        chunk.split(self.game)
        return chunk
    
    def loadFromStream(self, f):
        while True:
            chunk = self.read_chunk(f)
            if chunk == None:
                break
            self.chunks.append(chunk)
    
    def print_bo(self):
        print("Dump of known build order related commands")
        print("Time\tPlayer\tAction")
        for chunk in self.chunks:
            chunk.print_bo()
    
    def dump_commands(self):
        print("Dump of commands")
        print("Time\tPlayer\tcmd_id\tparams")
        for chunk in self.chunks:
            chunk.dump_commands()


class KWReplayWithCommands(KWReplay):
    def __init__(self, fname=None, verbose=False):
        self.replay_body = None

        # self.footer_str ... useless
        self.final_time_code = 0
        self.footer_data = None # I have no idea what this is. I'll keep it as it is.
        #self.footer_length = 0

        super().__init__(fname=fname, verbose=verbose)

    def read_footer(self, f):
        footer_str = read_cstr(f, self.FOOTER_MAGIC_SIZE)
        self.final_time_code = read_uint32(f)
        self.footer_data = f.read()
        if self.verbose:
            print("footer_str:", footer_str)
            print("final_time_code:", self.final_time_code)
            print("footer_data:", self.footer_data)
            print()

    # Sometimes, we get invalid player_id in some commands for unknown reason.
    # See cornercases/big_player_id for example.
    # Why do I do this? cos I work with pid as array indexes a lot.
    def fix_pid(self):
        discarded = 0
        for chunk in self.replay_body.chunks:

            # keep valid commands
            commands = []
            for cmd in chunk.commands:
                # invalid player id!
                if cmd.player_id < len(self.players):
                    commands.append(cmd)

            if len(commands) != len(chunk.commands):
                discarded += len(chunk.commands) - len(commands)
                chunk.commands = commands

        print(discarded, "commands with invalid player discarded")

    def loadFromFile(self, fname):
        self.guess_game(fname)
        f = open(fname, 'rb')
        self.loadFromStream(f)
        self.replay_body = ReplayBody(f, game=self.game)
        self.read_footer(f)
        f.close()


def main():
    fname = "1.KWReplay"
    if len(sys.argv) >= 2:
        fname = sys.argv[1]
    kw = KWReplayWithCommands(fname=fname, verbose=False)
    print(fname)
    print()
    kw.replay_body.print_bo()
    print()
    kw.replay_body.dump_commands()


def main_2(fname):

    kw = KWReplayWithCommands(fname=fname, verbose=False)
    print(fname)
    print()
    kw.replay_body.print_bo()
    print()
    kw.replay_body.dump_commands()

if __name__ == "__main__":

    fname = "../replays/盟军vs欧列格.RA3Replay"
    main_2(fname)
    # import os
    # r = os.path.exists(fname)
