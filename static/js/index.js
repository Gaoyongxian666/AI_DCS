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

        
        
});


