// $(document).ready(function () {
//
//
//
//     $('#search').click(function () {
//         $.ajax({
//             url: '/library/search',
//             type: 'get',
//             data: {
//                 page: 1,
//                 search_text: $('#search_text').val(),
//                 choose:$("[name='choose']:checked").val()
//             },
//             success: function (res) {
//                 for (i = 1; i <= res.last_book[0]; i++) {
//                     bid = res.bid[i - 1] + 1
//                     $("#img" + i).attr('src', '/static/upload/books/img/' + bid + '.png')
//                     $("#a" + i).text(res.bname[i - 1])
//                     $("#a" + i).attr('href', '/library/books/' + bid)
//                     $("#img" + i).removeClass("hidden")
//                     $("#a" + i).removeClass("hidden")
//                 }
//                 $('.pagination').jqPaginator({
//                     totalCounts: res.count_book[0],
//                     pageSize: 10,
//                     visiblePages: 10,
//                     currentPage: 1,
//                     onPageChange: function (num, type) {
//                         $.post('/library', {
//                                 page: num
//                             }, function (res) {
//                                 for (i = 1; i <= 10; i++) {
//                                     $("#img" + i).addClass("hidden")
//                                     $("#a" + i).addClass("hidden")
//                                 }
//                                 for (i = 1; i <= res.last_book[0]; i++) {
//                                     bid = res.bid[i - 1] + 1
//                                     $("#img" + i).attr('src', '/static/upload/books/img/' + bid + '.png')
//                                     $("#a" + i).text(res.bname[i - 1])
//                                     $("#a" + i).attr('href', '/library/books/' + bid)
//                                     $("#img" + i).removeClass("hidden")
//                                     $("#a" + i).removeClass("hidden")
//                                 }
//                             }
//                         )
//                     }
//                 })
//             }
//         })
//     })
// })
