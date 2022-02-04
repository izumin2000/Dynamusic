var inputSpeed, inputTrack, inputNote, inputLength
var IsSpeedOK = true, IsTruckOK = true, IsNoteOK = true, IsLengthOK = true;

window.onload = function(){
    var soundEditorId = document.getElementById("soundEditor");
    soundEditorId.style.display = "block";
}

function checkSoundForm() {
    inputSpeed = Number(document.getElementById("input-speed").value);
    if ((20 <= inputSpeed && inputSpeed <= 999) || inputSpeed == '') {
        IsSpeedOK = true;
        document.getElementById("speed-error").innerHTML = '';
    } else {
        IsSpeedOK = false;
        document.getElementById("speed-error").innerHTML = "20～999の半角数字を入力してください";
    }
    
    inputTrack = Number(document.getElementById("input-track").value);
    if ((1 <= inputTrack && inputTrack <= 9) || inputTrack == '') {
        IsTruckOK = true;
        document.getElementById("track-error").innerHTML = '';
    } else {
        IsTruckOK = false;
        document.getElementById("track-error").innerHTML = "1～9の半角数字を入力してください";
    }

    inputNote = document.getElementById( "input-note" ).value;
    if (inputNote.length <= 10) {
        IsNoteOK = true;
        document.getElementById("note-error").innerHTML = '';
    } else {
        IsNoteOK = false;
        document.getElementById("note-error").innerHTML = "10文字以内の文字を入力してください";
    }
    
    inputLength = Number(document.getElementById( "input-rows" ).value);
    if ((1 <= inputLength && inputLength <= 16) || inputLength == '') {
        IsLengthOK = true;
        document.getElementById("rows-error").innerHTML = '';
    } else {
        IsLengthOK = false;
        document.getElementById("rows-error").innerHTML = "1～16の半角数字を入力してください";
    }

    var inputSubmit = document.getElementById("submitButton");
    if ([IsLengthOK, IsNoteOK, IsSpeedOK, IsTruckOK].every(value => { return value })) {
        if (inputNote == 'error') {     // デバック用
            document.getElementById("sound-error").innerHTML = "デバック用エラーです";
            inputSubmit.disabled = true;
            inputSubmit.style.color = '#0F8EAE80';
        } else {
            document.getElementById("sound-error").innerHTML = "";
            inputSubmit.disabled = false;
            inputSubmit.style.color = '#0F8EAE';
        }
    } else {
        document.getElementById("sound-error").innerHTML = "エラーが発生しているため、送信することができません。";
        inputSubmit.disabled = true;
        inputSubmit.style.color = '#0F8EAE80';
    }
}