<script type="text/javascript">
    $(function(){
        // Attach the dynatree widget to an existing <div id="tree"> element
        // and pass the tree options as an argument to the dynatree() function:
        $("#tree_%(fieldName)s").dynatree({
            checkbox: true,
            children: [
                {title: "%(voctitle)s", hideCheckbox: true, expand: %(root_expanded)s, children: [
%(subtree)s
                    ]
                }
            ]
        });
        // On submitting create hidden inputs for each selected item
        $("#searchform").submit(function(){
            selected = $("#tree_%(fieldName)s").dynatree("getSelectedNodes")
            for (var i = 0; i < selected.length; i++) {
                input = document.createElement('input')
                input.type = "hidden"
                input.name = "%(fieldName)s:list"
                input.value = selected[i].data.key
                $('.column2b').find('.search_index').after(input)
            }
        });

    });
</script>
