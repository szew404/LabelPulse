$(document).ready(function () {
    $('.send-button').off('click').on('click', function (event) {
        event.preventDefault();

        var url = $(this).data('url');

        $.ajax({
            url: url,
            type: 'GET',
            success: function (response) {
                alert('Test sent successfully.');
            },
            error: function () {
                alert('There was an error sending the test email.');
            }
        });
    });
});
