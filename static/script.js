$(function() {
    function success(data, status, xhr) {
        window.location.reload();
    }

    function enter_edit_mode() {
        var section = $(this);
        var tasklet = section.text().trim();
        // Remove the X from .delete button
        tasklet = tasklet.slice(0, tasklet.length-1).trim();
        var input_field = $("<input type='text'>").val(tasklet);

        section.empty();
        section.off("dblclick");
        section.append(input_field);
        document.getSelection().removeAllRanges();

        input_field.keyup(function(event) {
            if(event.keyCode == 13) { // enter
                $.post("/change/", {
                    text: tasklet,
                    new: input_field.val()
                }, success);
            }
        });
    }

    function delete_tasklet() {
        var section = $(this).parent();
        var tasklet = section.text().trim();
        // Remove the X from .delete button
        tasklet = tasklet.slice(0, tasklet.length-1).trim();

        $.post("/change/", {
            text: tasklet,
            new: ":rm"
        }, success);
    }

    $("section").dblclick(enter_edit_mode);

    $("section .delete").click(delete_tasklet);

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
