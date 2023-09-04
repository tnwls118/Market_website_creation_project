$(document).ready(function () {
    $(".list-group-item-action").click(function () {
        let product_title = $(this).attr('id');
        $.get("http://127.0.0.1:5000/detail?title=" + product_title)
            .then(function (result) {
                $("#detailModalLabel").text(result.title);
                $("#detailModalLocation").text('지역: ' + result.location);
                $("#detailModalPrice").text('가격: ' + result.price);
                $("#detailModalImage").attr('src', '/static/' + result.image);
                $("#detailModalContent").html(result.content);
                $("#detailModal").modal('show');
            });
    });
});