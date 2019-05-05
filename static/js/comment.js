$(function(){
    $("body").delegate(".comment","propertychange input",function(){
        if($(this).val().length > 0 ){
            //让按钮可用，此时的this变指的是输入框的变化
            $(".submitButton").prop("disabled", false).css("background","#01A0EC");
        }else{
            //让按钮不可用
            $(".submitButton").prop("disabled",true).css("background","gray");

        }
    });

    //监听评论按钮，如果创建了内容使其显示在页面上
    $(".submitButton").click(function(){

        //得到用户输入的内容
        var $text = $(".comment").val();
        var $name = $(this).parents(".myDiscussion").find(".media-heading").html();
        var $comment = createEle($text,$name);
        $(".messageList").prepend($comment);
        $(".comment").val("");
    });
    
    //监听“顶一下”点击
    $("body").delegate(".infoTop","click",function(){
        $(this).text(parseInt($(this).text()) + 1);
    });

    //监听“踩一下”点击
    $("body").delegate(".infoDown","click",function(){
        $(this).text(parseInt($(this).text()) + 1);
    });

    //监听“小回复”点击
    $("body").delegate(".infoRes","click",function(){
        // alert("q");
        $(this).parents(".infoOperation").siblings(".infoResMod").toggle();
    });

    //监听“大回复”按钮
    $("body").delegate(".replyButton","click",function(){
        // alert("q");
        $(this).parent(".infoResMod").hide(100);

        var $resText = $(".infoResMod_res").val();
        var $resComment = createEle( $resText);
        $(this).parent(".infoResMod").siblings(".infoNewRes").prepend($resComment);
        $(this).siblings(".infoResMod_res").val("");
    });



    // $(".infoRes").click(function(){
    //     $(".infoResText").toggle();
    // });
    
    //创建节点的方法
    function createEle(text,name){
        var $comment = $("<li class=\"info\">\n" +
            "                                <div class=\"media-left commentHead\">\n" +
            "                                    <a href=\"#\">\n" +
            "                                    <img class=\"media-object\" src=\"../static/img/head.jpg\" alt=\"...\">\n" +
            "                                    </a>\n" +
            "                                </div>\n" +
            "                                <div class=\"media-body commentContent\">\n" +
            "                                        <p class=\"infoName\">"+ name +"</p>\n" +
            "                                        <p class=\"infoText\">"+ text +"</p>\n" +
            "                                        <p class=\"infoOperation\">\n" +
            "                                            <span class=\"infoTime\">"+ formartDate()+"</span>\n" +
            "                                            <span><a href=\"javascript:;\" class=\"infoRes\">回复</a></span>\n" +
            "                                            <span class=\"infoHandle\">\n" +
            "                                                <a href=\"javascript:;\"class=\"infoTop\">0</a>\n" +
            "                                                <a href=\"javascript:;\"class=\"infoDown\">0</a>\n" +
            "                                               <!--  <a href=\"javascript:;\"class=\"infoDel\">删除</a> -->\n" +
            "                                            </span>\n" +
            "                                        </p>\n" +
            "                                        <p class=\"infoResMod\"style=\"display:none;\">\n" +
            "                                            <textarea class=\"form-control infoResMod_res\" rows=\"3\">回复@"+ name +"：</textarea>\n" +
            "                                            <input type=\"button\" value=\"回复\" class=\"replyButton\">\n" +
            "                                        </p>                                   \n" +
            "                                        <p class=\"infoNewRes\">\n" +
            "                                        </p>                                   \n" +
            "                                </div> \n" +
            "                            </li>");
        return $comment;
    };

    //生成时间的方法
    function formartDate(){
        var data = new Date();
        //想要得到的格式 2018-10-19 19:22:23
        var arr = [data.getFullYear() + "-",
                    data.getMonth() + 1 + "-",
                    data.getDate() + " ",
                    data.getHours() + ":",
                    data.getMinutes() + ":",
                    data.getSeconds()];
        return arr.join("");
    }
});