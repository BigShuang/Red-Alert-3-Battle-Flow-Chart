current_node = null;
current_index = 0
var cur_camp = "Soviet"
node_data = {
    root: null,
    data:[

    ]
}
function set_selected_camp() {
    $("#camp-select").val(cur_camp);
}

function ChangeCamp(camp){
    if(node_data.data.length > 0){
        var r = confirm(TEXTS["change_camp_hit"]);
        if (r == true) {
            cur_camp = camp
            node_data = {
                root: null,
                data:[]
            }
        } else {
            set_selected_camp()
        }
    }else{
        cur_camp = camp
    }
}

function ClickNode(node_id){
    var rc = node_id.slice(1).split("c")
    var nr = parseInt(rc[0])
    var nc = parseInt(rc[1])
    var cnode = node_data.data[nr][nc] // TODO: must ensure that IDs are in order
    set_current_node(cnode)
}


function add_row_node(datanode){
    var new_data = new LineData("unused",10)
    var new_node = new DataNode(datanode.r, datanode.c + 1,new_data)

    new_node.prev = datanode
    datanode.next = new_node

    node_data.data[datanode.r].push(new_node)
    $(".main-board").append(new_node.get_html())
    var cell = $(".main-board").find(".line-node#"+new_node.get_nid())

    // refresh width, height, left, top
    new_node.refresh_layout()
    // set position css 
    new_node.set_css(cell)

    set_current_node(new_node)

    $(cell).on("click", function(){
        if(! $(this).hasClass("current-node")){
            var nid = $(this).attr("id")
            ClickNode(nid)
        }
    })
   
    return cell
}


function add_base_cell(parent){
    var pobj = $(parent)

    var blank_data = new UnitData("","","")
    var blank_node = new DataNode(0,0,blank_data)
    node_data.root = blank_node
    node_data.data = [
        [blank_node]
    ]

    pobj.append(blank_node.get_html())
    var cell = pobj.find(".cell-node#"+blank_node.get_nid())

    blank_node.refresh_layout()
    blank_node.set_css(cell)

    set_current_node(blank_node)

    $(cell).on("click", function(){
        if(! $(this).hasClass("current-node")){
            var nid = $(this).attr("id")
            ClickNode(nid)
        }
    })
   
    return cell
}

function set_current_node(anode){
    // add functional buttons for current node
    $(".current-node").removeClass("current-node")
    $(".current-node-button").remove() 

    current_node = anode 

    html_1 = `<div class="node-button-1 add-node current-node-button" 
    style="margin-left: ${current_node.left + current_node.width}px;margin-top: ${current_node.top + current_node.height / 2  - 15 }px;">
    <img src="images/icons/add.png"></div>`
    html_2 = `<div class="node-button-1 add-row current-node-button" 
    style="margin-left: ${current_node.left + current_node.width - 15}px;margin-top: ${current_node.top + current_node.height}px;">
    <img src="images/icons/add_row.png"></div>`

    var cell = $(".main-board").find("#"+current_node.get_nid())
    cell.addClass("current-node")
    $(".main-board").append(html_1)
    $(".main-board").append(html_2)

    $(".add-node.current-node-button").on("click", function() {
        add_row_node(current_node)
    })

    if(current_node.data.get_type() == "unit"){
        show_side_bar(cur_camp, current_node)
    }else if(current_node.data.get_type() == "line"){
        show_side_bar_for_line_node(cur_camp, current_node)
    }
}


function init_board(){
    $(".main-board").on("dblclick",
        function(){
            if(node_data.data.length == 0) {
                add_base_cell(this)
            }
        }
    )
}


function generate_data_json(data){

}

function generate_html_from_json(json){
    // TODO
}

$(document).ready(function(){
    init_board()
    set_selected_camp()

    $(".cell-node").on("click", function(){
        // set clicked node as current node

    })
})
