// append this to board view in 'board_lists' class
let lists = $('.board_lists');
$.each(lists, function(i, elem){
    let listId = $(elem).data('id');
    $.ajax({
        url: `/list/${listId}/cards/`,
        method: 'get',
        success: function(res) {
            $(elem).append(res);
        }
    })
});