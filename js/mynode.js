class UnitData {
    constructor(country, kind, name) {
        this.country = country || ""
        this.kind = kind || ""
        this.name = name || ""
        this.start_time = 0
    }
    
    set_all(country, kind, name){
        this.country = country
        this.kind = kind
        this.name = name
    }

    get_stary_px(){
        return this.start_time * SIZE.second
    }

    get_img(){
        if(this.country == "" || this.kind == "" || this.name == ""){
            return ""
        }else {
            var img_p = get_img_src(this.country, this.kind, this.name)

            return `<img src="${img_p}" class="unit-img ${this.kind}-unit" alt="${PATH.wrong_1}"/>`
        }
    }

    get_div(nid){
        var html = '<div class="basic-node cell-node" id="' + nid + '">' + this.get_img() + '</div>'
        return html
    }

    get_col_line_div(clid){
        var html = `<div class="col-line" id="${clid}"></div>`
        return html
    }

    get_type(){
        return "unit"
    }

    get_json(){
        var json ={
            country: this.country,
            kind: this.kind,
            name: this.name,
        }
        
        if(this.start_time>0){
            json.start_time = this.start_time
        }

        return json
    }

}


class LineData {
    constructor(kind, duration, unit = null) {
        // kind : success, fail, move, unused
        this.kind = kind;
        // duration: int , the second spent
        this.duration = duration;
        this.unit = unit
    }

    set_k_d(kind, duration){
        this.kind = kind;
        this.duration = duration;
    }

    set_unit(country, kind, name){
        if(country!= null && kind!= null &&  name!= null){
            this.unit = new UnitData(country, kind, name)
        }else{
            this.unit = null
        }
    }

    get_inner_html(){
        var html = ""
        if(this.unit){
            html += `<div class="cell-node medium-size-cell">${this.unit.get_img()}</div>`
        }else{
            html += `<div class="medium-size-cell"></div>`
        }
        var line_kind = this.kind + "-line"
        html += `<div class="line ${line_kind}"></div><div class="line-dot ${line_kind}"></div>`
        html += `<div class="duration-time ${line_kind}-text">${this.duration}</div>`
        return html
    }

    get_div(nid){
        var html = `<div class="basic-node line-node" id="${nid}">`
        html += this.get_inner_html()
        html += '</div>'

        return html
    }

    get_type(){
        return "line"
    }

    get_json(){
        if(this.unit){
            return {
                kind: this.kind,
                duration: this.duration,
                unit: this.unit.get_json()
            }
        }else{
            return {
                kind: this.kind,
                duration: this.duration,
            }
        }
    }
}


class DataNode {
    constructor(nr, nc, ndata) {
        this.r = nr;
        this.c = nc;
        this.data = ndata;

        this.row_prev = null;  // the parent node in previous row
        this.prev = null;  // The previous node of the current row
        this.row_next = null;  // the child node in next row
        this.next = null;  // The next node of the current row

        this.left = 0;
        this.top = 0;
        this.width = 0;
        this.height = 0;
    }

    get_duration_length() {
        return this.data.duration * SIZE.second
    }

    get_nid() {
        return 'r' + this.r + 'c' + this.c
    }

    get_clid(){
        return `c-${this.c}-fr-${this.r}`
    }

    get_html() {
        var nid = this.get_nid()
        if(this.row_prev && this.data.get_type() == "unit"){
            return this.data.get_col_line_div(this.get_clid()) + this.data.get_div(nid);
        }else{
            return this.data.get_div(nid);
        }
    }
    
