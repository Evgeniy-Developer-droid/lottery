jQuery(document).ready(function ($) {

    $('#search_form_header input').focusout(()=>{
        $('#mini_search_result_wrap').fadeOut();
    })

    $('#search_form_header input').on('keyup', function (e) {
        if ($(this).val().length === 0){$('#mini_search_result_wrap').fadeOut();return 1;}

        if ($(this).val().length > 2) {
            $('#mini_search_result_wrap').fadeIn()
        $('#mini_search_result_wrap').html(`<div class="d-flex justify-content-center align-items-center">
          <div class="spinner-border text-danger" role="status">
          </div>
        </div>`)
            $.ajax({
                url: '/api/search-product-mini',
                type: 'POST',
                data: {search: $(this).val()},
                beforeSend: function (xhr, settings) {

                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                },
                success: function (response) {
                    let html = ``;
                    if (response.length !== 0) {
                        response.forEach((val)=>{
                            html += `<div
                                class="item-lottery-mini d-flex p-2 border rounded m-2">
                                <div class="image col-4"><img
                                    src="${val.thumbnail}"
                                    alt=""></div>
                                <div class="info text-black">
                                    <a href="/single/${val.id}">${val.name}</a>
                                    <p>Price $${val.price} <span class="rounded-circle ${val.status}" title="${val.status}"></span></p>
                                </div>
                            </div>`;
                        })
                        $('#mini_search_result_wrap').html(html)
                    }else{
                        $('#mini_search_result_wrap').html('<div class="d-flex justify-content-center"><div class="text-black">Not found</div></div>')
                    }
                },
            });
        }

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

})