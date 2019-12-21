// sortable drag and drop
$( function() {
$( "#sortable" ).sortable();
$( "#sortable" ).disableSelection();
} );

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

// ajax card data 
$(document).on('submit', '#post-form',function(e){
e.preventDefault();
$.ajax({
    type:'POST',
    url:'',
    data:{
        title:$('#title').val(),
        description:$('#description').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
    },
    success:function(json){
        document.getElementById("post-form").reset();
        $(".posts").prepend('<div class="col-md-6">'+
            '<div class="row no-gutters border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative">' +
                '<div class="col p-4 d-flex flex-column position-static">' +
                    '<h3 class="mb-0">' + json.title + '</h3>' +
                    '<p class="mb-auto">' + json.description + '</p>' +
                '</div>' +
            '</div>' +
        '</div>' 
        )
    },
    error : function(xhr,errmsg,err) {
    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
}
});
});

// // 
// $(document).ready(function() {
//   // SideNav Button Initialization
//   $(".button-collapse").sideNav({
//     slim: true
//   });
//   // SideNav Scrollbar Initialization
//   var sideNavScrollbar = document.querySelector('.custom-scrollbar');
//   var ps = new PerfectScrollbar(sideNavScrollbar);
// })




// adfsdfsdf
$('.test').sortable({
connectWith: '.test',
update: function(event, ui) {
    var changedList = this.id;
    var order = $(this).sortable('toArray');
    var positions = order.join(';');

    console.log({
    id: changedList,
    positions: positions
    });
}
});
$('.tests').sortable({
connectWith: '.tests',
update: function(event, ui) {
    var changedList = this.id;
    var order = $(this).sortable('toArray');
    var positions = order.join(';');

    console.log({
    id: changedList,
    positions: positions
    });
}
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