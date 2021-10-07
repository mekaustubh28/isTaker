$(document).ready(()=>{
    var x = 0

    $('input[type="checkbox"]').click(function () {
        $('button#service_confirm').attr('disabled', false)
        $('button#service_reset').attr('disabled', false)
        var service = $(this).attr('id')
        var price = $(this).attr('name')
        if ($(this).prop("checked") == true) {
            addTable(price, service)
        } else if ($(this).prop("checked") == false) {
            deleteTable(price, service)
        }
    });

    function addTable(price, service) {
        x = x + parseInt(price)
        var table = '<tr value="' + service + '"><td>' + service + '</td><th scope="row">₹' + price + '/-</th></tr>'
        document.getElementById('table-content').innerHTML += table
    }

    function deleteTable(price, service) {
        x = x - parseInt(price)
        var table = $('tr[value="' + service + '"]')
        table[0].remove()
    }

    $('button#service_confirm').click(function () {
        var service_list = []
        var service_price = []
        $('input[type="checkbox"]').attr('disabled', true)
        $('button#service_reset').attr('disabled', false)
        var table_content = $('#table-content').find('tr')
        var table = document.getElementsByTagName('table')[0];
        //console.log(table)
        for (let index = 0; index < table_content.length; index++) {
            var Row = table.rows[index + 1];
            var Content = Row.firstChild.textContent;
            var price = Row.children[1].innerHTML;
            price = price.substring(1, price.length - 2)
            service_price.push(price)
            service_list.push(Content)
        }
        service_price.push(x)
        $('input#service_list').attr('value', service_list)
        $('input#total_price').attr('value', service_price)
    })

    $('button#service_reset').click(function(){
        $('input[type="checkbox"]').prop("checked", false)
        document.getElementById('table-content').innerHTML = ''
        $('button#service_confirm').attr('disabled', true)
        $('button#service_reset').attr('disabled', true)
    })
});