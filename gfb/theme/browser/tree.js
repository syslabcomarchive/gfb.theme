<script type="text/javascript">
    jQuery(function(){
        // Attach the dynatree widget to an existing <div id="tree"> element
        // and pass the tree options as an argument to the dynatree() function:
        jQuery("#tree_%(fieldName)s").dynatree({
            checkbox: true,
            children: [
                {title: "%(voctitle)s", hideCheckbox: true, expand: %(root_expanded)s, children: [
%(subtree)s
                    ]
                }
            ]
        });
        // On submitting create hidden inputs for each selected item
        jQuery("#searchform").submit(function(){
            selected = $("#tree_%(fieldName)s").dynatree("getSelectedNodes")
            if (jQuery("#tree_%(fieldName)s").parent().attr('class').search('disabled')<0)
            {
                for (var i = 0; i < selected.length; i++) {
                    input = document.createElement('input')
                    input.type = "hidden"
                    input.name = "%(fieldName)s:list"
                    input.value = selected[i].data.key
                    $('.search_filters').after(input)
                }
            }
        });

    });
</script>
