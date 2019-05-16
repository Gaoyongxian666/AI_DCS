// $(function(){
//          //文本框失去焦点后
//         $('form :input').blur(function(){
//             var $parent = $(this).parent();
//             $parent.find(".formtips").remove();
//
//             //验证注册邮件
//             if( $(this).is('#email') ){
//                 if( this.value=="" || ( this.value!="" && !/.+@.+\.[a-zA-Z]{2,4}$/.test(this.value) ) ){
//                       var errorMsg = '请输入正确的E-Mail地址.';
//                       $parent.append('<p class="formtips onError">'+'<span class="glyphicon glyphicon-remove"></span>&nbsp;&nbsp;'+errorMsg+'</span>');
//                 }else{
//                       var okMsg = '输入正确.';
//                       $parent.append('<p class="formtips onSuccess">'+'<span class="glyphicon glyphicon-ok"></span>&nbsp;&nbsp;'+okMsg+'</span>');
//                 }
//             }
//
//
//             //验证注册密码
//             if( $(this).is('#password') ){
//                 if( this.value=="" || this.value.length < 6 ){
//                     var errorMsg = '输入错误,密码至少为六位.';
//                     $parent.append('<p class="formtips onError">'+'<span class="glyphicon glyphicon-remove"></span>&nbsp;&nbsp;'+errorMsg+'</span>');
//                 }else{
//                     var okMsg = '输入正确.';
//                     $parent.append('<p class="formtips onSuccess">'+'<span class="glyphicon glyphicon-ok"></span>&nbsp;&nbsp;'+okMsg+'</span>');
//                 }
//             }
//
//             // //验证登录邮件
//             // if( $(this).is('#logEmail') ){
//             //     if( this.value=="" || ( this.value!="" && !/.+@.+\.[a-zA-Z]{2,4}$/.test(this.value) ) ){
//             //         $parent.append('<p class="formtips logOnError"></span>');
//             //     }else{
//             //         $parent.append('<p class="formtips logOnSucces"></span>');
//             //     }
//             // }
//
//             //验证登录密码
//             if( $(this).is('#logPassword') ){
//                 if( this.value=="" || this.value.length < 6 ){
//                     $parent.append('<p class="formtips logOnError"></span>');
//                 }else{
//                    $parent.append('<p class="formtips logOnSucces"></span>');
//                 }
//             }
//
//         }).keyup(function(){
//            $(this).triggerHandler("blur");
//         }).focus(function(){
//            $(this).triggerHandler("blur");
//         });//end blur
//
//
//         //提交登录，最终验证。
//         $('#logSend').click(function(){
//             $("form :input.logRequired").trigger('blur');
//             var logNumError = $('form .logOnError').length;
//             if(logNumError){
//                 return false;
//             }else{
//                 //
//             }
//         });
//
// });
//
//
