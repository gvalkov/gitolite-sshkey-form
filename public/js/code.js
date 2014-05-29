// Utility functions
function shortError(msg) {
  $('#oneline-error span').text(msg);
  $('#oneline-error').show();
}

function onErrorShort(xhr, error, ign) {
  shortError(xhr.responseText);
}

function hasFileAPI() {
  return window.File
      && window.FileReader
      && window.FileList
      && window.Blob;
};


// UI elements
$('#add-key').button({disabled: true});
$('#load-key').button();
$('div#git-identity button').button();

$('#faq').accordion({
  active: true,
  animate: false,
  autoHeight: true,
  collapsible: true,
});


// UI actions
/* Load key from file (needs html5 file API) */
if (hasFileAPI()) {
  $('#load-key').click(function () {
    $('#load-key-file').click()
  });

  $('#load-key-file').change(function (e) {
    var f = $('#load-key-file')[0].files[0];
    var r = new FileReader();

    r.readAsText(f, 'UTF-8'); // @todo
    r.onload = function(e) {
      var res= e.target.result;
      var fn = $('#load-key-file')[0].files[0].name;
      $('div.pubkey textarea').val(res).trigger('change');
    };
  });
} else {
  $('#load-key').button('disable');
}

// $('div#loading').loading({
//   text   : 'Waiting...',
//   pulse  : 'ellipsis',
//   delay  : 50,
//   onAjax : true
// });


// /* Dropping a key */
$('div.drop-key button').each( function(index, value) {
  $(value).button({
    icons: { primary: 'icon-delete' }
  });

  $(value).click(function () {
    var parent = this.parentNode;
    var keynum = $(parent).data('machine');

    $.ajax({
      url:  location.pathname + 'drop/' + keynum,
      type: 'POST',
      data: {},
      error: onErrorShort,
      success: function (data, error, ign) {
        $(parent).fadeOut(400, function (){ $(this).remove});
      }
    });
  });
});

// /* Updating an identity */
// $('div#git-identity button').click(function () {
//   var identity = $.trim( $('div#git-identity input').val() );

//   $.ajax({
//     url   : location.pathname + 'set-identity',
//     type  : 'POST',
//     data  : {'identity' : identity},
//     error : onErrorShort,
//   });
// });

/* Adding a key */
$('#add-key').click(function () {
  var key = $.trim( $('div.pubkey textarea').val());

  $.ajax({
    url:  location.pathname + 'add',
    type: 'POST',
    data: {'data': key},
    error: onErrorShort,
    success: function (data, error, ign) {
      location.reload();
    }
  });
});

// Enable the #add-key button only if its input field is not empty
$('div.pubkey textarea').on('keyup change', function () {
  if (this.value.length == 0) {
    $('#add-key').button('disable');
  } else {
    $('#add-key').button('enable');
  }
});

var ta_content = $.trim($('div.pubkey textarea').val());
if (ta_content !== '') {
    $('#add-key').button('enable');
}


// /* Default identity textinput value */
// $('div#git-identity input').focus( function(src) {
//   var el = $(this);

//   if (el.val() == el[0].title) {
//     el.removeClass('text-area-inactive');
//     el.val('');
//   }
// });

// $('div#git-identity input').blur( function() {
//        var el = $(this);

//        if (el.val() == '') {
//          el.addClass('text-area-inactive');
//          el.val(el[0].title);
//          // @todo: opacity without affecting border
//          //$('div#git-identity button').button('disable');
//        } else {
//          //$('div#git-identity button').button('enable');
//        }
//      });

// $('div#git-identity input').blur();
