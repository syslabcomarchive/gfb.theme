$(function() {
    $("#breadcrumbs-you-are-here").click(function() {
        $("#hidden-path-bar").toggleClass("hide-path-bar");
        $("#portal-breadcrumbs").toggleClass("portal-breadcrumbs-highlighted");
    });
});
