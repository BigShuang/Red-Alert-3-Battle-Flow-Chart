current_node = null;
current_index = 0
var cur_camp = "Soviet"


function set_selected_camp() {
    $("#camp-select").val(cur_camp);
}

function ClickNode(node_id){
    var rc = node_id.slice(1).split("c")
    var nr = parseInt(rc[0])
    var nc = parseInt(rc[1])
    var cnode = NODE_DATA.data[nr][nc] // TODO: must ensure that IDs are in order
    set_current_node(cnode)
}


function add_row_node(prev_node){
    var new_data = new LineData("unused",10)
    var new_node = new DataNode(prev_node.r, prev_node.c + 1,new_data)

    var prev_next = prev_node.next

    new_node.prev = prev_node
    prev_node.next = new_node

    if(prev_next){
        NODE_DATA.data[prev_node.r].splice(new_node.c,0,new_node)

        for(var ri = prev_node.r; ri < NODE_DATA.data.length; ri++){
            if(NODE_DATA.data[ri][new_node.c - 1] === null){
                NODE_DATA.data[ri].unshift(null)
            }
        }
    }else{
        NODE_DATA.data[prev_node.r].push(new_node)
    }
    
    // refresh width, height, left, top
    new_node.refresh_layout()

    if(prev_next){
        prev_next.prev = new_node
        new_node.next = prev_next

        prev_next.refresh_self_and_children("add")
    }

    $(".main-board").append(new_node.get_html())
    var cell = $(".main-board").find(".line-node#"+new_node.get_nid())

    TIME_DATA[prev_node.r] = NODE_DATA.data[prev_node.r][NODE_DATA.data[prev_node.r].length-1].get_end_time()
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


function add_col_node(row_prev_node){
    // create a node in a new row
    var new_data = new UnitData("", "", "")
    if(row_prev_node.data.get_type() == "unit"){
        new_data.set_all(row_prev_node.data.country, row_prev_node.data.kind, row_prev_node.data.name)
    }else if(row_prev_node.data.get_type() == "line" && row_prev_node.data.unit){
        new_data.set_all(row_prev_node.data.unit.country, row_prev_node.data.unit.kind, row_prev_node.data.unit.name)
    }else{
        return
    }

    var new_node = new DataNode(NODE_DATA.data.length, row_prev_node.c, new_data)

    new_node.row_prev = row_prev_node
    row_prev_node.row_next = new_node

    NODE_DATA.data.push([])
    for(var i = 0; i< new_node.c; i++){
        NODE_DATA.data[new_node.r].push(null)
    }
    NODE_DATA.data[new_node.r].push(new_node)
    TIME_DATA[new_node.r] = new_node.get_end_time()

    $(".main-board").append(new_node.get_html())
    var cell = $(".main-board").find(".cell-node#"+new_node.get_nid())

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


function add_base_cell(start_time){
    var pobj = $(".main-board")

    var blank_data = new UnitData("","","")
    if(start_time > 0){
        blank_data.start_time = start_time
    }
    
    var blank_node = new DataNode(0,0,blank_data)
    
    NODE_DATA.root = blank_node
    NODE_DATA.data = [
        [blank_node]
    ]
    TIME_DATA[0] = blank_node.data.start_time

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


function delete_row_and_children(anode){
    var del_r = anode.r
    // 1 - delete the col-line html for the first node
    // 2 - for all nodes in the row, then delete the node html, then delete_row_and_children if it has a row
    // 3 - delete the row data from the NODE_DATA
    // 4 - all nodes below this anode.r: r minus 1 

    // the deletion will be done out of the funciton, in fact , it will delete all col-line html below the anode
    // $("#" + anode.get_clid()).remove()
    for(var ci = 0; ci < NODE_DATA.data[del_r].length; ci++){
        if(NODE_DATA.data[del_r][ci]){
            // the deletion of the node html will be done out of the funciton, in fact , it will delete all nodes' html below the anode
            // $("#" + NODE_DATA.data[del_r][ci].get_nid()).remove()
            if(NODE_DATA.data[del_r][ci].row_next){
                delete_row_and_children(NODE_DATA.data[del_r][ci].row_next)
            }
        }
    }

    NODE_DATA.data.splice(del_r, 1)
    for(var ri = del_r; ri < NODE_DATA.data.length; ri++){
        for(var ci = 0; ci < NODE_DATA.data[ri].length; ci++){
            if(NODE_DATA.data[ri][ci]){
                NODE_DATA.data[ri][ci].r -= 1
            }
        }
    }
}


function delete_node(anode){
    if(anode.prev){
        anode.prev.next = anode.next
    }

    if(anode.next){
        anode.next.prev = anode.prev
    }
    
    var del_r = -1

    if(anode.row_next){
        var del_r = anode.row_next.r
    }else if(anode.row_prev){
        var del_r = anode.r
    }
    
    if(del_r >= 0){
        // delete all nodes' html below the anode
        for(var ri = del_r; ri < NODE_DATA.data.length; ri++){
            for(var ci = 0; ci < NODE_DATA.data[ri].length; ci++){
                var i_node = NODE_DATA.data[ri][ci]
                if(i_node){
                    $("#" + i_node.get_nid()).remove()
                    if(i_node.row_prev){
                        $("#" + i_node.get_clid()).remove()
                    }
                }
            }
        }

        delete_row_and_children(NODE_DATA.data[del_r][anode.c])

        // regenerate all nodes' html below the anode
        for(var ri = del_r; ri < NODE_DATA.data.length; ri++){
            for(var ci = 0; ci < NODE_DATA.data[ri].length; ci++){
                var i_node = NODE_DATA.data[ri][ci]
                if(i_node){
                    i_node.refresh_content()
                    i_node.refresh_layout()
                    i_node.set_css(null, false)
                }
            }

            TIME_DATA[ri] = NODE_DATA.data[ri][NODE_DATA.data[ri].length-1].get_end_time()
        }

        // a fast way to delete all item in TIME_DATA whose index beyond the NODE_DATA.data.length
        TIME_DATA.length = NODE_DATA.data.length
    }

    // TODO change
    if(!anode.row_prev){
        // not the start node of a row, which has been delete in the previous code
        if(anode.next){
            // have next node
            NODE_DATA.data[anode.r].splice(anode.c,1)

            for(var ri = anode.r+1; ri < NODE_DATA.data.length; ri++){
                if(NODE_DATA.data[ri][anode.c] === null){
                    NODE_DATA.data[ri].shift(null)
                }
            }
    
            $("#" + anode.get_nid()).remove()
            anode.next.refresh_self_and_children("remove")
        }else{
            $("#" + anode.get_nid()).remove()
            NODE_DATA.data[anode.r].pop()
        }
        TIME_DATA[anode.r] = NODE_DATA.data[anode.r][NODE_DATA.data[anode.r].length-1].get_end_time()
    }

    refresh_timeline()
    deselect_current()
}

function set_current_node(anode){
    // add functional buttons for current node
    $(".current-node").removeClass("current-node")
    $(".current-node-button").remove() 

    current_node = anode 

    // button to add node in a row
    html_1 = `<div class="node-button-1 add-node current-node-button" 
    style="margin-left: ${current_node.left + current_node.width}px;margin-top: ${current_node.top + current_node.height / 2  - 15 }px;">
    <img src="images/icons/add.png"></div>`
    // button to add node in a new row 
    html_2 = `<div class="node-button-1 add-row current-node-button" 
    style="margin-left: ${current_node.left + current_node.width - 15}px;margin-top: ${current_node.top + current_node.height}px;">
    <img src="images/icons/add_row.png"></div>`
    // button to delete node self
    html_3 = `<div class="node-button-1 delete-node current-node-button" 
    style="margin-left: ${current_node.left + current_node.width - 15}px;margin-top: ${current_node.top - 15}px;">
    <img src="images/icons/delete.png"></div>`

    var cell = $(".main-board").find("#"+current_node.get_nid())
    cell.addClass("current-node")
    $(".main-board").append(html_1)
    $(".add-node.current-node-button").on("click", function() {
        add_row_node(current_node)
    })

    if(current_node != NODE_DATA.root){
        $(".main-board").append(html_3)
        $(".delete-node.current-node-button").on("click", function() {
            delete_node(current_node)
        })
    }

    if(current_node.data.get_type() == "line" && current_node.data.unit != null){
        $(".main-board").append(html_2)

        $(".add-row.current-node-button").on("click", function() {
            add_col_node(current_node)
        })
    }

    if(current_node.data.get_type() == "unit"){
        show_side_bar(cur_camp, current_node)
    }else if(current_node.data.get_type() == "line"){
        show_side_bar_for_line_node(cur_camp, current_node)
    }
}


function deselect_current(){
    $(".current-node").removeClass("current-node")
    $(".current-node-button").remove() 

    current_node = null
    
    hide_side_bar()
}

function init_board(){
    var html=`<div class="begin-tip"><div>${TEXTS.init.select_country}: <select class="custom-select" id="camp-select">`
    for(camp of CAMPS){
        html += `<option value="${camp}">${TEXTS.camps[camp]}</option>`
    }
    html += `</select>${TEXTS.init.start_time}: <input class="custom-select" type="number" name="start-time" value="0"/>
        </div>
        <div class="begin-draw">${TEXTS.init.first}<br>${TEXTS.init.then}</div>
    </div>`

    $(".main-board").html(html)


    $(".begin-draw").on("dblclick",
        function(){
            if(NODE_DATA.data.length == 0) {
                cur_camp = $("#camp-select").val()
                $("#current-camp").html(TEXTS.camps[cur_camp]);
                var start_time = $('input[type="number"][name="start-time"]').val()
                start_time = parseInt(start_time)
                $(".main-board").html("")
                add_base_cell(start_time)
            }
        }
    )
}


function generate_data_json(){
    var json_data = {}
    json_data.camp = cur_camp
    if(NODE_DATA.root){
        json_data.root = NODE_DATA.root.get_nid()
    }else{
        json_data.root = null
    }
    json_data.data = []

    for(row of NODE_DATA.data){
        var row_json = []
        for(node of row){
            if(node){
                row_json.push(node.get_json())
            }else{
                row_json.push(null)
            }
        }

        json_data.data.push(row_json)
    }

    return JSON.stringify(json_data, null, '  ')
}

function generate_html_from_json(json){
    var json_data = JSON.parse(json)
    console.log(json_data)
    if(json_data.root == null || json_data.camp == null || !CAMPS.includes(json_data.camp)) {
        return 
    }

    cur_camp = json_data.camp
    $("#current-camp").html(TEXTS.camps[cur_camp]);
    var rc = json_data.root.slice(1).split("c")
    var nr = parseInt(rc[0])
    var nc = parseInt(rc[1])


    var pobj = $(".main-board")
    pobj.html("")
    for(var ri=0; ri<json_data.data.length; ri++) {
        //  create new row in data
        NODE_DATA.data[ri] = []
        for(var ci=0; ci<json_data.data[ri].length; ci++){
            var i_json = json_data.data[ri][ci]
            if(i_json==null){
                NODE_DATA.data[ri][ci] = null
                continue
            }
            
            if(i_json.type == "unit"){
                var i_data = new UnitData(i_json.country,i_json.kind,i_json.name)
                if(i_json.start_time && i_json.start_time>0){
                    i_data.start_time = i_json.start_time
                }
            }else{
                var i_data = new LineData(i_json.kind,i_json.duration)
                if(i_json.unit){
                    i_data.set_unit(i_json.unit.country,i_json.unit.kind,i_json.unit.name)
                }
            }

            var i_node = new DataNode(ri,ci,i_data)

            if(ri==nr && ci == nc){
                ;
            } else if(i_json.row_prev != null){
                i_node.row_prev = NODE_DATA.data[i_json.row_prev][ci]
                NODE_DATA.data[i_json.row_prev][ci].row_next = i_node
            }else{
                i_node.prev = NODE_DATA.data[ri][ci-1]
                NODE_DATA.data[ri][ci-1].next = i_node
            }

            pobj.append(i_node.get_html())
            var cell = pobj.find(".basic-node#"+i_node.get_nid())

            i_node.refresh_layout()
            i_node.set_css(cell)
                    
            NODE_DATA.data[ri][ci] = i_node
        }
    }

    NODE_DATA.root = NODE_DATA.data[nr][nc]

    $(".basic-node").on("click", function(){
        if(! $(this).hasClass("current-node")){
            var nid = $(this).attr("id")
            ClickNode(nid)
        }
    })

    // regenerate all nodes' html below the anode
    for(var ri = 0; ri < NODE_DATA.data.length; ri++){
        TIME_DATA[ri] = NODE_DATA.data[ri][NODE_DATA.data[ri].length-1].get_end_time()
    }

    // a fast way to delete all item in TIME_DATA whose index beyond the NODE_DATA.data.length
    TIME_DATA.length = NODE_DATA.data.length
    refresh_timeline()
}



$(document).ready(function(){
    init_board()
    show_icon_info()
    set_selected_camp()

    $(".cell-node").on("click", function(){
        // set clicked node a)s current node
    })

    $(".clict-to-deselect").on("click", function(){
        deselect_current()
    })

    $(".save-load-button").on("click", function(){
        var data_json_str = generate_data_json(NODE_DATA)
        $("#nodes-data").val(data_json_str)
        $(".popup").show()
    })


    $("#pupup-button-return").on("click", function(){
        $(".popup").hide()
    })

    // copy data in text area to Clipboard
    $("#pupup-button-copy").on("click", function(){
        var data_area = $("#nodes-data")
        data_area.focus()
        data_area.select()

        try {
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
            console.log('Fallback: Copying text command was ' + msg);
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
        }
    })

    // copy data in text area to Clipboard
    $("#pupup-button-load").on("click", function(){
        var json = $("#nodes-data").val()
        generate_html_from_json(json)
        deselect_current()
    })
})
