jQuery(document).ready(function ($){


    function generateOrder() {
        let chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let order = '';
        for(let i = 0; i < 10; i++) {
            order += chars[Math.floor(Math.random() * chars.length)];
        }
        return order;
    }

    $('#pay-link').click(function (e){
        e.preventDefault();
        let amount = $('#amount').val()
        if(amount){
            let link = $(this).attr("href")+"?amount=";
            link += amount;
            link += "&order_id="+generateOrder()
            window.location.href = link
        }else{
            $(".alert").text("Enter coins please")
            setTimeout(()=>{
                $(".alert").fadeIn()
            }, 1000)
        }
    })


})