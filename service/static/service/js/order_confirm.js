$(document).click(function () {
        $('div.alert').remove();
})
$('button#order_confirm_semi').click(function () {
        $('div#loader').removeClass('no-display');
})

$('button#order_confirm_semi').click(function () {
        localStorage.setItem('time_left', new Date().getTime())
})

var refresh = setInterval(function () {
        var start_time = localStorage.getItem("time_left");
        var current_time = new Date().getTime();
        var difference = current_time - start_time;
        var seconds = Math.floor((difference % (60 * 1000)) / 1000);
        document.getElementById('timer').innerHTML = 15 - seconds
}, 1000)