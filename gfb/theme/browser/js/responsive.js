$(function() {
if ($(window).width() < 1000) {
    var navTreeHeight = $("ul.navTreeLevel0").height();
    if (! navTreeHeight) { navTreeHeight = 0 };
    var footerActions = $("ul#portal-siteactions")[1];
    $(footerActions).css({"padding-bottom": navTreeHeight + "px"});
}
});
