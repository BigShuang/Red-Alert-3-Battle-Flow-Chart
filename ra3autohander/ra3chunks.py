# !/usr/bin/python3
# coding: utf8
"""

http://www.gamereplays.org/community/index.php?showtopic=706067&st=0&p=7863248&#entry7863248
The decoding of the replays format is credited to R Schneider.

This code file is from https://github.com/forcecore/KWReplayAutoSaver
"""


import chunks
from game_config import *


class RA3Chunk(chunks.Chunk):

    def is_bo_cmd(self, cmd):
        return cmd.cmd_id in BO_COMMANDS

    def is_known_cmd(self, cmd):
        return cmd.cmd_id in CMDNAMES

    def resolve_known(self, cmd):
        return CMDNAMES[cmd.cmd_id]

    # Decode decodable commands
    def decode_cmd(self, cmd):
        # hide some distracting commands
        if cmd.cmd_id == 0x21:
            cmd.cmd_ty = chunks.Command.HIDDEN  # lets forbid this from showing.

        if cmd.cmd_id == 0x09:
            cmd.decode_placedown_cmd(UNITNAMES, UNITCOST, FREEUNITS)
        elif cmd.cmd_id == 0x05:
            cmd.decode_ra3_queue_cmd(UNITNAMES, AFLD_UNITS, UNITCOST)
        elif cmd.cmd_id == 0x06:
            cmd.decode_ra3_hold_cmd(UNITNAMES)
        elif cmd.cmd_id == 0x00:
            cmd.decode_ra3_deploy_cmd()
        elif cmd.cmd_id == 0x14:
            cmd.decode_move_cmd()
        elif cmd.cmd_id == 0x0A:
            cmd.decode_sell_cmd()
        elif cmd.cmd_id == 0x2c:
            cmd.decode_formation_move_cmd()
        elif cmd.cmd_id == 0x36:
            cmd.decode_reverse_move_cmd()
        elif cmd.cmd_id == 0x4E:
            cmd.decode_science_sel_cmd(SCIENCENAMES)
        elif cmd.cmd_id == 0xFF:
            cmd.decode_skill_xy(POWERNAMES, POWERCOST)
        elif cmd.cmd_id == 0x01:
            # sometimes, GG
            cmd.decode_skill_target(POWERNAMES, POWERCOST)
        elif cmd.cmd_id == 0x03:
            cmd.decode_upgrade_cmd(UPGRADENAMES, UPGRADECOST)
        elif cmd.cmd_id == 0xFE:
            cmd.decode_skill_targetless(POWERNAMES, POWERCOST)
        elif cmd.cmd_id == 0x32:
            cmd.decode_skill_2xy(POWERNAMES, POWERCOST)

        #if cmd.cmd_id == 0x01:
        #    cmd.decode_gg()
        # Fortunately, we don't have target skill, in the sidebar skills, in TW.
        #elif cmd.cmd_id == 0x??:
        #    cmd.decode_skill_target(POWERNAMES, POWERCOST)
