$(document).ready(function () {
    $.post('/library', {
        page: 1
    }, function (res) {
        for (i = 1; i <= res.last_book[0]; i++) {
            bid = res.bid[i - 1] + 1
            $("#img" + i).attr('src', '/static/upload/books/img/' + bid + '.png')
            $("#a" + i).text(res.bname[i - 1])
            $("#a" + i).attr('href', '/library/books/' + bid)
            $("#img" + i).removeClass("hidden")
            $("#a" + i).removeClass("hidden")
        }
        $('.pagination').jqPaginator({
            totalCounts: res.count_book[0],
            pageSize: 10,
            visiblePages: 10,
            currentPage: 1,
            onPageChange: function (num, type) {
                $.post('/library', {
                        page: num
                    }, function (res) {
                        for (i = 1; i <= 10; i++) {
                            $("#img" + i).addClass("hidden")
                            $("#a" + i).addClass("hidden")
                        }
                        for (i = 1; i <= res.last_book[0]; i++) {
                            bid = res.bid[i - 1] + 1
                            $("#img" + i).attr('src', '/static/upload/books/img/' + bid + '.png')
                            $("#a" + i).text(res.bname[i - 1])
                            $("#a" + i).attr('href', '/library/books/' + bid)
                            $("#img" + i).removeClass("hidden")
                            $("#a" + i).removeClass("hidden")
                        }
                    }
                )
            }
        });
    })

    $.post('/api/check_admin', {}, function (res) {
        if (res.status[0] == 200) {
            $('#add_book').removeClass("hidden")
        }
    })
    $('#add_book').click(function () {
        $.post('/api/check_admin', {}, function (res) {
            if (res.status[0] == 200) {
                window.location.href = '/library/add_book'
            } else {
                Swal.fire({
                    type: 'error',
                    icon: 'error',
                    title: '用户权限不足',
                    showConfirmButton: false,
                    timer: 1500
                })
            }
        })
    })
})
