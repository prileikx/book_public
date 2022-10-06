function change_page(page) {
    $.post("/library",
        {
            page: page
        },
        function (res) {
            if (res.status == 200) {
                for (i = 1; i <= 10; i++) {
                    bid = res.bid[i - 1] + 1
                    $("#img" + i).attr('src', '/static/upload/' + bid + '.png')
                    $("#a" + i).text(res.bname[i - 1])
                    $("#a" + i).attr('href', '/library/books/' + bid)
                }
                page = res.page[0]
                if ($("#page1").attr('class') == "active") {
                    $("#page1").removeAttr('class')
                }
                if ($("#page2").attr('class') == "active") {
                    $("#page2").removeAttr('class')
                }
                if ($("#page3").attr('class') == "active") {
                    $("#page3").removeAttr('class')
                }
                if ($("#page4").attr('class') == "active") {
                    $("#page4").removeAttr('class')
                }
                if ($("#page5").attr('class') == "active") {
                    $("#page5").removeAttr('class')
                }
                if (page == 1) {
                    page = page - 1
                }
                console.log(page <= res.pageall - 5)
                if (page >= 2 && page <= res.pageall - 5) {
                    page = page - 2
                } else if (page == res.pageall - 4) {
                    page = page - 2
                } else if (page == res.pageall - 3) {
                    page = page - 3
                } else if (page == res.pageall - 2) {
                    page = page - 4
                }


                for (i = 1; i <= 5; i++) {
                    page = page + 1
                    $("#page_a" + i).text(page)
                }
                page = res.page[0] + 1
                if (page == 1) {
                    $('#page1').addClass("active")
                } else if (page == 2) {
                    $('#page2').addClass("active")
                } else if (page == res.pageall[0] - 2) {
                    $('#page4').addClass("active")
                } else if (page == res.pageall[0] - 1) {
                    $('#page5').addClass("active")
                } else {
                    $('#page3').addClass("active")
                }
            } else {
                alert("加载失败")
            }
        })
}

$(document).ready(function () {
    $.post("/library",
        {
            page: 1
        },
        function (res) {
            if (res.status == 200) {
                for (i = 1; i <= 10; i++) {
                    bid = res.bid[i - 1] + 1
                    $("#img" + i).attr('src', '/static/upload/' + bid + '.png')
                    $("#a" + i).text(res.bname[i - 1])
                    $("#a" + i).attr('href', '/library/books/' + bid)
                }
                page = res.page[0]
                if (page == 1) {
                    page = page - 1
                }
                if (page >= 2) {
                    page = page - 2
                }
                if (page == res.pageall - 2) {
                    page = page - 4
                }
                if (page == res.pageall - 1) {
                    page = page - 5
                }
                for (i = 1; i <= 5; i++) {
                    page = page + 1
                    $("#page_a" + i).text(page)
                }
                page = res.page[0] + 1
                if (page == 1) {
                    $('#page1').addClass("active")
                } else if (page == 2) {
                    $('#page2').addClass("active")
                } else if (page == res.pageall[0] - 2) {
                    $('#page4').addClass("active")
                } else if (page == res.pageall[0] - 1) {
                    $('#page5').addClass("active")
                } else {
                    $('#page3').addClass("active")
                }
            } else {
                alert("加载失败")
            }
        })
    $("#page1").click(function () {
        change_page($("#page1").text())
    })
    $("#page2").click(function () {
        change_page($("#page2").text())
    })
    $("#page3").click(function () {
        change_page($("#page3").text())
    })
    $("#page4").click(function () {
        change_page($("#page4").text())
    })
    $("#page5").click(function () {
        change_page($("#page5").text())
    })
    $("#jump_btn").click(function () {
        if ($("[name='jump_input']").val() == "") {
            return "false"
        } else {
            change_page($("[name='jump_input']").val())
        }

    })
})
