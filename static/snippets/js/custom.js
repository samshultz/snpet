$(function(){
    $('button[name=copy]').click(function(event) {
        var att = $(this).parent();
        var name = $(this).attr('name');
        console.log(name);
        $(this).attr({'data-clipboard-target':att,
            'data-clipboard-action': name,
        });
        var clipboard = new Clipboard(name);
        console.log(clipboard);
    });
    
});
