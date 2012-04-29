$(function () {
    function shortError (msg) {
        $('#oneline-error span').text(msg);
        $('#oneline-error').show('highlight');
    }

    function onErrorShort (xhr, error, ign) {
        shortError(xhr.responseText);
    }

    function hasFileAPI() {
        var w = window;
        return w.File && w.FileReader && w.FileList && w.Blob
    };

    $('#faq').accordion({
        active      : true,
        animated    : false,
        autoHeight  : false,
        collapsible : true,
    });

    $('div#loading').loading({
        text   : 'Waiting...',
        pulse  : 'ellipsis',
        delay  : 50,
        onAjax : true
    });

    $('#add-key').button({
        icons: { primary: 'icon-key' }
    });

    $('#load-key').button({
        icons: { primary: 'icon-file' }
    });

    $('div#git-identity button').button({
        icons: { primary: 'icon-sync' }
    });

    /* Dropping a key */
    $('div.drop-key button').each( function(index, value) {
        $(value).button({
            icons: { primary: 'icon-delete' }
        });

        $(value).click(function () {
            var parent = this.parentNode;
            var keynum = $(parent).data('machine');

            $.ajax({
                url   : location.pathname + 'drop/' + keynum,
                type  : 'POST',
                data  : {},
                error : onErrorShort,
                success : function (data, error, ign) {
                    $(parent).fadeOut(400, function (){ $(this).remove});
                }
            });
        });
    });

    /* Updating an identity */
    $('div#git-identity button').click(function () {
        var identity = $.trim( $('div#git-identity input').val() );

        $.ajax({
            url   : location.pathname + 'set-identity',
            type  : 'POST',
            data  : {'identity' : identity},
            error : onErrorShort,
        });
    });

    /* Adding a key */
    $('#add-key').click(function () {
        var key = $.trim( $('div.pubkey textarea').val() );

        function onSuccess (data, error, ign) {
            window.location.href = window.location;
        };

        $.ajax({
            url   : location.pathname + 'add',
            type  : 'POST',
            data  : {'key' : key},
            dataType : 'json',
            success : onSuccess,
            error   : onErrorShort,
        });
    });

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
                $('div.pubkey textarea').val(res);
            };
        });
    } else {
        $('#load-key').button('disable');
    }

    /* Default textinput value */
    $('div#git-identity input').focus( function(src) {
        var el = $(this);

        if (el.val() == el[0].title) {
            el.removeClass('text-area-inactive');
            el.val('');
        }
    });
    
    $('div#git-identity input').blur( function() {
        var el = $(this);

        if (el.val() == '') {
            el.addClass('text-area-inactive');
            el.val(el[0].title);
            // @todo: opacity without affecting border
            //$('div#git-identity button').button('disable');
        } else {
            //$('div#git-identity button').button('enable');
        }
    });
    
    $('div#git-identity input').blur();
})
