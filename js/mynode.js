class UnitData {
    constructor(country, kind, name) {
        this.country = country || ""
        this.kind = kind || ""
        this.name = name || ""
    }
    
    set_all(country, kind, name){
        this.country = country
        this.kind = kind
        this.name = name
    }

    get_img(){
        if(this.country == "" || this.kind == "" || this.name == ""){
            return ""
        }else {
            var img_p = get_img_src(this.country, this.kind, this.name)

            return `<img src="${img_p}" class="unit-img ${kind}-unit" alt="${PATH.wrong_1}"/>`
        }
    }

    get_div(nid){
        var html = '<div class="basic-node cell-node" id="' + nid + '">' + this.get_img() + '</div>'
        return html
    }

    get_type(){
        return "unit"
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

    get_html() {
        var nid = this.get_nid()
        return this.data.get_div(nid);
    }
    
    refresh_layout() {
        if(this.row_prev == null){
            if(this.prev == null) {
                this.left = BOARD.px
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


        }
    }

    set_css(cell){
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
}
