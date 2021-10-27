$(document).ready(function () {
        $('a').click(function(){
                var id = $(this).attr('id')
                // console.log(id)
                var name = document.getElementsByClassName(id)[0].innerText
                // console.log(name)
                $('input#pending_ID').attr('value',id)
                document.getElementById('ID').innerText = id
                document.getElementById('name').innerText = name
                document.getElementById('span_name').innerText = name
        })
});