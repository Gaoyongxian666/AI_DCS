/**
 * Created by zxm on 2017/5/20.
 */
$(function(){
    var selectImgTake = {
        "init":function(divId,maxSelectNumber){
            if(maxSelectNumber==null||maxSelectNumber==""){
                selectImgTake.initSelectEvent(divId,-1);
            }else{
                selectImgTake.initSelectEvent(divId,maxSelectNumber);
            }
        },
        "initSelectEvent":function(divId,maxSelectNumber){
            $("#"+divId+" .item").on("click",function(){
                var i_display = $(this).find(".img_isCheck i").css("display"); //判断图片的状态
                if(i_display=="none"){     //图片未选中
                    if(maxSelectNumber!=-1){    //指定了几张
                        var selectImgDivs = selectImgTake.getSelectImgs(divId);
                        if(selectImgDivs.length>=maxSelectNumber){
                            // alert("最多只能选择"+maxSelectNumber+"张图片");
                            return;
                        }
                    }
                    $(this).find(".img_isCheck i").css("display","block");
                    $(this).attr("ischecked","true");
                }else{//图片选中
                    $(this).find(".img_isCheck i").css("display","none");
                    $(this).removeAttr("ischecked");
                }
            });
        },
        "getSelectImgs":function(divId){
            var selectImgDivs = $("#"+divId+" .item[ischecked='true']");
            return selectImgDivs;
        },
        "cancelInit":function(divId){
            // $("#"+divId+" .item").off("click");
            $(".img_isCheck i").css("display","none");
            $("#"+divId+" .item").removeAttr("ischecked");
        }
    };

    selectImgTake.init('selectItemDiv');//先定义，在调用

    $("#cancel").click(function(){
        selectImgTake.cancelInit('selectItemDiv');
    });
})



