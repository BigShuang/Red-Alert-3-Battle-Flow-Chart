# usr/bin/env python3
# -*- coding:utf-8- -*-
from gui import GUI
from tkinter import Tk


TEXT = {
    "title": "RA3录像自动分析工具",

    "info_1": "请先选择一个录像文件",
    "browse_file": "选择文件",
    "export_1": "导出流程图信息",
    "export_2": "导出所有命令信息",

    "No Support": "无法获取电脑的操作",
    "Invalid Faction": "不支持该阵营（帝国）",
    "Error": "报错: ",

    "OK": "成功导出到json文件: \n",
    "name": "玩家名",
    "faction": "阵营",
    "team": "队伍",

    "About": "关于作者",
    "More": "详细信息",

    "Author": "该工具作者是大爽歌.\n"
              "他的b站: https://space.bilibili.com/149259132\n"
              "他的GitHub: https://github.com/BigShuang"
              "他的CSDN: https://blog.csdn.net/python1639er\n",
    "Details": "详情请查看该工具的readme文档: \n"
               "https://github.com/BigShuang/Red-Alert-3-Battle-Flow-Chart",
}


win = Tk()
win.title(TEXT["title"])
GUI(win, TEXT, width=700, height=400, bg="#ddd")
win.mainloop()