$(document).ready(function() {
    $('.like-btn,.dislike-btn').on('click', function() {
        var action = $(this).data('action');
        var postId = $(this).data('post-id');
        var url = $(this).data('url');
        var csrfToken = '{{ csrf_token }}'; // Get the CSRF token from the template

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                action: action,
                post_id: postId
            },
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(data) {
                // Update the rating display
                $('.rating').text(data.rating + 'рейтинг новости');
                // Toggle the button state
                toggleButtonState($(this), action);
            }
        });

        $.ajax({
        type: 'POST',
        url: '/News/dislike/1/',
        data: {},
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(data) {
            // ...
        }
});
    });
});