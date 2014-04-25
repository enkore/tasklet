$(function() {
    function success(data, status, xhr) {
        window.location.reload();
    }

    function enter_edit_mode() {
        var section = $(this);
        var tasklet = section.text().trim();
        var input_field = $("<input type='text'>").attr("value", tasklet);

        section.empty();
        section.off("dblclick");
        section.append(input_field);

        input_field.keyup(function(event) {
            if(event.keyCode == 13) { // enter
                $.post("/change/", {
                    text: tasklet,
                    new: input_field.val()
                }, success);
            }
        });

    }

    $("section").dblclick(enter_edit_mode);

    $(".new input").keyup(function(event) {
        var text = $(this).val();
        if(event.keyCode == 13) { // enter
            $.post("/add/", {
                text: text
            }, success);
        } else {
            text = text.toLocaleLowerCase();
            $("section:not(.new)").each(function() {
                $(this).attr("style", "display: " + ($(this).text().toLocaleLowerCase().indexOf(text) == -1 ? "none":"block"));
            });
        }
    });
});
