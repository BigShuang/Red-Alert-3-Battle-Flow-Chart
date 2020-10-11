from gui import GUI
from tkinter import Tk


TEXT = {
    "title": "RA3 Replay Auto Analysis Tool",

    "info_1": "Choose a replay file first",
    "browse_file": "Select file",
    "export_1": "Export flowchart information",
    "export_2": "Export all commands information",

    "No Support": "Get AI info is not supported",
    "Invalid Faction": "Exporting this faction information is not supported",
    "Error": "Error: ",

    "OK": "Successfully exported to json: \n",
    "name": "Name",
    "faction": "Faction",
    "team": "Team",

    "About": "About Author",
    "More": "More Details",

    "Author": "The author of this tool is Li Big Shuang.\n"
              "His Youtube: https://www.youtube.com/channel/UCxAamo4HH-qMEpepDjHORdQ.\n"
              "His GitHub: https://github.com/BigShuang\n",
    "Details": "See the readme doc for details of the tool: \n"
               "https://github.com/BigShuang/Red-Alert-3-Battle-Flow-Chart",

    "map_name": "Map name: ",
    "factions": {
        "S": "Soviet",
        "E": "Empire",
        "A": "Allied",
        "Rnd": "Random"
    }

}


win = Tk()
win.title(TEXT["title"])
GUI(win, TEXT, width=700, height=400, bg="#ddd")
win.mainloop()
