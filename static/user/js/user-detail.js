jQuery(document).ready(function ($){

    $('.change-avatar').click(()=>{$('#file').click()})

    $("#file").change(function (){
        let fd = new FormData();
        let files = $('#file')[0].files;

        // Check file selected or not
        if(files.length > 0 ) {
            fd.append('file', files[0]);
            $.ajax({
                url: '/user/api/change-user-avatar',
                type: 'POST',
                data: fd,
                contentType: false,
                processData: false,
                beforeSend: function(xhr, settings) {
                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                },
                success: function(response){
                    if(response.type === "success"){
                        let m = $("#messages-response")
                        m.text(response.message)
                        m.addClass("alert-success");
                        m.fadeIn()
                        setTimeout(()=>{
                            window.location.reload()
                        }, 1500)
                    }else{
                        let m = $("#messages-response")
                        m.text(response.message)
                        m.removeClass("alert-success")
                        m.addClass("alert-danger");
                        m.fadeIn()
                    }
                },
            });
        }
    })


    $(".field-row").mouseenter(function (){
        let wrap = $(this)
        wrap.children(".btn-custom").fadeIn()
    })

    $(".field-row").mouseleave(function (){
        let wrap = $(this)
        setTimeout(()=>{
            wrap.children(".btn-custom").fadeOut()
        }, 2000)
    })

    $(".btn-custom").click(function (){
        let parent = $(this).parent();
        parent.children(".text-secondary").fadeOut()
        setTimeout(()=>{
            parent.children(".input-group").fadeIn()
        }, 1000)
    })

    $(".btn-save").click(function (){
        let parent = $(this).parent()
        let value = parent.children('.form-control').val()
        let action = parent.children('.form-control').data('action')
        console.log(value, action)
        $.ajax({
            url: '/user/api/change-user-data',
            type: 'POST',
            data: {value:value, action:action},
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                if(response.type === "success"){
                    let m = $("#messages-response")
                    m.text(response.message)
                    m.addClass("alert-success");
                    m.fadeIn()
                    setTimeout(()=>{
                        window.location.reload()
                    }, 1500)
                }else{
                    let m = $("#messages-response")
                    m.text(response.message)
                    m.removeClass("alert-success")
                    m.addClass("alert-danger");
                    m.fadeIn()
                }
            },
        });
    })


    $('#complain').click(function (){
        $.ajax({
            url: '/user/api/add-complain',
            type: 'POST',
            data: {user:$("#user_id").val()},
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                if(response.type === "success"){
                    let m = $("#messages-response")
                    m.text(response.message)
                    m.addClass("alert-success");
                    m.fadeIn()
                    setTimeout(()=>{
                        window.location.reload()
                    }, 1500)
                }else{
                    let m = $("#messages-response")
                    m.text(response.message)
                    m.removeClass("alert-success")
                    m.addClass("alert-danger");
                    m.fadeIn()
                }
            },
        });
    });

    $('#estimate').click(function (){
        $("#modalChoice").fadeIn()
    });
    $("#modalChoice").click(function (){
        $(this).fadeOut()
    })
    $('.btn-rating').click(function (){
        $.ajax({
            url: '/user/api/add-estimate',
            type: 'POST',
            data: {user:$("#user_id").val(), value: parseInt($(this).text())},
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                if(response.type === "success"){
                    let m = $("#messages-response")
                    m.text(response.message)
                    m.addClass("alert-success");
                    m.fadeIn()
                    setTimeout(()=>{
                        window.location.reload()
                    }, 1500)
                }else{
                    let m = $("#messages-response")
                    m.text(response.message)
                    m.removeClass("alert-success")
                    m.addClass("alert-danger");
                    m.fadeIn()
                }
            },
        });
    })



    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie != '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});