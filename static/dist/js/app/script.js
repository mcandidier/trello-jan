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

$('#viewCardModal').on('show.bs.modal', function(event){
    console.log("SULOD")
    let remoteUrl = $(event.relatedTarget).data('remote')
    let modal = $(this)
    
    $.ajax({
        method: 'GET',
        url: remoteUrl
    }).done(function(response){
        
        modal.find('.modal-body').html(response)
    })
})


$(document).on('submit','#viewCardModal', function(event){
event.preventDefault()
let action = $('#edit-card-form').attr('action')
let card_data = $('#edit-card-form').serialize()
let csrf = $('input[name="csrfmiddlewaretoken"]').val();

console.log(action,"url")

$.ajax({
    url: action,
    method: 'POST',
    data: card_data,
    headers:{
        'X-CSRFToken':csrf
    }

}).done(function(response){
    this.clo
})
})

// dev

$("form").submit(function(e){
    $.post('', $(this).serialize());
    console.log('ssssss');
    $('div').append('dsd');
    e.preventDefault();
});

function showUser(str) {
    if (str=="") {
      document.getElementById("txtHint").innerHTML="";
      return;
    }
    if (window.XMLHttpRequest) {
      // code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
    } else { // code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function() {
      if (this.readyState==4 && this.status==200) {
        document.getElementById("txtHint").innerHTML=this.responseText;
      }
    }
    xmlhttp.open("GET",+str,true);
    xmlhttp.send();
  }