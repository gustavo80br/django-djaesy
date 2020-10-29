;(function() {
    $(document).ready(function() {

        let selects = $('select:required');
        selects.each(function(index, value){
            let el = $(value);
            let children = el.children().length;
            if(children === 1) {
                el.prop("selectedIndex", 0);
                if(el.select2) {
                    el.trigger('change');
                }
            } else if(children === 2) {
                if(el.children()[0].text === '---------') {
                    el.prop("selectedIndex", 1);
                    if(el.select2) {
                        el.trigger('change');
                    }
                }
            }
        });
    });
}.call(this));