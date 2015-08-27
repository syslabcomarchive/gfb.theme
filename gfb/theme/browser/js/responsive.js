$(function() {
    if ($(window).width() < 1000) {
      var navTree = $("ul.navTreeLevel0");
      var navTreeHeight = $("ul.navTreeLevel0").height() || 0;
      globalNavHeight = $('#globalnav-group').height();
      totalNavHeight = globalNavHeight + navTreeHeight;
      $("#visual-portal-wrapper").css({"padding-bottom": totalNavHeight + "px"});
      navTree.css({"bottom": globalNavHeight + "px", "visibility": "visible" });
    }
});


(function () {
    jQuery(document).ready( function () {
        jQuery('ul.contentViews li#contentview-submit a').click( function() {
            alert('Wenn Sie diesen Artikel zur Veröffentlichung einreichen, können Sie ihn nicht mehr bearbeiten. Wollen Sie dies trotzdem tun, wählen Sie "eingereichte Veröffentlichung zurückziehen"');
        });
    });

}());
