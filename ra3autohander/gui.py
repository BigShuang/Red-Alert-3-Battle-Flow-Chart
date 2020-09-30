# usr/bin/env python
# -*- coding:utf-8- -*-

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from hander import *


class GUI(tk.Frame):
    def __init__(self, master, TEXT, **kwargs):
        self.TEXT = TEXT
        super().__init__(master, **kwargs)
        self.pack()
        self.pack_propagate(0)

        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        browse_file_bt = ttk.Button(top_frame, text=self.TEXT["browse_file"], command=self.browse_file)
        browse_file_bt.pack(side=tk.LEFT)

        self.info = ttk.Label(top_frame, text=self.TEXT["info_1"])
        self.info.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.fn = ""
        self.replay = None

        body_frame = tk.Frame(self, bg=kwargs["bg"])
        body_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        body_frame_1 = tk.Frame(body_frame)
        body_frame_1.pack(side=tk.LEFT)
        # title for player info list
        title = "{:15} {:10} {:5}".format(self.TEXT["name"], self.TEXT["faction"], self.TEXT["team"])
        tk.Label(body_frame_1, text=title).pack(side=tk.TOP)
        self.plist = tk.Listbox(body_frame_1, width=30)
        self.plist.pack(side=tk.TOP)
        self.plist.grid_propagate(0)
        self.init_plist()

        body_frame_2 = tk.Frame(body_frame, bg=kwargs["bg"])
        body_frame_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        export_button_1 = ttk.Button(body_frame_2, text=self.TEXT["export_1"], command=self.export_1)
        export_button_1.pack(side=tk.TOP, fill=tk.X, pady=10)
        export_button_2 = ttk.Button(body_frame_2, text=self.TEXT["export_2"], command=self.export_2)
        export_button_2.pack(side=tk.TOP, fill=tk.X)

        self.show_board = tk.Text(body_frame_2, width=20, height=8, state=tk.DISABLED, fg="blue")
        self.show_board.pack(side=tk.BOTTOM, fill=tk.X)

        bottom_frame = tk.Frame(self, bg=kwargs["bg"])
        bottom_frame.pack(side=tk.BOTTOM, pady=10)
        info_button_1 = ttk.Button(bottom_frame, text=self.TEXT["About"], command=lambda: self.show_result(self.TEXT["Author"]))
        info_button_2 = ttk.Button(bottom_frame, text=self.TEXT["More"], command=lambda: self.show_result(self.TEXT["Details"]))
        info_button_1.pack(side=tk.LEFT, padx=20)
        info_button_2.pack(side=tk.LEFT, padx=20)

        # self.show_result(self.TEXT["Author"])

    def show_result(self, res, kind="normal"):
        self.show_board.config(state="normal")
        self.show_board.delete("1.0", tk.END)
        self.show_board.insert(tk.END, res)
        self.show_board.config(state="disabled")
        if kind == "normal":
            self.show_board.config(fg="blue")
        else:
            self.show_board.config(fg="red")

    def export_1(self):
        items = self.plist.curselection()
        if len(items) == 0:
            self.show_result(self.TEXT["info_1"])
            return
        index = items[0]

        try:
            res = get_chartflow_data(self.fn, index, self.replay)
            if res in self.TEXT:
                res_str = self.TEXT[res]
            else:
                res_str = self.TEXT["OK"] + res
            self.show_result(res_str)
        except Exception as e:
            res_str = self.TEXT["Error"] + str(e)
            self.show_result(res_str, "error")

    def export_2(self):
        if len(self.fn) == 0:
            self.show_result(self.TEXT["info_1"])
            return

        try:
            res = get_replaybody_json(self.fn, -1, self.replay)
            if res in self.TEXT:
                res_str = self.TEXT[res]
            else:
                res_str = self.TEXT["OK"] + res
            self.show_result(res_str)
        except Exception as e:
            res_str = self.TEXT["Error"] + str(e)
            self.show_result(res_str, "error")

    def init_plist(self):
        self.plist.delete(0, tk.END)

    def browse_file(self):
        self.fn = askopenfilename(initialdir="../", title="Select a File",
                                  filetypes=(("RA3Replay files", "*.RA3Replay*"), ("all files", "*.*")))

        self.init_plist()
        if self.fn:
            try:
                self.info.configure(text=self.fn)
                self.show_players()
            except Exception as e:
                self.replay = None
                res_str = self.TEXT["Error"] + str(e)
                self.show_result(res_str, "error")
        else:
            self.info.configure(text=self.TEXT["info_1"])

    def show_players(self):
        self.replay = get_replay(self.fn)
        if self.replay:
            for i in range(len(self.replay.players)):
                p = self.replay.players[i]
                pinfo = "{:15} ".format(p.name)
                if p.is_human_player():
                    pinfo += "{:10} {:5}".format(get_faction(p), p.team)

                self.plist.insert(i + 1, pinfo)



