jQuery(document).ready(function() {

    jQuery("#highlights-tabs").tabs(
        "#highlights-content > div",
        {
            // Truncate the content to the size of the container on activation
            onClick : function (event, tabIndex) { 
                var tab = jQuery("#highlights-"+(tabIndex+1)+ " .highlight");
                // Only truncate once
               if ( tab.data("dotdotdot") != true ) {
                    tab.dotdotdot();
                }
            }
        }
    );

    var highlights = jQuery("#homepage-tabs-2-link");
    highlights.live("click", function () {
        var tab = jQuery("#highlights-1 .highlight");
        tab.dotdotdot();
    })
    

});
