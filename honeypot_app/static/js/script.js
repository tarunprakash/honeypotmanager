const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

function refreshPage() {
    location.reload();

    return false;
}

function removeHoneypot() { // remove honeypot 
    $.ajax({
        url: './remove',
        type: 'POST',
        data: {
            'honeypotType': $('#deleteType').text(),
            'honeypotIP': $('#deleteIP').text(),
            'csrfmiddlewaretoken': csrfToken
        },
        success: data => {
            refreshPage()
        }
    })
}

$("#createForm").submit(e => { // create honeypot
    e.preventDefault();
    $.ajax({
        url: $("#createForm").attr("action"),
        type: 'POST',
        data: $("#createForm").serialize(),
        success: data => {
            refreshPage()
        }
    })
});

$('#deleteConfirmModal').on('show.bs.modal', function (event) { // show delete confirmation modal
    var button = $(event.relatedTarget)
    var honeypotType = button.data('type')
    var honeypotIP = button.data('ip') 
    
    var modal = $(this)
    modal.find('#deleteType').text(honeypotType)
    modal.find('#deleteIP').text(honeypotIP)
});


let socket = new WebSocket("ws://localhost:8000/log");

socket.onmessage = function(event) {
    refreshPage();
};
