// append this to board view in 'board_lists' class
var lists = $('.board_lists');
$.each(lists, function(i, elem){
    var listId = $(elem).data('id');
    $.ajax({
        url: `/list/${listId}/cards/`,
        method: 'get',
        success: function(res) {
            $(elem).append(res);
        }
    })
});