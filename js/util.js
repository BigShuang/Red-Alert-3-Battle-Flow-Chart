var TIME_DATA = []
var NODE_DATA = {
    root: null,
    data:[

    ]
}

var last_tnum = null

$(document).ready(function(){
    $win = $(".float-window-bar")
    $win.bind("mousedown",function(event){
        /* 获取需要拖动节点的坐标 */
        var win_parent = $(this).parent()
        var offset_x = $(win_parent)[0].offsetLeft;//x坐标
        var offset_y = $(win_parent)[0].offsetTop;//y坐标
        /* 获取当前鼠标的坐标 */
        var mouse_x = event.pageX;
        var mouse_y = event.pageY;
        // console.log("click mouse xy: ",mouse_x, mouse_y)
        /* 绑定拖动事件 */

        $(this).bind("mousemove",function(ev){
            /* 计算鼠标移动了的位置 */
            var _x = ev.pageX - mouse_x;
            var _y = ev.pageY - mouse_y;
            // console.log("mouse move xy: ",_x, _y)
            
            /* 设置移动后的元素坐标 */
            var now_x = (offset_x + _x ) + "px";
            var now_y = (offset_y + _y ) + "px";

            // console.log("result xy: ",now_x, now_y)
            /* 改变目标元素的位置 */
            $(win_parent).css({
                "top":now_y,
                "left":now_x
            })
        })
    })

    /* 当鼠标左键松开，接触事件绑定 */
    $win.bind("mouseup",function(){
        $(this).unbind("mousemove");
    })

    $win.bind("mouseleave",function(){
        $(this).unbind("mousemove");
    })


    
})

function show_side_bar(camp, cur_node) {
    // add menu to side bar
    var node_html = `<div class="nodes-menu">`

    set_node_menu(camp, node_html)

    $("ul.menu-unit-items li").on("click", function(){
        var unitname = $(this).data("unit-name")
        var unitkind = $(this).data("unit-kind")
        if(cur_node){
            cur_node.data.set_all(camp, unitkind, unitname)
            cur_node.refresh_content()
        }
    })
}

function show_side_bar_for_line_node(camp, cur_node) {
    // add menu to side bar
    var line_kind = "move"
    var duration = 10
    if(cur_node && cur_node.data){
        line_kind = cur_node.data.kind
        duration = cur_node.data.duration
    }
   
    var node_html = `<div class="line-menu"><ul>`
    for (lk of LINE_KINDS){
        if(lk == line_kind){
            node_html += `<li><input type="radio" name="line-kind" value="${lk}" id="${lk}-line" checked>
            <label class="${lk}-line-text" for="${lk}-line">${lk}</label></li>`
        }else{
            node_html += `<li><input type="radio" name="line-kind" value="${lk}" id="${lk}-line">
            <label class="${lk}-line-text" for="${lk}-line">${lk}</label></li>`
        }
    }

    node_html += `</ul><span>${TEXTS["duration"]}: </span><input type="number" name="duration-time" value="${duration}"/>
    <input type="button" value="${TEXTS["confirm"]}" id="confirm-line"/></div><div class="nodes-menu">`

    set_node_menu(camp, node_html)

    if(line_kind == "unused" || line_kind == "move"){
        $("#bar-body .nodes-menu").hide()
    }

    $("ul.menu-unit-items li").on("click", function(){
        var unitname = $(this).data("unit-name")
        var unitkind = $(this).data("unit-kind")

        if(cur_node){
            cur_node.data.set_unit(camp, unitkind, unitname)
            cur_node.refresh_content()
        }
    })

    $("input#confirm-line").on("click", function(){
        var line_kind = $('input[type="radio"][name="line-kind"]:checked').val()
        var duration = $('input[type="number"][name="duration-time"]').val()
        duration = parseInt(duration)
        if(duration<=0){
            alert("Duration must be greater than 0.")
            return
        }
    
        if(line_kind == "unused" || line_kind == "move"){
            $("#bar-body .nodes-menu").hide()
            cur_node.data.set_unit()
        }else{
            $("#bar-body .nodes-menu").show()
            if(!cur_node.data.unit){
                cur_node.data.set_unit("","","")
            }
        }
    
        cur_node.data.set_k_d(line_kind, duration)
        TIME_DATA[cur_node.r] = NODE_DATA.data[cur_node.r][NODE_DATA.data[cur_node.r].length-1].get_end_time()

        cur_node.refresh_layout()
        cur_node.set_css()
        cur_node.refresh_content()
        set_current_node(cur_node)
        cur_node.refresh_self_and_children()

    })
}

function set_node_menu(camp, html) {
    var camp_imgs = node_imgs[camp]
    for(kind in camp_imgs){
        var menu_kind = kind.split(" ").join("_")
        html += `<div class="kind-menu"><h3 data-kind-name="${menu_kind}" data>${kind}</h3>`
        html += `<ul class="menu-unit-items menu-${menu_kind}">`
        for(unit in camp_imgs[kind]){
            html += `<li data-unit-kind="${kind}" data-unit-name="${unit}"><img src="${camp_imgs[kind][unit]}"></li>`
        }
        html += `</ul></div>`
    }
    html += `</div>`
    $("#bar-body").html(html)
    $(".sidebar").show()

    // Click to expand or collapse the items of node kind menu
    $(".kind-menu h3").on("click", function(){
        if($(this).hasClass("active-menu")){
            $(`ul.active-menu, h3.active-menu`).removeClass("active-menu")
        }
        else {
            $(`ul.active-menu, h3.active-menu`).removeClass("active-menu")
            var kind = $(this).data("kind-name");
            $(this).addClass("active-menu")
            $(`ul.menu-${kind}`).addClass("active-menu")
        }
    })
}

function get_img_src(country, kind, name){
    return node_imgs[country][kind][name]
}


function hide_side_bar(){
    $(".sidebar").hide()
}

function get_time_str_by_num(tnum){
    var t = tnum * TIMELINE.min_unit
    var m = Math.floor(t / 60)
    var s = t % 60
    if(s<10){
        return `${m}:0${s}`
    }else{
        return `${m}:${s}`
    }
     
}

function refresh_timeline(){
    var max_t = Math.max(...TIME_DATA)

    var t_num = Math.ceil(max_t / TIMELINE.min_unit )

    var t_num = Math.max(t_num, TIMELINE.init)

    if(last_tnum == null){
        var html = ""
        for(var i = 0; i<= t_num; i++){
            html += `<div class="time-scale" id="t${i}">${get_time_str_by_num(i)}</div>`
        }
        $(".time-axis").append(html)
    }else if(last_tnum < t_num){
        var html = ""
        for(var i = last_tnum + 1; i<= t_num; i++){
            html += `<div class="time-scale" id="t${i}">${get_time_str_by_num(i)}</div>`
        }
        $(".time-axis").append(html)
    }else if(last_tnum > t_num){
        var html = ""
        for(var i = t_num + 1; i<= last_tnum; i++){
            $("#t" + i).remove()
        }
    }

    last_tnum = t_num
}

function show_icon_info(){
    var html = ""
    for (lk of LINE_KINDS){
        html += `<li><span class="line ${lk}-line"></span><span class="${lk}-line-text">${lk}</span></li>`
    }
    html += `<li>Offline numbers are time consuming</li>`

    $(".icon-info-board").html(html)
}
