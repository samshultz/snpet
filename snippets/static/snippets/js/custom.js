$(document).ready(function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
});
$(document).ready(function () {
  $("a#upvote, a#downvote").click(function(e){
      e.preventDefault();
      var curr_action = $(this).data("action");
      var callout = $(this).parent().parent()[0];

      function upvote_downvote (attr) {
          // increment the upvote or downvote element value
          var value = parseInt($(callout).find('span[title='+ attr + ']').first().text());
          value += 1
          $(callout).find('span[title='+ attr +']').first().text(value)
      };

      $.post($(this).attr("js-post-upvote-url"),
      {
          id: $(this).data("id"),
          action: curr_action
      },
      function (data) {
          if (curr_action == 'upvote' && !data['upvoted']) { 
            upvote_downvote("upvotes");
        }

        else if (curr_action == 'downvote' && !data['downvoted']) {
            upvote_downvote("downvotes");
        };
    });
  });

  $('a#bookmark').click(function (e) {
    e.preventDefault();
    $.post($(this).attr("js-post-bookmark-url"),
    {
        id: $(this).data("id"),
        action: $(this).data("action")
    })
})
})