$(document).ready(function () {

    $('button').click(function () {
        if ($(this).hasClass("like_button")) {
            var postIdVar;
            postIdVar = $(this).attr("data-postid");

            var commentIdVar;
            commentIdVar = $(this).attr("data-commentid");

            // either comment or post like
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
                    var likeCountData = data[0];
                    if (data[2] == "T") {
                        likeCountData += " likes.";
                    } else {
                        likeCountData += " like.";
                    }
                    
                    $("#like_count_" + id + "_" + type).html(likeCountData);
                    if (data[1] == "F") {
                        $("#like_button_" + id + "_" + type).children('img').attr("src", "/static/images/icons/likeEmpty.svg");
                    } else {
                        $("#like_button_" + id + "_" + type).children('img').attr("src", "/static/images/icons/likeFilled.svg");
                    }
                }
            )
        }
    });

});