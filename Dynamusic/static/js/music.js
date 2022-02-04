var i;                      // 再生している行
var speed = 120;            // 曲の速さ
var isPlay = false;         // 再生中かどうか
var isFirst = true;         // はじめから再生するかどうか
var isAutoscroll = true;    // 自動スクロールはするかどうか
var isAutoplay;             // 途中から再生するかどうか
var isloaded = false;       // ロードがしているかどうか
var isStoped = false;       // 一度でも停止ボタンが押されたら
var intervalId, musicTableId, autoscrollButtonId, playpauseButtonId, sliderlabelId, sliderId, isAutoplayDummyId;
var track_num;


// ロードが終わったか判断する関数
window.onload = function(){
    // ロード後の処理
    isloaded = true;

    // 要素の取得
    musicTableId = document.getElementById('musicTable');
    autoscrollButtonId = document.getElementById('autoscrollButton');
    playpauseButtonId = document.getElementById('playpauseButton');
    sliderlabelId = document.getElementById("sliderlabel");
    sliderId = document.getElementById("slider");

    // トラック列の列数の取得
    track_num = document.getElementById("0").childElementCount - 5;

    // ローディング画面を非表示
    var tableLoadId = document.getElementById('tableLoad');
    if (tableLoadId != null) {
        tableLoadId.style.display = "none";
    }
    
    // テーブルを表示
    var tableWarapperId = document.getElementById('table-wrapper');
    if (tableWarapperId != null) {
        tableWarapperId.style.display = "block";
    }

    // プレイヤーを表示
    var playerId = document.getElementById('player');
    if (playerId != null) {
        playerId.style.display = "block";
    }

    // 自動再生するかどうか
    var isAutoplayDummyId = document.getElementById('isAutoplayDummy');
    if (isAutoplayDummyId != null) {
        isAutoplay = isAutoplayDummyId.innerText;
        if (isAutoplay != '') {        // 途中再生をする場合は
            i = Number(isAutoplay);
            if (isPlay) {
                musicplaypause();
            }
            musicplaypause();
        } else {
            i = 1;
        }
    }

    // 途中再生のままリロードした時に、MIDIの再生を最初に戻す処理
    MIDIjs.stop();
}


// 音楽の再生と一時停止の処理をする関数
function musicplaypause(){
    if(isloaded) {
        if(isPlay) {
            // 音楽停止の処理
            MIDIjs.pause();
            clearInterval(intervalId);
            isPlay = false;
            intervalId = null;

            // ボタンの処理
            playpauseButtonId.title = "クリックして再生";
            playpauseButtonId.style.color = "#000000";

            //背景色を元に戻す
            var before_td_colspan = document.getElementById(String(i-1)).getElementsByTagName('td');
            //奇数・偶数で役割分け
            if ((i-1)%2 == 1) {
                for (var j=5; j<before_td_colspan.length; j++){
                    before_td_colspan[j].style.backgroundColor = '#F5F5F5';
                }
            }

            else {
                for (var j=5; j<before_td_colspan.length; j++){
                    before_td_colspan[j].style.backgroundColor = '#FFFFFF';
                }
            }
        } 
        else {
            // 音楽再生の処理
            isPlay = true;

            // ボタンの処理
            playpauseButtonId.title = "クリックして一時停止";
            playpauseButtonId.style.color = "#0F8EAE";

            // 最初から再生か、途中から再生か
            if(isFirst) {
                // 最初から再生の場合
                isFirst = false;
                if (isAutoplay == '') {        // 最初から再生する場合は
                    i = 1;
                }
                MIDIjs.play('../static/week_audio/output_beats' + String(i) + '.mid');
            } else {
                // 途中から再生の場合
                MIDIjs.resume();
            }


            // スクロール関数
            const readnextline=()=>{
                if (i <= 1024) {
                    if (i > 1){
                        //背景色を元に戻す
                        var before_td_colspan = document.getElementById(String(i-1)).getElementsByTagName('td');
                        //奇数・偶数で役割分け
                        if ((i-1)%2 == 1) {
                            for (var j=5; j<before_td_colspan.length; j++){
                                before_td_colspan[j].style.backgroundColor = '#F5F5F5';
                            }
                        }

                        else {
                            for (var j=5; j<before_td_colspan.length; j++){
                                before_td_colspan[j].style.backgroundColor = '#FFFFFF';
                            }
                        }
                    }
                    
                    //背景色を変更
                    var now_td_colspan = document.getElementById(String(i)).getElementsByTagName('td');
                    for (var j=5; j<now_td_colspan.length; j++){
                        now_td_colspan[j].style.backgroundColor = '#FFC9D2';
                    }

                    // スライダーの処理
                    sliderlabelId.innerHTML="ID:" + i;     // スライダーラベルの書き換え
                    sliderId.value = i;
                    
                    // スクロール処理
                    speed = 60000 / Number(musicTableId.rows[i].cells[4].childNodes[0].textContent) * Number(musicTableId.rows[i].cells[4].childNodes[2].textContent);   //速さの取得
                    speed /= 0.995       // 音ズレ対策用
                    if (isAutoscroll) {
                        window.location.href = "\#" + String(i - 1);                // 1行スクロール
                    }

                    // 次の行の処理
                    i++;
                    intervalId = setTimeout(readnextline, speed);        // 次の行を読み込み

                } else {
                    // 最後まで再生が終わったら
                    MIDIjs.stop();
                    i = 1;
                }
            }

            // スクロール関数の最初の呼び出し
            intervalId = setTimeout(readnextline, speed);
        }
    }
}


