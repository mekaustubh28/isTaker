$('li.link').click(function () {
        $('li.link').removeClass('active_link')
        $(this).addClass('active_link')
    })
    $('li.section').click(function () {
        var id = $(this).attr('id')
        $('div.section').addClass('noshow')
        $('div.' + id).removeClass('noshow')
    })
    $('span#name').click(function () {
        console.log('wprking')
        $('input.name').attr('disabled', false)
        $('button.name').removeClass('noshow')
    })
    $('span#father_name').click(function () {
        console.log('wprking')
        $('input.father_name').attr('disabled', false)
        $('button.father_name').removeClass('noshow')
    })
    $('span#email').click(function () {
        console.log('wprking')
        $('input.email').attr('disabled', false)
        $('button.email').removeClass('noshow')
    })
    $('span#mobile').click(function () {
        console.log('wprking')
        $('input.mobile').attr('disabled', false)
        $('button.mobile').removeClass('noshow')
    })

    $('span#address').click(function () {
        console.log('wprking')
        $('input.address').attr('disabled', false)
        $('button.address').removeClass('noshow')
    })

    $('span#state').click(function () {
        console.log('wprking')
        $('select.state').attr('disabled', false)
        $('button.state').removeClass('noshow')
    })

    $('span#city').click(function () {
        console.log('wprking')
        $('input.city').attr('disabled', false)
        $('button.city').removeClass('noshow')
    })
    $('span#pin').click(function () {
        console.log('wprking')
        $('input.pin').attr('disabled', false)
        $('button.pin').removeClass('noshow')
    })
    $('span#adhaar').click(function () {
        console.log('wprking')
        $('input.adhaar').attr('disabled', false)
        $('button.adhaar').removeClass('noshow')
    })