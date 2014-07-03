$(function() {
    if ($(window).width() < 1000) {
      var navTree = $("ul.navTreeLevel0");
      var navTreeHeight = $("ul.navTreeLevel0").height() || 0;
      var globalnavTop = $('#globalnav-group').position()["top"];
      globalNavHeight = $('#globalnav-group').height();
      totalNavHeight = globalNavHeight + navTreeHeight;
      $("#visual-portal-wrapper").css({"padding-bottom": totalNavHeight + "px"});
      navTree.css({"bottom": globalNavHeight + "px", "visibility": "visible" });
    }
});