// 音楽の停止に関する処理
function musicstop(){
    if (isloaded) {
        // 音階の停止とフラグの変更
        MIDIjs.stop();
        clearInterval(intervalId);
        isPlay = false;
        isFirst = true;
        intervalId = null;

        // ボタンの処理
        playpauseButtonId = document.getElementById('playpauseButton');
        playpauseButtonId.title = "クリックして再生"
        playpauseButtonId.style.color = "#000000";

        // スライダーの処理
        sliderId.value = 1;
        sliderlabelId.innerHTML="ID:1";

        if (i > 1) {
            //背景色を元に戻す
            var before_td_colspan = document.getElementById(String(i-1)).getElementsByTagName('td');
            //奇数・偶数で役割分け
            if ((i-1)%2 == 1) {
                for (var j=5; j<before_td_colspan.length; j++){
                    before_td_colspan[j].style.backgroundColor = '#F5F5F5';
                }
            }

            else {
                for (var j=5; j<before_td_colspan.length; j++){
                    before_td_colspan[j].style.backgroundColor = '#FFFFFF';
                }
            }
        }

        // スクロールの処理
        i = 1;
        isStoped = true;
        window.location.href = "\#0";
    }
}


// 自動スクロールするかどうかの切り替えする関数
function musicautoscroll(){
    if (isloaded) {
        autoscrollButtonId = document.getElementById('autoscrollButton');
        if (isAutoscroll) {
            // オートスクロールをしないのなら
            autoscrollButtonId.style.color = "#000000";
            autoscrollButtonId.title = "クリックして自動スクロールをオン"
            isAutoscroll = false;
        } else {
            // オートスクロールをするのなら
            autoscrollButtonId.style.color = "#0F8EAE";
            autoscrollButtonId.title = "クリックして自動スクロールをオフ"
            isAutoscroll = true;
        }
    }
}


// マウスホイールによる#musicTableのスクロール操作
window.onmousewheel = function(event){
    // スクロールの処理
    if (isloaded){
        if((event.wheelDelta > 0) && (i > 0)) {
            i--;
            window.location.href = "\#" + String(i); 
	    } else if ((event.wheelDelta < 0) && (i < 1024)) {
            i++;
            window.location.href = "\#" + String(i); 
	    }

        // スライダーの処理
        if (sliderlabelId != null) {
            sliderlabelId.innerHTML="ID:" + i;
            sliderId.value = i;
        }
    }
}


// スライダーによる#musicTableの操作
function target() {
    var beats = document.getElementById('slider').value;
    if (beats == 1) {
        window.location.href = "\#0";
        i = 0;
        sliderlabelId.innerHTML="ID:" + 1;
    } else {
        window.location.href = "\#" + String(beats);
        i = beats;
        sliderlabelId.innerHTML="ID:" + beats;
    }
}

// オンマウス再生
var before_note = "";
function onmouseplay(note) {
    note = note.replace("レb", "ド#");
    note = note.replace("ミb", "レ#");
    note = note.replace("ソb", "ファ#");
    note = note.replace("ラb", "ソ#");
    note = note.replace("シb", "ラ#");
    var JPNtoENGNoteDict = {"ド":"C", "レ":"D", "ミ":"E", "フ":"F", "ソ":"G", "ラ":"A", "シ":"B"};
    if ((note != null) && (note != "") && (note.slice(0, 1) != '「') && !(isPlay) && (before_note != note)) {
        MIDIjs.stop();
        var filename = "../static/audio/";
        var CDE = note.match("[ドレミフソラシ]");
        filename += JPNtoENGNoteDict[CDE[0]];
        if (note.indexOf('b') != -1) {
            filename += "b";
        }
        if (note.indexOf('#') != -1) {
            filename += "s";
        }
        var octave = note.slice(-1);
        filename += octave + ".mid";
        MIDIjs.play(filename);
        before_note = note;
    } else {
        if (before_note != note) {
            before_note = "";
        }
    }
}