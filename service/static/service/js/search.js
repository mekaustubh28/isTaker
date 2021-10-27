$(document).ready(() => {

        $('div#hospital').click(function () {
                var id = $(this).attr('name')
                $('input').attr('checked', false)
                $('input#' + id).attr('checked', true)
                $('input#' + id + 'place').attr('checked', true)
                $('input#hospital_id').attr('value', $(this).attr('name'))
                $('button#hospital_done').attr('disabled', false)
                $('div#hospital').removeClass('select')
                $(this).addClass('select')
        })

        $('button#btn_search_by_place').click(function () {
                // console.log('id="btn_search_by_place"')
        })

        $('button#btn_search_by_pin').click(function () {
                // console.log('id="btn_search_by_pin"')
        })

});