var SIZE = {
    cell: 100,
    small_cell: 50,

    second: 10, // the length px for 1 second
}

var BOARD = {
    px: 100,
    py: 200,
    hrate: 1.5,
    CLW: 10,  // col line width, Associated with css width of col line
    RLW: 12, // row line width
}

var CAMPS = ["Soviet", "Allied", "Imperial"]


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
        +"Are you sure you want to modify it?\n",
    "line_kinds": ["success", "fail", "move", "unused"],

    
}


var TIMELINE = {
    min_unit: 30,
    init: 2,

}
