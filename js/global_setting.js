var SIZE = {
    cell: 100,
    small_cell: 50,

    second: 10, // the length px for 1 second
}

var BOARD = {
    px: 100,
    py: 200,
    hrate: 1.5
}


var STATECOLORS = {
    "wait": "#999999",  // 灰色
    "move": "#FFA500",  // 橙色
    "done": "#32CD32",  // 绿色
    "success": "#4169E1",  // 蓝色
    "fail": "#FF69B4",  // 粉红色
    "record": "#8A2BE2"  // 紫色
}

var LINE_KINDS = ["success", "fail", "move", "unused"]
    

var PATH = {
    image: "images",
    dir_sep: "/",  // directory separator
    img_suf: ".png",  // suffix name for image

    wrong_1: "Invalid image path",
}

var TEXTS = {
    "duration": "time(s)",
    "confirm": "confirm",
    "change_camp_hit": "Modifying the state discards the existing node data.\n"
        +"If you do not save the data, it is recommended to cancel the modification and save it first.\n"
        +"Are you sure you want to modify it?\n"
}


