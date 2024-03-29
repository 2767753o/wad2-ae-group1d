// https://code.jquery.com/jquery-3.3.1.min.js

$(document).ready(function () {

    $('button').click(function () {
        if ($(this).hasClass("like_button")) {
            var postIdVar;
            postIdVar = $(this).attr("data-postid");

            var commentIdVar;
            commentIdVar = $(this).attr("data-commentid");

            // either comment or post like, cant be both
            if (commentIdVar !== undefined && commentIdVar !== false) {
                var id = commentIdVar;
                var type = "comment"
                var url = "/blink/like_comment/";
                var context_dict = {"comment_id": commentIdVar};
            } else {
                var id = postIdVar;
                var type = "post"
                var url = "/blink/like_post/";
                var context_dict = {"post_id": postIdVar};
            }

            $.get(
                url,
                context_dict,
                function (data) {
                    var likeCountData = data.substring(2, );
                    // pluralisation
                    if (data[1] == "T") {
                        likeCountData += " likes";
                    } else {
                        likeCountData += " like";
                    }

                    // like count
                    $("#like_count_" + id + "_" + type).html(likeCountData);
                    if (data[0] == "F") {
                        var imageType = "likeEmpty";
                    } else {
                        var imageType = "likeFilled";
                    }
                    $("#like_button_" + id + "_" + type).children('img').attr("src", "/static/images/icons/" + imageType + ".svg");
                }
            )
        }

        if ($(this).hasClass("delete_button")) {
            var postIdVar;
            postIdVar = $(this).attr("data-postid");

            $.get(
                '/blink/delete_post/',
                { 'post_id': postIdVar },
                function (data) {
                    window.location.replace(data);
                }
            )
        }
    });

    $('#search_input').keyup(function () {
        var query;
        query = $(this).val();

        $.get('/blink/search/',
            { 'search_query': query },
            function (data) {
                $('#content').html(data);
            })
    });

    $('div .like_button').click(function(event) {
        event.stopPropagation();
    });

});