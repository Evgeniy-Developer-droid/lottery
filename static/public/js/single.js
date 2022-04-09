jQuery(document).ready(function ($){

    $('.buy-button').click(function (){
        $('.bg-custom-modal').fadeIn()
    });

    $('.btn-cancel').click(function (){
        $('.bg-custom-modal').fadeOut()
    });

    $('.btn-buy').click(function (){
        let data = {lottery_id:$('#lottery_id').val()}

        $.ajax({
            type : "POST",
            url: '/api/buy-ticket',
            dataType : "json",
            headers:{
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            data: data,
            success: function (response){
                $('.con').fadeOut()
                if(response.type === 'error'){
                    switch (response.meta){
                        case 'not available':
                            $('.con-not-available p').text(response.message);
                            setTimeout(()=>{
                                $('.con-not-available').fadeIn()
                            }, 1000)
                            break;

                        case 'not price':
                            $('.con-not-price p').text(response.message);
                            setTimeout(()=>{
                                $('.con-not-price').fadeIn()
                            }, 1000)
                            break;

                        case 'not auth':
                            $('.con-not-auth p').text(response.message);
                            setTimeout(()=>{
                                $('.con-not-auth').fadeIn()
                            }, 1000)
                            break;
                    }
                }else{
                    $('.con-success p').text("Your ticket is number "+response.data.ticket_number);
                    $('.con-success h5').text(response.message);
                    setTimeout(()=>{
                        $('.con-success').fadeIn()
                    }, 1000)
                    setTimeout(()=>{
                        $('.bg-custom-modal').fadeOut()
                        document.location.reload();
                    }, 2000)
                }
            }
        })


    });

});