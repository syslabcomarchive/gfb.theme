$(function() {
    var searchInput = $("#searchInput");
    var suggestionArea = $("#suggestion-area");

    searchInput.bind( "paste keyup", function () {
        var term = searchInput.val();

        $.getJSON("suggest-terms?term="+term, function( data ) {
            suggestionArea.empty();

            /* Sometimes we get back a list of strings, instead of
               objects with useful values, just ignore them */
            if (data.length > 0 && data[0].constructor == Object) {
                suggestionArea.append("<div id='suggestions' class='livesearchContainer'/>");
                var suggestions = $('#suggestions');

                $(data).each( function (index, value) {
                    if ( value.constructor == Object ) {
                        suggestions.append("<p>"+value.value.word+"</p>");
                    };
                });

                suggestions.find("p").click(function() {
                    searchInput.val($(this).text());
                    suggestionArea.empty();
                });
            };
        });
    });

    searchInput.blur(function() {
        // Allow time for a click event to be fired from the suggestion-area
        setTimeout("$('#suggestion-area').empty()", 200); 
    });
});
