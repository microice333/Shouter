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
}

$().ready(function() {
  $('.accept-btn').click(function() {
      if (!($(this).hasClass('disabled'))) {
          $.post('/ajax/accept/',
              {
                'invited': $(this).attr('id').substring(7),
                'csrfmiddlewaretoken': getCookie('csrftoken'),
              },
              function(res) {
                alert(res);
              }
          );
          $(this).addClass("disabled");
          $(this).text("Accepted");
        }
  });
});
