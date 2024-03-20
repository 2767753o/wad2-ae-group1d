$(document).ready(function () {

    $('button').click(function () {
        if ($(this).hasClass("like_button")) {
            var postIdVar;
            postIdVar = $(this).attr("data-postid");

            $.get(
                "/blink/like_post/",
                {"post_id": postIdVar},
                function (data) {
                    $("#like_count_" + postIdVar).html(data[0]);
                    if (data[1] == "F") {
                        $("#like_button_" + postIdVar).children('img').attr("src", "/static/images/icons/likeEmpty.svg");
                    } else {
                        $("#like_button_" + postIdVar).children('img').attr("src", "/static/images/icons/likeFilled.svg");
                    }
                }
            )
        }
    });

});