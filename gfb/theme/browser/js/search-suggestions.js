$(function() {
    var searchInput = $(".LSBox input[name='SearchableText']");
    $(searchInput).attr("autocomplete", "off");

    searchInput.bind( "paste keyup", function ( event ) {
        var term = event.target.value;

        $.getJSON("suggest-terms?term="+term, function( data ) {
            $("#suggestion-area").remove();
            $(event.target).parent().append("<div id='suggestion-area'/>");

            /* Sometimes we get back a list of strings, instead of
               objects with useful values, just ignore them */
            if (data.length > 0 && data[0].constructor == Object) {
                    $("#suggestion-area")
                    .append("<ul id='suggestions' class='livesearchContainer'/>");
                var suggestions = $('#suggestions');

                $(data).each( function (index, value) {
                    if ( value.constructor == Object ) {
                        suggestions.append("<li>"+value.value+"</li>");
                    };
                });

                suggestions.find("li").click(function() {
                    $(event.target).val($(this).text());
                    $("#suggestion-area").remove();
                });
            };
        });
    });

    searchInput.blur(function() {
        // Allow time for a click event to be fired from the suggestion-area
        setTimeout("$('#suggestion-area').remove()", 200);
    });
});
