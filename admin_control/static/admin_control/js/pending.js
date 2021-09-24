$(document).ready(function () {
        $('a').click(function(){
                var id = $(this).attr('id')
                var Class = $(this).attr('class')
                var customer_id = $(this).attr('data-filter-item')
                console.log(customer_id)
                document.getElementById('span_customer').innerText = customer_id
                document.getElementById('span_id').innerText = id
                document.getElementById('span_pin').innerText = Class
                $('input#customer_id').attr('value',customer_id)
                $('input#customer_trip_id').attr('value',id)
        })
});