jQuery(document).ready(function ($){
    const pages = parseInt($('#count_pages').val());
    const now_page = parseInt($('#now_page').val());

    let dots = false;
    for(let i = 1; i <= pages; i++){
        if(i === now_page){
            dots = true
            $('#pages-wrap').append(`<li class="page-item active"><a class="page-link" href="?page=${i}">${i}</a></li>`)
        }else{
            if(i === 1 || i === 2 || i === pages || i === pages - 1 || i === now_page - 1 || i === now_page + 1){
                dots = true
                $('#pages-wrap').append(`<li class="page-item"><a class="page-link" href="?page=${i}">${i}</a></li>`)
            } else {
                if(dots){
                    $('#pages-wrap').append('<li class="page-item"><span class="page-link">...</span></li>')
                    dots = false
                }
                continue;
            }
        }
    }

});