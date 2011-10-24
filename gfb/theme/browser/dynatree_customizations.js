var CustomHiddenForm = Backbone.View.extend({
    initialize: function(){
        _.bindAll(this, "render");
        this.model.bind("change:selected", this.render);
    },
    render: function(){
        var val = "";
        if(this.model.get("selected").length){
            debugger;
            _.each(this.model.get("selected"), function(elem){
                jq('<input type="hidden" name="%s" value="%s">').insertAfter(this.el);
            });
        }
        this.el.val(val);
    }
});

jq(document).ready(function(){
    jq(".dynatree-custom").each(function() {
        var jqthis = jq(this);
        var datamodel = jqthis.data('collective.dynatree');
        var custom_hidden_form = new CustomHiddenForm({el: jqthis.find(".customhiddeninput"),
                                                       model: datamodel});
    });
});
