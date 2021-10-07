$(document).ready(function () {
    $('input#search_filter').on('change keyup paste', function () {
        var input, filter, ul, li, a, i, txtValue;
        input = document.getElementById("search_filter")
        filter = input.value;
        // console.log(filter, typeof(filter))
        table = document.getElementById("table_filter")
        tr = document.getElementsByClassName('table_content');
        $('tr.table_content').addClass('hidden');
        for (i = 0; i < tr.length; i++) {
            if (tr[i].innerText.toLowerCase().indexOf(filter.toLowerCase()) != -1) {
                $('tr#'+tr[i].id).removeClass('hidden')
            }
        }
    })

});