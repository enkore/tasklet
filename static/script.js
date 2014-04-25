$(function() {
    function success(data, status, xhr) {
        window.location.reload();
    }

    function get_text(section) {
        var tasklet = section.text().trim();
        return tasklet.slice(0, tasklet.length-1).trim();
    }

    $("section").dblclick(function () {
        var section = $(this);
        var tasklet = get_text(section);
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
    });

    $("section .delete").click(function () {
        var section = $(this).parent();
        var tasklet = get_text(section);

        $.post("/change/", {
            text: tasklet,
            new: ":rm"
        }, success);
    });

    $(".new input").keyup(function (event) {
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

    $(".tasklets-false").sortable().bind("sortupdate", function (event, item) {
        $.post("/move/", {
            text: get_text($(item.item)),
            pos: $(item.item).index()
        }, success);
    });
});
