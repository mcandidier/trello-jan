// append this to board view in 'board_lists' class
var lists = $('.board_lists');
$.each(lists, function(i, elem){
    console.log(elem, 'afdsfa');
    console.log($(elem).data('id'));
    var listId = $(elem).data('id');
    $.ajax({
        url: `/list/${listId}/cards/`,
        method: 'get',
        success: function(res) {
            console.log(res, 'data');
            $(elem).append(res);
        }
    })
});