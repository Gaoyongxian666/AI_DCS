from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

num_progress = 0 # 当前的后台进度值（不喜欢全局变量也可以很轻易地换成别的方法代替）

def process_html(request):
    task_id= request.GET['task_id']
    return render(request, "progress.html",{
        "task_id":task_id
    })

    # for i in range(12345):
    #     # ... 数据处理业务
    #     num_progress = i * 100 / 12345 # 更新后台进度值，因为想返回百分数所以乘100
    # return JsonResponse("ok", safe=False)

def show_progress(request):
    return JsonResponse(num_progress, safe=False)