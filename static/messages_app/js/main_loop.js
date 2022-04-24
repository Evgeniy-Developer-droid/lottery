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
                if(contacts){
                    let room = contacts.find(`[data-room='${data.content.room}']`);
                    if(room.length === 0){
                        let icon = data.content.icon ? data.content.icon : "https://bootdey.com/img/Content/avatar/avatar7.png"
                        contacts.prepend(`<a href="#" data-room="${data.content.room}" data-user="${data.content.user_id}" 
                            class="list-group-item list-group-item-action border-0 contact">
                            <div class="badge bg-success float-right">1</div>
                            <div class="d-flex align-items-start">
                            <img src="${icon}" class="rounded-circle mr-1" alt="${data.content.name}" width="40" height="40">
                            <div class="flex-grow-1 ml-3">
                                ${data.content.name}
                                </div>
                            </div>
                        </a>`)
                        room = contacts.find(`[data-room='${data.content.room}']`);
                    }else{
                        room.children(".badge").text(parseInt(room.children(".badge").text())+1);
                        room.prependTo('#contacts')
                    }
                    room.css('background', '#d38282')
                }
            }
        }


    }


})