    refresh_layout() {
        if(this.row_prev == null){
            if(this.prev == null) {
                this.left = BOARD.px + this.data.get_stary_px() 
                this.top = BOARD.py

                if(this.data.get_type() == "unit"){
                    this.width = SIZE.cell;
                    this.height = SIZE.cell;
                }else{
                    this.width = this.get_duration_length()
                    this.height == 0;
                }
            }else {
                this.left = this.prev.left + this.prev.width
                this.top = this.prev.top

                if(this.data.get_type() == "unit"){
                    this.width = SIZE.cell;
                    this.height = SIZE.cell;
                }else{
                    this.width = this.get_duration_length()
                    this.height = SIZE.cell;
                }
            }
        }else{
            this.left = this.row_prev.left + this.row_prev.width - SIZE.cell
            this.top = this.row_prev.top +  SIZE.cell * BOARD.hrate * (this.r - this.row_prev.r);

            this.width = SIZE.cell;
            this.height = SIZE.cell;
        }
    }

    set_css(cell, refresh_t = true){
        if(!cell){
            var cell = $(".main-board").find("#"+this.get_nid())
        }
        cell.css("margin-left", "" + this.left + "px")
        cell.css("margin-top", "" + this.top + "px")

        if(this.width>0){
            cell.css( "width", this.width);
        }

        if(this.height>0){
            cell.css( "height", this.height);
        }

        if(this.row_prev && this.data.get_type() == "unit"){
            var col_line = $("#" + this.get_clid())
            var left = this.left + SIZE.cell - BOARD.CLW / 2
            var top = this.row_prev.top + SIZE.cell / 2
            var height = (this.r - this.row_prev.r) * SIZE.cell * BOARD.hrate;
            col_line.css("margin-left", "" + left + "px")
            col_line.css("margin-top", "" + top + "px")
            col_line.css( "height", height);
        }

        if(refresh_t){
            refresh_timeline()
        }
    }

    refresh_content(){
        if(this.data.get_type() == "unit"){
            var nid = this.get_nid()
            $("#"+nid).html(this.data.get_img())
        }else if(this.data.get_type() == "line"){
            var nid = this.get_nid()
            $("#"+nid).html(this.data.get_inner_html())
        }
        
    }

    get_json() {
        var json = this.data.get_json()
        json["type"] = this.data.get_type();
        if(this.row_prev){
            json["row_prev"] = this.row_prev.r
        }

        return json
    }

    get_end_time() {
        if(this.row_prev == null){
            if(this.prev == null) {
                return this.data.start_time
            }else{
                return this.prev.get_end_time() + this.data.duration
            }
        }else{

            return this.row_prev.get_end_time()
        }
    }

    refresh_self_and_children(rkind){
        if(this.row_prev == null){
            if(this.prev == null) {
                return
            }else{
                if(rkind == "remove"){
                    var old_nid = this.get_nid()
                    this.r = this.prev.r
                    this.c -= 1

                    var new_nid = this.get_nid()
                    $("#"+old_nid).attr({"id": new_nid})
                }

                this.refresh_layout()
                if(this.next){
                    this.next.refresh_self_and_children(rkind)
                }
                if(this.row_next){
                    this.row_next.refresh_self_and_children(rkind)
                }

                if(rkind == "add"){
                    var old_nid = this.get_nid()
                    this.r = this.prev.r
                    this.c += 1

                    var new_nid = this.get_nid()
                    $("#"+old_nid).attr({"id": new_nid})
                }

                this.set_css(null, false)

            }
        }else{
            //  the change of r is made when the data changed

            if(rkind == "remove"){
                var old_nid = this.get_nid()
                var old_clid = this.get_clid()
                this.c -= 1

                var new_nid = this.get_nid()
                var new_clid = this.get_clid()
                $("#"+old_nid).attr({"id": new_nid})
                $("#"+old_clid).attr({"id": new_clid})
            }

            this.refresh_layout()
            if(this.next){
                this.next.refresh_self_and_children(rkind)
            }

            if(rkind == "add"){
                var old_nid = this.get_nid()
                var old_clid = this.get_clid()
                this.c += 1

                var new_nid = this.get_nid()
                var new_clid = this.get_clid()
                $("#"+old_nid).attr({"id": new_nid})
                $("#"+old_clid).attr({"id": new_clid})
            }

            TIME_DATA[this.r] = NODE_DATA.data[this.r][NODE_DATA.data[this.r].length-1].get_end_time()
            this.set_css(null, false)
        }
    }
}
