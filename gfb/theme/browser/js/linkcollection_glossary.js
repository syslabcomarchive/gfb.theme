$(function() {
    $("li.linkList a").each( function (index, value) {
      $.getScript(value.href+"/ploneglossary_definitions.js");
    });
});
