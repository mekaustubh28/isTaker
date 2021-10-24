$(document).ready(function () {
    pin_array = []
    $('input#pin_dropdown').on('keyup', function(){
        // tags = document.getElementsByClassName('tag')
        value = $(this).val()
        // for (var x=0;x<tags.length;x++){
        //     tag_array.push(tags[x].innerText)
        // }
        if(value.length>5){
            check = 0
            for(var x=0;x<pin_array.length;x++){
                if (value==pin_array[x]){
                    check = 1
                }
            }
            if(check == 0){
                pin_array.push(value)
            }
            console.log(pin_array)
        }
        var all_pin = ''
        for(var x=0;x<pin_array.length;x++){
            if(x!=pin_array.length-1){
                all_pin = all_pin + pin_array[x] + ","
            }else{
                all_pin = all_pin + pin_array[x]
            }
        }
        $('input#s_pin_serve').attr('value', all_pin)
        $('input#demo_pin_serve').attr('value', all_pin)
    })

    $('select#languages_dropdown').click(function () {
        prev_langauges = $('input#s_languages').val()
        current_language = $(this).val()
        $("select#languages_dropdown option[value=" + current_language + "]").remove();
        if (prev_langauges == '') {
            $('input#s_languages').attr('value', current_language)
        } else {
            $('input#s_languages').attr('value', prev_langauges + ", " + current_language)
        }
        $('input#demo_languages').attr('value', $('input#s_languages').val())
    });

    $('label.customer').click(function () {
        $('div.customer').removeClass('hide')
        $('div.service_boy').addClass('hide')
    })

    $('label.service_boy').click(function () {
        $('div.customer').addClass('hide')
        $('div.service_boy').removeClass('hide')
    })
    $('input#email_c_choice').attr('checked', true);
    $('input#email_s_choice').attr('checked', true);

    $('input#email_c_choice').click(function(){
        document.getElementById('c_email_number').innerText='Email address'
        // $('label#email_number').text('value','Email address')
        $('input#c_number').attr('type','email')
        $('input#c_number').attr('name','email')
        $('input#c_number').attr('placeholder','Email')
        $('input#c_number').attr('value','')
        $('input#c_number').attr('id','c_email')
    })

    $('input#number_c_choice').click(function(){
        document.getElementById('c_email_number').innerText='Contact Number'
        $('input#c_email').attr('type','number')
        $('input#c_email').attr('name','number')
        $('input#c_email').attr('value','')
        $('input#c_email').attr('placeholder','Phone Number')
        $('input#c_email').attr('id','c_number')
    })

    $('input#email_s_choice').click(function(){
        document.getElementById('s_email_number').innerText='Email'
        $('input#s_number').attr('type','email')
        $('input#s_number').attr('name','email')
        $('input#s_number').attr('placeholder','Email')
        $('input#s_number').attr('value','')
        $('input#s_number').attr('id','s_email')
    })

    $('input#number_s_choice').click(function(){
        document.getElementById('s_email_number').innerText='Contact Number'
        $('input#s_email').attr('type','number')
        $('input#s_email').attr('name','number')
        $('input#s_email').attr('value','')
        $('input#s_email').attr('placeholder','Phone Number')
        $('input#s_email').attr('id','s_number')
    })

    
    if (localStorage.getItem('c_credentials') != null) {
        $('input#c_email').attr('value', JSON.parse(localStorage.getItem('c_credentials'))['email'])
    }
    if (localStorage.getItem('s_credentials') != null) {
        $('input#ID').attr('value', JSON.parse(localStorage.getItem('s_credentials'))['ID'])
        $('input#s_email').attr('value', JSON.parse(localStorage.getItem('s_credentials'))['email'])
    }
});