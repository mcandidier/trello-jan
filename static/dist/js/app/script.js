// append this to board view in 'board_lists' class
let lists = $('.list_objects');
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


// menu
function openNav() {
  setTimeout(function(){
    document.getElementById("archive-title-board").style.display = "contents";
    document.getElementById("archive-title-list").style.display = "contents";
    document.getElementById("archive-title-card").style.display = "contents";
  }, 300);
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("mySidenav").style.zIndex = 2;
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("archive-title-board").style.display = "none";
  document.getElementById("archive-title-list").style.display = "none";
  document.getElementById("archive-title-card").style.display = "none";
}