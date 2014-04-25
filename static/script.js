$(function() {
    function enter_edit_mode() {
        var section = $(this);
        var tasklet = section.text().trim();
        var input_field = $("<input type='text'>").attr("value", tasklet);

        section.empty();
        section.off("dblclick");
        section.append(input_field);

        input_field.keyup(function(event) {
            if(event.keyCode == 13) { // enter
                window.location.pathname = "/change/" + encodeURIComponent(tasklet) + "/" + encodeURIComponent(input_field.val());
            }
        });

    }

    $("section").dblclick(enter_edit_mode);

    $(".new input").keyup(function(event) {
        if(event.keyCode == 13) { // enter
            window.location.pathname = "/add/" + encodeURIComponent($(this).val());
        }
    });
});
