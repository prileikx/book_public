$(document).ready(function () {
    $.post('/api/check_admin', {}, function (res) {
        if (res.status[0] == 200) {
        } else {
            window.location.href = '/homepage'
        }
    })
    $("#add_book").click(function () {
        $.post('/library/add_book', {
                bname: $("[name='bname']").val(),
                author: $("[name='author']").val(),
                press: $("[name='press']").val(),
                isbn_code: $("[name='isbn_code']").val(),
                book_class: $("[name='book_class']").val(),
                price: $("[name='price']").val(),
                number: $("[name='number']").val(),
                Issue_date: $("[name='Issue_date']").val(),
                introduce: $("[name='introduce']").val(),
            },
            function (res) {
                if (res.status[0] == 200) {
                    Swal.fire({
                        type: 'success',
                        icon: 'success',
                        title: res.message[0],
                        showConfirmButton: false,
                        timer: 1500
                    })
                $("[name='bname']").val("")
                $("[name='author']").val("")
                $("[name='press']").val("")
                $("[name='isbn_code']").val("")
                $("[name='book_class']").val("")
                $("[name='price']").val("")
                $("[name='number']").val("")
                $("[name='Issue_date']").val("")
                $("[name='introduce']").val("")
                } else {
                    Swal.fire({
                        type: 'error',
                        icon: 'error',
                        title: res.message[0],
                        showConfirmButton: false,
                        timer: 1500
                    })
                }
            })
    })
})