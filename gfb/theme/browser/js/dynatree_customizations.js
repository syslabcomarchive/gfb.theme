var CustomHiddenForm = Backbone.View.extend({
    initialize: function(){
        _.bindAll(this, "render");
        this.model.bind("change:selected", this.render);
        this.render();
    },
    render: function(){
        if(this.model.get("selected").length){
            var el = this.el;
            var tmpl = this.input_template;
            var name = this.model.get("name");
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
});
