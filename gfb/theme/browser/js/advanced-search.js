$(function() {
    $("input#radio_category_common").click(function() {
        $(".search_deactivatable").addClass("disabled");
    });
    $("input#radio_category_special").click(function() {
        $(".search_deactivatable").removeClass("disabled");
    });
});
