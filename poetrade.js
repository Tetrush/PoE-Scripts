javascript:
(function(){
        if(!location.href.match(/search/)){
            alert('Not correct page');
            return;
        }
    /*  T: ページリフレッシュの周期 */
        var H ='
            var T = 0.5;
            var nowstatus = 0;

            setInterval("mainflow();", T*1000);
            function mainflow(){
                var parentdoc = window.opener.document;
                var whisperbutton = parentdoc.getElementsByClassName("btn btn-xs btn-default direct-btn");

                for(var i=0;i<whisperbutton.length;i++){
                /*  ページ内のボタンを取得・押下済かチェックする*/
                    if(whisperbutton[i].textContent.includes("Direct")){
                        whisperbutton[i].click();
                        document.getElementById("nowstatus").textContent = nowstatus+1;
                        nowstatus++;
                        setInterval("",T*1000);
                    }else{
                        break;
                    }   
                }
            }
        ';
        var openW = open();
        with (openW.document){
            write('<html><script>' + H +'</script><body>処理実行中。<br>現在<span id="nowstatus">0</span>回処理実行</br></body></html>');
        }
})();