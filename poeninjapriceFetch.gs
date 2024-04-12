var apikey = "ak-p6shy-rw5ce-z1yeq-mgj3e-2f833";
 
function pjscloudget() {
  //Target URL
  var url = "https://poe.ninja/economy/affliction/essences";
 
  //HTTPSレスポンスに設定するペイロードのオプション項目を設定する
  var option = {
    url:url,
    renderType:"HTML",
    outputAsJson:true
  };
 
  var payload = JSON.stringify(option);
  payload = encodeURIComponent(payload);
 
  var requesturl = "https://phantomjscloud.com/api/browser/v2/"+ apikey +"/?request=" + payload;
 
  var ret = UrlFetchApp.fetch(requesturl);
 
  var json = JSON.parse(ret.getContentText());
 
  var source = json["content"]["data"];
 
  var $ = Cheerio.load(source);
 
  var $tables = $('.table td');
 
  var essence = [];
  var temparr = [];
 
  var cnt = 1;
  $tables.each(function(index, element) {
    //tdの値を取り出す
    let value = $(element).text();
    temparr.push(value);
 
    cnt = cnt + 1;
 
    //カウンタが7になったら配列を1個進める
    if(cnt == 7){
      essence.push(temparr);
 
      cnt = 1;
      temparr = [];
    }
  });
 
  //essenceをスプレッドシートに書き出す
  var ui = SpreadsheetApp.getUi();
  var ss = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("scraping");
  var colcnt = essence[0].length;
  var rowcnt = essence.length;
  ss.getRange(2,1,rowcnt,colcnt).setValues(essence);
 
  //終了メッセージ
  ui.alert("Updated Successfully");
}