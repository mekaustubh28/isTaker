$(document).ready(function () {
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