// 绑定页面
$(function () {
    var $tooltips = $('.js_tooltips');

    $(".weui-cell").click(function () {
        $(this).removeClass("weui-cell_warn");
    });

    $(".weui-dialog__btn").click(function () {
        $(".my-mask").fadeOut(100);
    });

    $('#showTooltips').on('click', function () {
            var $stunum = $("#input_stunum");
            var $libpsd = $("#input_libpsd");
            var $edupsd = $("#input_edupsd");
            var $cardpsd = $("#input_cardpsd");
            var $cell_stunum = $("#cell_stunum");
            var $cell_libpsd = $("#cell_libpsd");
            var alertStr = '';
            try {
                if (($stunum.val() == '' )) {
                    $cell_stunum.addClass("weui-cell_warn");
                    alertStr = '请输入学号';
                    throw "err";
                }
                if (($libpsd.val() == '' && $edupsd.val() == '' && $cardpsd.val() == '')) {

                    $cell_libpsd.addClass("weui-cell_warn");
                    alertStr = '请至少填写一项密码';
                    throw "err";
                }
            } catch (e) {
                if ($tooltips.css('display') != 'none') return;
                // toptips的fixed, 如果有`animation`, `position: fixed`不生效
                $('.page.cell').removeClass('slideIn');

                $tooltips.text(alertStr);
                $tooltips.css('display', 'block');
                setTimeout(function () {
                    $tooltips.css('display', 'none');
                }, 2000);
                if (alertStr) {
                    return false;
                }
            }

            $tooltips.text("");
            var $loadingToast = $("#loadingToast");

            $.ajax({
                url: '/bind',
                type: 'post',
                beforeSend: function () {

                    if ($loadingToast.css("display") != "none") return;

                    $loadingToast.show();
                },
                data: {
                    "stuNum": $stunum.val(), "libPsd": $libpsd.val(),
                    "eduPsd": $edupsd.val(), "cardPsd": $cardpsd.val()
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data.status);
                    $loadingToast.hide();
                    $('.my-mask').fadeIn(100);
                    if (data.status == true) {
                        $("#dialogContent2").text("绑定成功~");
                        $('#chooseDialog').fadeIn(100);
                    }
                    else {
                        $("#dialogContent1").text("系统错误.请重试~");
                        $('#infoDialog').fadeIn(100);
                    }
                }
            });
        }
    );
});

$(function () {

    $('.weui-dialog__btn').on('click', function () {
        $(this).parents('.js_dialog').fadeOut(100);
    });

});
function changeButtonResponse(link) {
    $('.weui-dialog__btn').on('click', function () {
        window.location.href = link;
        $(this).parents('.js_dialog').fadeOut(100);
    });
}

function showButtonAndSetLink(text,link) {
    $('.my-mask').fadeIn(100);
    $("#dialogContent1").text(text);
    $('#infoDialog').fadeIn(20);
    changeButtonResponse(link);
}
// 续借页面

$(function () {
    $("#xjButton").on('click', function () {
        $(".booksCheck").animate({"margin-left": "0px"});
        $("#booksListTitle").text("请选择要续借的图书");
        $(this).hide();
        $("#sbButton").show();
        $("#qxButton").show();
    });

    $("#qxButton").on('click', function () {
        $(".booksCheck").animate({"margin-left": "-45px"});
        $("#booksListTitle").text("图书列表");
        $(this).hide();
        $("#sbButton").hide();
        $("#xjButton").show();
    });

    $("#sbButton").on("click", function () {
        var checked = [];
        $("input[name='booksCheckbox']:checked").each(function () {
           checked.push($(this).val());
        });
        if(checked.length == 0){
            $('.my-mask').fadeIn(100);
            $("#dialogContent1").text("你没有选择任何图书");
            $('#infoDialog').fadeIn(20);
            return;
        }
        // 获取url中的参数
        var argStr = window.location.search.split('&');
        var args = {};
        for(var i=0;i<argStr.length;i++){
            var k = argStr[i].split('=')[0].substr(1);
            args[k] = argStr[i].split('=')[1];
        }
        $.ajax({
                url: '/lib/xj',
                type: 'post',
                beforeSend: function () {
                    if(args['user'] === undefined){
                        alert('非法访问');
                        history.back();
                        return;
                    }
                    if ($loadingToast.css("display") != "none") return;

                    $loadingToast.show();
                },
                data: {
                    'books':checked,
                    'aim':'xj',
                    'user': args['user']
                },
                dataType: 'json',
                success: function (data) {
                    if(data.length == 0){
                        showButtonAndSetLink("服务器出错~~请稍后再试");
                    }
                    var i = 0;
                    status = {"-2":"已达到续借限制","-3": "本书不能续借","0":"成功"};
                    checked.each(function () {
                        var value = $(this);
                        $("input[name='booksCheckbox'], input[value="+value+"]").text(status[data[i]]);
                    })
                }
            });
    });
});