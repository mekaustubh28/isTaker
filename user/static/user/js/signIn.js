$(document).ready(function () {
    $('label.customer').click(function () {
        $('div.customer').removeClass('hide')
        $('div.service_boy').addClass('hide')
    })

    $('label.service_boy').click(function () {
        $('div.customer').addClass('hide')
        $('div.service_boy').removeClass('hide')
    })
});