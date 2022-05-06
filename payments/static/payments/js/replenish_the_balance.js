jQuery(document).ready(function ($){
    // some

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

    $('#amount').keyup(function (e){
        let val = $(this).val();

        const threshold = parseFloat($('#threshold').val());
        const tax_top_up_fixed = parseFloat($('#tax_top_up_fixed').val());
        const tax_top_up_percent = parseFloat($('#tax_top_up_percent').val());

        if(val){
            val = parseFloat(val)
            if(val < threshold){
                $('#commis').text('$'+tax_top_up_fixed)
                $('#total').text('$'+(val+tax_top_up_fixed))
            }else{
                let commis = val * (tax_top_up_percent / 100)
                $('#commis').text('$'+Math.round((commis) * 100) / 100)
                $('#total').text('$'+Math.round((val+commis) * 100) / 100)
            }
        }else {
            $('#commis').text('$0')
            $('#total').text('$0')
        }
    })


})