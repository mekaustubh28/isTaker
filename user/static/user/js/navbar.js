$(document).ready(function() {
    // Returns width of browser viewport
    if (screen.width < 501) {
        document.getElementById('after_500').innerHTML = document.getElementById('before_500').innerHTML;
        $('div#before_500').addClass('hidden');
        $('div#after_500').removeClass('hidden');
    } else {
        $('div#before_500').removeClass('hidden');
        $('div#after_500').addClass('hidden');
    }
});