// 除logo其他页面上传
    document.getElementById('fileWorks').onchange = function(){
        var imgFileWorks = this.files[0];
        var frWorks = new FileReader();
        frWorks.onload = function(){
            document.getElementById('generateBefore').getElementsByTagName('img')[0].src = frWorks.result;
        };
        frWorks.readAsDataURL(imgFileWorks);
	};