// $().ready(function() {
    // let serializedUserData = localStorage.getItem('chat-user');
    // if (serializedUserData == null) {
    //     var userData = {};
    // } else {
    //     var userData = JSON.parse(serializedUserData);
    // }
    // setUser(userData);
    //
    // $('#login').click(function() {
    //     let userData = {
    //         username: $('#username').val(),
    //         password: $('#password').val()
    //     };
    //     $.post('/ajax/chat_login/', userData, function() {
    //         setUser(userData);
    //     }).fail(function() {
    //         alert('Incorrect username or password. Try again.');
    //     });
    // });
    //
    // getAndDisplayChat();
    //
    // setInterval(getAndDisplayChat, 3000);
//
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

    $('.like-btn').click(function() {
        if ($(this).hasClass('like')) {
            $.post('/ajax/like/',
                {
                  'message_id': $(this).attr('id').substring(8),
                  'csrfmiddlewaretoken': getCookie('csrftoken'),
                },
                function(res) {
                  alert(res);
                }
            );
            $(this).removeClass("like btn-outline-primary").addClass("unlike btn-primary");
            $(this).text("Unlike");
            $(this).parent().children(".like-nb").text($(this).parent().children(".like-nb").text() +1);
        } else {
          $.post('/ajax/unlike/',
              {
                'message_id': $(this).attr('id').substring(8),
                'csrfmiddlewaretoken': getCookie('csrftoken'),
              },
              function(res) {
                alert(res);
              }
          );
          $(this).removeClass("unlike btn-primary").addClass("like btn-outline-primary");
          $(this).text("Like");
          $(this).parent().children(".like-nb").text($(this).parent().children(".like-nb").text() -1);
        }
    });

    $('.invitation-btn').click(function() {
        if (!($(this).hasClass('disabled'))) {
            $.post('/ajax/invite/',
                {
                  'invited': $(this).attr('id').substring(11),
                  'csrfmiddlewaretoken': getCookie('csrftoken'),
                },
                function(res) {
                  alert("Send invitation");
                }
            );
            var selector = '#' + $(this).attr('id') + '.invitation-btn';
            $(selector).addClass("disabled");
            $(selector).text("Invited");
          }
    });
});
