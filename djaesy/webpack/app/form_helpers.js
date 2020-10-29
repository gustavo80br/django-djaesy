;(function() {

    $(document).ready(function() {

        // Hidden fields Div column hidding
        $('.hide-if-hidden:has(> input[type=hidden])').hide();

        // When tracked_object is selected, it overides company, representative and client choices in the Module Form
        // $('#id_tracked_object').on('change', function() {
        //     let tracked_obj_id = $(this).val();
        //     if(tracked_obj_id) {
        //         $.getJSON(`http://localhost:8000/api/v1/trackobj/${tracked_obj_id}`, function(data) {
        //             data = JSON.parse(data);
        //             for(const index in data) {
        //                 $(`#id_${index}`).val(data[index]).trigger("change.select2");
        //             }
        //         });
        //     }
        // });

    });

}.call(this));