$(function(){

    // 控制密码验证
    //文本框失去焦点后
    $('form :input').blur(function(){
        var $parent = $(this).parent();
        $parent.find(".formtips").remove();

        //修改密码
        if( $(this).is('#personPassword') ){
            if( this.value=="" || this.value.length < 6 ){
                var errorMsg = '密码至少为六位.';
                $parent.append('<p class="formtips perOnError">'+'<span class="glyphicon glyphicon-remove"></span>&nbsp;&nbsp;'+errorMsg+'</span>');
            }else{
                var okMsg = '可以使用.';
                $parent.append('<p class="formtips perOnSuccess">'+'<span class="glyphicon glyphicon-ok"></span>&nbsp;&nbsp;'+okMsg+'</span>');
            }
        }
        //再次验证密码，判断两次是否一致
        if( $(this).is('#personRePassword') ){
            var pw= document.getElementById("personPassword");
            var pwValue = pw.value;
            if( this.value=="" || this.value.length < 6 || this.value != pwValue){
                var errorMsg = '';
                $parent.append('<p class="formtips perOnError">'+errorMsg+'</span>');
            }else{
                var okMsg = '两次密码一致';
                $parent.append('<p class="formtips perOnSuccess">'+'<span class="glyphicon glyphicon-ok"></span>&nbsp;&nbsp;'+okMsg+'</span>');
            }
        }
    }).keyup(function(){
       $(this).triggerHandler("blur");
    }).focus(function(){
       $(this).triggerHandler("blur");
    });//end blur

    //提交修改密码，最终验证。
    $('#perSend').click(function(){
        $("form :input.perRequired").trigger('blur');
        var perNumError = $('form .perOnError').length;
        if(perNumError){
            return false;
        }else{
            alert('修改成功.')
        }
    });

    // 响应式导航
    $('#navClick').click(function(){
        $('.rigtNav').toggle();
    });
    $("#close").find("li").click(function(){
        $("#close").hide();
    });

    //介绍页的文字跳动
    // $(".function_name_we").lbyl({
    //     content:"innovative,enthusiastic...",
    //     speed: 100,
    //     type: 'show',
    //     fadeSpeed: 500
    // });

    //各种功能页图片的上传
    $("#imgUpload").change(function(){
        var imgURL = getImgURL(this.files[0]);
        if (imgURL)
        {
            $("#showImg").attr("src", imgURL);
        }
    });
    function getImgURL(Img)
    {
        var url = null ;
        if (window.createObjectURL!=undefined)
        { // basic
            url = window.createObjectURL(Img) ;
        }
        else if (window.URL!=undefined)
        {
            // mozilla(firefox)
            url = window.URL.createObjectURL(Img) ;
        }
        else if (window.webkitURL!=undefined) {
            // webkit or chrome
            url = window.webkitURL.createObjectURL(Img) ;
        }
        return url ;
    }

    //先让表单禁止提交
    // $("form").click(function(){
    //     // event.preventDefault();
    // });

    //进度条处理函数
    // $("#imgGenerated").click(function(){
    //     $(".function_progress").show();
    //     $


    // });
});


