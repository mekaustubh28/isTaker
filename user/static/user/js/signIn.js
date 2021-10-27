$(document).ready(function () {
    // Verification Code
    var answer = 0;
    function verify_question() {
        var rndNum1 = Math.floor(Math.random() * 10) + 1
        var rndNum2 = Math.floor(Math.random() * 10) + 1
        var calculation = Math.floor(Math.random() * 3) + 1
        if (rndNum1 == 0) {
            rndNum1 = 1
        } if (rndNum2 == 0) {
            rndNum2 = 1
        } if (calculation == 0) {
            calculation = 1
        }
        var cal_symbol = ['+', '+', '-', '*']
        calculation = cal_symbol[calculation]
        answer = calc_answer(rndNum1, rndNum2, calculation)
        var question = '' + rndNum1 + ' ' + calculation + ' ' + rndNum2
        $('input#verification_ques').attr('value', question)
    }

    verify_question()

    $('a#reload_question').click(function () {
        verify_question()
    })

    $('a#verify_answer').click(function () {
        var user_answer = $('input#verification_ans').val()
        if (answer == user_answer) {
            check = true
        } else {
            check = false
        }

        if (check) {
            document.getElementById('reload_question').innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="1.5vw" height="1.5vw" fill="green" class="bi bi-check-lg" viewBox="0 0 16 16">
                <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z"/>
                </svg>
            `
            document.getElementById('verify_answer').innerHTML = 'Human Verified'
            $(this).attr('id', 'verified_answer')
            $('a#reload_question').removeAttr('href')
            $('a#reload_question').attr('id', 'verified_answer')
            $('input#verification_ans').attr('disabled', true)
            $('input.submit').attr('disabled', false)
        } else {
            document.getElementById('verify_answer').innerHTML = 'Incorrect Answer'
            $(this).attr('id', 'invalid')
            setTimeout(() => {
                location.reload()
            }, 1000);
        }
    })


    function calc_answer(num1, num2, sym) {
        if (sym == '+') {
            return (num1 + num2)
        } else if (sym == '-') {
            return (num1 - num2)
        } else {
            return (num1 * num2)
        }
    }
    pin_array = []
    $('input#pin_dropdown').on('keyup', function () {
        // tags = document.getElementsByClassName('tag')
        value = $(this).val()
        // for (var x=0;x<tags.length;x++){
        //     tag_array.push(tags[x].innerText)
        // }
        if (value.length > 5) {
            check = 0
            for (var x = 0; x < pin_array.length; x++) {
                if (value == pin_array[x]) {
                    check = 1
                }
            }
            if (check == 0) {
                pin_array.push(value)
            }
        }
        var all_pin = ''
        for (var x = 0; x < pin_array.length; x++) {
            if (x != pin_array.length - 1) {
                all_pin = all_pin + pin_array[x] + ","
            } else {
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
        location.reload()
    })

    $('label.service_boy').click(function () {
        $('div.customer').addClass('hide')
        $('div.service_boy').removeClass('hide')

        $('div#c_human_verification').remove();
    })
    $('input#email_c_choice').attr('checked', true);
    $('input#email_s_choice').attr('checked', true);

    $('input#email_c_choice').click(function () {
        document.getElementById('c_email_number').innerText = 'Email address'
        // $('label#email_number').text('value','Email address')
        $('input#c_number').attr('type', 'email')
        $('input#c_number').attr('name', 'email')
        $('input#c_number').attr('placeholder', 'Email')
        $('input#c_number').attr('value', '')
        $('input#c_number').attr('id', 'c_email')
    })

    $('input#number_c_choice').click(function () {
        document.getElementById('c_email_number').innerText = 'Contact Number'
        $('input#c_email').attr('type', 'number')
        $('input#c_email').attr('name', 'number')
        $('input#c_email').attr('value', '')
        $('input#c_email').attr('placeholder', 'Phone Number')
        $('input#c_email').attr('id', 'c_number')
    })

    $('input#email_s_choice').click(function () {
        document.getElementById('s_email_number').innerText = 'Email'
        $('input#s_number').attr('type', 'email')
        $('input#s_number').attr('name', 'email')
        $('input#s_number').attr('placeholder', 'Email')
        $('input#s_number').attr('value', '')
        $('input#s_number').attr('id', 's_email')
    })

    $('input#number_s_choice').click(function () {
        document.getElementById('s_email_number').innerText = 'Contact Number'
        $('input#s_email').attr('type', 'number')
        $('input#s_email').attr('name', 'number')
        $('input#s_email').attr('value', '')
        $('input#s_email').attr('placeholder', 'Phone Number')
        $('input#s_email').attr('id', 's_number')
    })


    if (localStorage.getItem('c_credentials') != null) {
        $('input#c_email').attr('value', JSON.parse(localStorage.getItem('c_credentials'))['email'])
    }
    if (localStorage.getItem('s_credentials') != null) {
        $('input#ID').attr('value', JSON.parse(localStorage.getItem('s_credentials'))['ID'])
        $('input#s_email').attr('value', JSON.parse(localStorage.getItem('s_credentials'))['email'])
    }
});