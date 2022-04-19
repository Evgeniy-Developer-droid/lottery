jQuery(document).ready(function ($){

    let connection = null;


    const readMessages = (room) => {
        const data = {room:room}
        $.ajax({
            url: '/user/api/read-messages',
            type: 'POST',
            data: data,
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                if(response.type === "success"){
                    let links = $("#contacts").find(`[data-room='${room}']`);
                    links.children(".badge").text(0);
                }
            },
        });
    }



    const startSocket = (room) => {
        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + room
            + '/'
        );
        return chatSocket
    }


    const newConnection = (room) => {
        connection = startSocket(room);
        connection.onmessage = function(e) {
            const data = JSON.parse(e.data);
            let icon = data.message.icon ? data.message.icon : "https://bootdey.com/img/Content/avatar/avatar7.png"
            let date = data.message.timestamp.split('T')[0];
            let time = data.message.timestamp.split('T')[1].split(".")[0]
            let timestamp = date+" "+time;
            if(data.message.user_id === parseInt($('#companion').val())){
                $('.chat-messages').append(`<div class="chat-message-left pb-4">
                    <div>
                        <img src="${icon}" class="rounded-circle mr-1" width="40" height="40">
                    </div>
                        <div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3">
                        <div class="font-weight-bold mb-1">${data.message.name} 
                        <span style="font-size: 10px" class="text-muted small text-nowrap mt-2">${timestamp}</span>
                        </div>
                            ${data.message.body}
                    </div>
                </div>`)
            }else{
                $('.chat-messages').append(`<div class="chat-message-right pb-4">
                    <div>
                        <img src="${icon}" class="rounded-circle mr-1" width="40" height="40">
                    </div>
                        <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                        <div class="font-weight-bold mb-1">${data.message.name} 
                        <span style="font-size: 10px" class="text-muted small text-nowrap mt-2">${timestamp}</span>
                        </div>
                            ${data.message.body}
                            
                    </div>
                </div>`)
            }
            $('.chat-messages').animate({ scrollTop: $('.chat-messages')[0].scrollHeight }, 1000);
            readMessages(room)
        };
        connection.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
    }




    $('#btn-send').click(function (){
        const data = {
            room: parseInt($('#room').val()),
            receiver: parseInt($('#companion').val()),
            body: $('#input-send').val()
        }
        $('#input-send').val("")
        $.ajax({
            url: '/user/api/post-message',
            type: 'POST',
            data: data,
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                if(response.type === "success"){
                    connection.send(JSON.stringify({message:response.data}));
                }
            },
        });

    })


    const initMessages = () => {
        $.ajax({
            url: '/user/api/get-contacts',
            type: 'POST',
            data: {},
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                response.forEach((val, index)=>{
                    let icon = val.icon ? val.icon : "https://bootdey.com/img/Content/avatar/avatar7.png"
                    $('#contacts').append(`<a href="#" data-room="${val.room_id}" data-user="${val.user_id}" 
                            class="list-group-item list-group-item-action border-0 contact">
                            <div class="badge bg-success float-right">${val.new}</div>
                            <div class="d-flex align-items-start">
                            <img src="${icon}" class="rounded-circle mr-1" alt="${val.name}" width="40" height="40">
                            <div class="flex-grow-1 ml-3">
                                ${val.name}
                                </div>
                            </div>
                        </a>`)
                })
            },
        });
    }


    $(document.body).on('click', '.contact' ,function(){
        if(connection){
            connection.close()
        }
        let room = $(this).data('room')
        readMessages(room)
        $('#companion').val($(this).data('user'))
        $('#room').val($(this).data('room'))
        newConnection(room);
        $.ajax({
            url: '/user/api/get-messages',
            type: 'POST',
            data: {'room':room},
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                $('.chat-messages').empty();
                let icon_meta = response.companion.icon ? response.companion.icon : "https://bootdey.com/img/Content/avatar/avatar7.png"
                $('#user-meta').html(`<div class="d-flex align-items-center py-1">
                    <div class="position-relative">
                        <img src="${icon_meta}" class="rounded-circle mr-1" width="40" height="40">
                    </div>
                    <div class="flex-grow-1 pl-3">
                        <strong>${response.companion.name}</strong>
                    </div>
                </div>`)

                response.messages.forEach((val, index)=>{
                    let icon = val.icon ? val.icon : "https://bootdey.com/img/Content/avatar/avatar7.png"
                    let date = val.timestamp.split('T')[0];
                    let time = val.timestamp.split('T')[1].split(".")[0]
                    let timestamp = date+" "+time;
                    if(val.user_id === response.companion.user_id){
                        $('.chat-messages').append(`<div class="chat-message-left pb-4">
                            <div>
                                <img src="${icon}" class="rounded-circle mr-1" width="40" height="40">
                            </div>
                                <div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3">
                                <div class="font-weight-bold mb-1">${val.name} 
                                <span style="font-size: 10px" class="text-muted small text-nowrap mt-2">${timestamp}</span>
                                </div>
                                    ${val.body}
                            </div>
                        </div>`)
                    }else{
                        $('.chat-messages').append(`<div class="chat-message-right pb-4">
                            <div>
                                <img src="${icon}" class="rounded-circle mr-1" width="40" height="40">
                            </div>
                                <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                                <div class="font-weight-bold mb-1">${val.name} 
                                <span style="font-size: 10px" class="text-muted small text-nowrap mt-2">${timestamp}</span>
                                </div>
                                    ${val.body}
                                    
                            </div>
                        </div>`)
                    }
                })

                $('.chat-messages').animate({ scrollTop: $('.chat-messages')[0].scrollHeight }, 1000);

            },
        });
    })




    initMessages()



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