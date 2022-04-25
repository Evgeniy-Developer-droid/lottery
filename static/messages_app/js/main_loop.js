jQuery(document).ready(function ($){

    let user_id = $('#user_id').val();
    let socket = null;


    if(user_id){
        socket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/event/'
            + user_id
            + '/'
        );

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);

            if(data.content.type === 'message'){
                let contacts = $('#contacts')

                if(contacts.length){
                    let room = contacts.find(`[data-room='${data.content.room}']`);
                    if(room.length === 0){
                        let icon = data.content.icon ? data.content.icon : "/static/public/img/default-user-icon.jpg"
                        contacts.prepend(`<a href="#" data-room="${data.content.room}" data-user="${data.content.user_id}" 
                            class="list-group-item list-group-item-action border-0 contact not-read">
                            <div class="badge bg-success float-right">1</div>
                            <div class="d-flex align-items-start">
                            <img src="${icon}" class="rounded-circle mr-1" alt="${data.content.name}" width="40" height="40">
                            <div class="flex-grow-1 ml-3">
                                ${data.content.name}
                                </div>
                            </div>
                        </a>`)
                    }else{
                        if(!room.hasClass('select')){
                            room.children(".badge").text(parseInt(room.children(".badge").text())+1);
                            room.prependTo('#contacts')
                            room.addClass('not-read')
                        }
                    }
                }else{
                    $('#new-mess-icon').css('background', 'red');
                    $('#drop-dawn').removeClass('btn-warning');
                    $('#drop-dawn').addClass('btn-danger');
                    localStorage.setItem('new-message', 1);
                    playSound($('#notification-soung').val())
                }
            }
        }


    }

    if(parseInt(localStorage.getItem('new-message')) === 1){
        $('#new-mess-icon').css('background', 'red');
        $('#drop-dawn').removeClass('btn-warning');
        $('#drop-dawn').addClass('btn-danger');
    }


    function playSound(url) {
        const audio = new Audio(url);
        audio.play();
    }


})