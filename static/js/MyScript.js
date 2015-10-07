/**
 * Created by kostya on 02.10.2015.
 */

function get_history (chat_id) {
    $.ajax({
        url: '/get_history/' + chat_id,
        type: 'POST',
        success: function (data) {
            $( "#history" ).html(data);
        }
    });
}
function get_members (chat_id) {
    $.ajax({
        url: '/get_members/' + chat_id,
        type: 'POST',
        success: function (data) {
            $( "#members" ).html(data);
        }
    });
}