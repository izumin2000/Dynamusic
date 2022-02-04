var inputTextLen, inputBeats
var IsTextOK = true, IsBeatsOK = true;
var chatSubmit

window.onload = function(){
    var soundEditorId = document.getElementById("chatForm");
    soundEditorId.style.display = "block";

    chatSubmit = document.getElementById("submitButton");
    chatSubmit.disabled = true;
}


function checkChatForm() {
    inputTextLen = document.getElementById("formChatText").value.length;
    chatSubmit.color = "#fff";

    if (inputTextLen <= 500) {
        IsTextOK = true;
        document.getElementById("chat-error").innerHTML = '';
    } else {
        IsTextOK = false;
        document.getElementById("chat-error").innerHTML = "1文字～500文字までの文章を入力してください";
    }

    inputBeats = Number(document.getElementById("formChatBeat").value);
    if ((0 <= inputBeats && inputBeats <= 1024) && inputTextLen > 0) {
        IsBeatsOK = true;
        document.getElementById("chat-error").innerHTML = '';
    } else if (inputTextLen == 0) {
        IsBeatsOK = false;
        document.getElementById("chat-error").innerHTML = "チャットを入力してください。";
    } else {
        IsBeatsOK = false;
        document.getElementById("chat-error").innerHTML = "1～1024の半角数字を入力してください";
    }

    if ([IsTextOK, IsBeatsOK].every(value => { return value })) {
        chatSubmit.disabled = false;
        chatSubmit.style.color = '#0F8EAE';
    } else {
        chatSubmit.disabled = true;
        chatSubmit.style.color = '#0F8EAE80';
    }
}