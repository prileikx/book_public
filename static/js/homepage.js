$(document).ready(function () {
    var html = ""
    $.ajax({
        url: "/api/my_fav",
        type: "post",
        success: function (res) {
            html = "<tr><td style='text-align: center;border-right: 1px solid #c2c2d6;border-bottom: 1px solid #c2c2d6'>书籍名称</td><td style='text-align: center;border-bottom: 1px solid #c2c2d6'>收藏时间</td></tr>"
            console.log(res.book_name)
            var n=res.countb[0]
            var show_more = false
            if(n>11){
                n=11
                show_more = true
            }
            for (i = 0; i < n; i++) {
                if (i % 2 == 0) {
                    html += "<tr style='background-color:#DDDDDD;'>"
                } else {
                    html += "<tr>"
                }
                html+="<td style='text-align: left;width: 415px;border-right: 1px solid #c2c2d6;border-bottom: 1px solid #c2c2d6'><a style='color: #0f0f0f' href='/library/books/"+res.book_bid[i]+"'>"+res.book_name[i]+"</asty></td><td style='text-align: center;border-bottom: 1px solid #c2c2d6'>"+res.book_fav_time[i]+"</td></tr>"
            }
            if(show_more == true){
                html+="<tr><td><a href='/user/fav_book'>[more...]</a></td></tr>"
            }
            $("#my_fav").html(html)
            console.log(html)
        }
    })
})