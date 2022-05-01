jQuery(document).ready(function ($){

    $('#launch').click(function (){
        $.ajax('/user/api/define-winners', {
            method: 'POST',
            data: JSON.stringify({'id': $('#lottery_id').val()}),
            contentType : 'application/json',
            dataType : 'json',
            beforeSend: function(xhr, settings) {
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
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function (response){
                if(response.type === "success"){
                    if(typeof response.data === 'undefined'){
                        $('#error_wrap').text(response.message);
                        $('#error_wrap').fadeIn();
                    }else{
                        let html = "";
                        $('#error_wrap').fadeOut();
                        response.data.forEach((val, index)=>{
                            html += `<div class="d-flex text-muted pt-3">
                                      <svg class="bd-placeholder-img flex-shrink-0 me-2 rounded" width="32" height="32" xmlns="http://www.w3.org/2000/svg" 
                                      role="img" aria-label="Placeholder: 32x32" preserveAspectRatio="xMidYMid slice" focusable="false">
                                      <title>Placeholder</title><rect width="100%" height="100%" fill="#007bff"></rect>
                                      <text x="50%" y="50%" fill="#007bff" dy=".3em">32x32</text></svg>
                                
                                      <div class="pb-3 mb-0 small lh-sm border-bottom w-100">
                                        <div class="d-flex justify-content-between">
                                          <strong class="text-gray-dark">${val.full_name}</strong>
                                          <a href="/user/user-detail/${val.user_id}">Profile</a>
                                        </div>
                                        <span class="d-block">Ticket number: ${val.number}</span>
                                      </div>
                                    </div>`
                        })
                        $("#wins_block").html(html)
                    }

                }else{
                    $('#error_wrap').text(response.message);
                    $('#error_wrap').fadeIn();
                }
            }
        })
    })

})