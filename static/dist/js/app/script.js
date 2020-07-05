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

// 
// 
// 

// sortable drag and drop
$( function() {
  $( "#sortable" ).sortable();
  $( ".sortable-list" ).disableSelection('#add-a-list');
  } );
  
  // disable dragable
  
  // card modal
  $('#viewCardModal').on('show.bs.modal', function(event){
      let remoteUrl = $(event.relatedTarget).data('remote')
      let modal = $(this)
      
      $.ajax({
          method: 'GET',
          url: remoteUrl
      }).done(function(response){
          
          modal.find('.modal-body').html(response)
      })
  })
  
  
  $(document).on('submit','#sendComment', function(event){
  event.preventDefault()
  let action = $('#sendComment').attr('action')
  let card_data = $('#sendComment').serialize()
  let comment = $('#sendComment').val();
  let csrf = $('input[name="csrfmiddlewaretoken"]').val();
  
  $.ajax({
      url:action,
      method:'POST',
      data:card_data,
      headers:{
          'X-CSRFToken':csrf
      }
  
  }).done(function(response){
      // console.log(comment);
  })
  })
  
  // leave board ajax
  $(document).on('submit','#leaveBoard', function(event){
      event.preventDefault()
      let action = $('#leaveBoard').attr('action')
      let card_data = $('#leaveBoard').serialize()
      let csrf = $('input[name="csrfmiddlewaretoken"]').val();
      
      $.ajax({
          url: action,
          method: 'GET',
          data:card_data,
          headers:{
              'X-CSRFToken':csrf
          }
      
      }).done(function(response){
          window.location.href = "http://127.0.0.1:8000/";
      })
  })
  
  // dragable scroll
  $("#content").draggable({axis: "x", containment: '.base-content'});
  
  // add event
  $( document.body ).click(function() {
  $( "a.change" ).each(function() {
      if ( "a.change" ){
      $( this ).replaceWith("<input class='input-change'>");
      if ( "a.change" ){
          $( ".input-change" ).focus();
          $( ".input-change" ).focusout(function() {
          $( this ).replaceWith('<a href="#" class="change">link</a>');
          });
      }
      }
  });
  });
  
  // {'a': 'b', 'b': 'b', 'c': 'c'}
  // drag and drop list
  $('.sortable-list').sortable({
  connectWith: '.sortable-list',
  update: function() {
      let changedList = this.id;
      let order = $(this).sortable('toArray');
      let positions = order.join(',');
      
      console.log({
      id: changedList,
      positions
      
      });
      $.ajax({
          url: '',
          method: 'GET',
          data: this.cardId,
          success: function() {
              // console.log({listId, cardId})
          }
      })
  }
  });
  
  // drag and drop cards
  $('.sortable-card').sortable({
      connectWith: '.sortable-card',
      receive: function(event, ui) {
        let dragCardId = ui.item.attr("id");
        let listId = this.id;
    
        $.ajax({
            url: `to/${listId}/get/${dragCardId}`,
            method: 'GET',
            data: this.cardId,
            success: function() {
                console.log(listId);
                console.log({dragCardId});
              alert('to '+ listId);
              alert('from '+ui.sender[0].id); // Where it came from
              alert('drag ID is '+ui.item[0].id); // Which item
            }
          })
      }
    });
  
  // submit without refresh
  function AjaxFormSubmit() {
  $.ajax({
      url : '',
      type : "POST",
      data : {
          title:$('#id_title').val(),
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      }
  }).done(function(returned_data){
      console.log('hmmmm');
  
  });
  }