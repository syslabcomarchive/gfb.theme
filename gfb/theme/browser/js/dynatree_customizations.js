var CustomHiddenForm = Backbone.View.extend({
    initialize: function(){
        _.bindAll(this, "render");
        this.model.bind("change:selected", this.render);
        this.render();
    },
    render: function(){
        var name = this.model.get("name");
        // either at least one item is still selected, or one previously selected item remains
        if(this.model.get("selected").length ||jq('input[name="' + name +':list"]').length){
            var el = this.el;
            var tmpl = this.input_template;
            el.empty();
            _.each(this.model.get("selected"), function(elem){
                jq(tmpl({name: name,
                         value: elem})).appendTo(el);
            });
        }
    },
    input_template: _.template('<input type="hidden" name="{{ name }}:list" value="{{ value }}" />')
});


jq(document).ready(function(){
    jq(".dynatree-custom").each(function() {
        var jqthis = jq(this);
        var datamodel = jqthis.data('collective.dynatree');
        var custom_hidden_form = new CustomHiddenForm({el: jqthis.find(".customhiddeninput"),
                                                       model: datamodel});
    });
    jq(".closed_widget").hide();

    function runEffect(fname) {
        // get effect type from
        var selectedEffect = "blind";
        // most effect types need no options passed by default
        var options = {};
        jq( "#" + fname ).toggle( selectedEffect, options, 500 );
    };

    // set effect from select menu value
    jq( ".toggleButton" ).click(function() {
        var jqthis = jq(this);
        jqthis.toggleClass('opened');
        jqthis.next().toggleClass('opened');
        var fname = jqthis[0].id.replace('button_', 'widget_');
        runEffect(fname);
        return false;
    });

javascript: if (!String.prototype.trim) {
    String.prototype.trim = function () {
        return this.replace(/^\s+|\s+$/g, '');
    };
}


function dynatree_to_input(input, dynatree) {
    var model = dynatree.data("collective.dynatree");
    model.bind("change:selected", function (model) {
        var old_keys = model.previous('selected'),
            new_keys = model.changedAttributes().selected,
            new_input = input.val().trim();
        _.each(_.difference(old_keys, new_keys), function (to_remove) {
            var to_remove_title = model.getDataFor(to_remove).title;
            new_input = new_input.replace(to_remove_title, "");
        });
        _.each(_.difference(new_keys, old_keys), function (to_add) {
            var to_add_title = model.getDataFor(to_add).title;
            new_input += " " + to_add_title;
        });
        input.val(new_input.trim());
        jq(dynatree).find('.close').click();
    });
}

var custom_popup = jq(".dynatree-custom-popup");
if (custom_popup.size() > 0) {
    dynatree_to_input(jq("#form-widgets-query"), jq(custom_popup[0]));
}
});
