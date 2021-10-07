$('button.pending-order-btn').click(function(){
        id = $(this).attr('id')
        $('input#pendingOrder').attr('value', id)
})