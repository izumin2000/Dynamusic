from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.http import request, response
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import Midi, Sound, Chat, Account, Information
from . import forms
import datetime
import pretty_midi
import random

NUMBER_OF_ROWS = 1024
NUMBER_OF_TRACKS = 10
MIN_SPEED = 20
MAX_SPEED = 999
MAX_COMMENT_LENGTH = 50
SCORE_CHAR_MAP = "/CDEFGABドレミファソラシド#b1234567890"
NOTE_STRING_MAP = "CDEFGABドレミファソラシド"
ENG_NOTE_STRING_MAP = "CDEFGAB"
JPN_NOTE_STRING_MAP = "ドレミファソラシド"
JPN_NOTE_STRING_LIST = ["ド", "レ", "ミ", "ファ", "ソ", "ラ", "シ", "ド"]
ENGtoJPN_NOTE_MAP = {"C": "ド", "D": "レ", "E": "ミ", "F": "ファ", "G": "ソ", "A": "ラ", "B": "シ"}
LENGRH_MAP = [0.25, 0.5, 1.0, 2.0, 4.0]


def tracksToList(sound) :
    return [sound.track1, sound.track2, sound.track3, sound.track4, sound.track5, sound.track6, sound.track7, sound.track8, sound.track9]


def tracksToListI(sound, i) :
    return tracksToList(sound)[int(i) - 1]


def getEndOfBeats() :
    beats = NUMBER_OF_ROWS + 1
    for row in Sound.objects.all()[::-1] :
        noteset = set(tracksToList(row))
        beats -= 1
        if len(noteset) - 1 :
            return beats + 1


def getHeadId() :
    if not(len(Sound.objects.all())) :
        return 1
    for head in Sound.objects.all() :
        return head.id


def Id_to_beats(id) :
    id += 1
    if (id % NUMBER_OF_ROWS) == 0 :
        beats = NUMBER_OF_ROWS
    else :
        beats = id % NUMBER_OF_ROWS

    return beats


# 任意のテキストから日本語の音階かコメントアウトを生成する関数
def textToNote(text) :
    if text == "" :
        return ""
    if text[0] == "#" :
        return f"「{text}」"
    if len(text) <= 5 :
        if len(set(text) - set(SCORE_CHAR_MAP)) == 0 :
            note = ""               # 書式に従った音階note
            if "/" in text :        # 音を区切り文字を含む場合は
                note += "/"
                text.replace("/", "")
            notetemp = (set(text) & set(NOTE_STRING_MAP)) - set("ァ")       # textに含まれてる音階を抽出
            if len(notetemp) != 1 :      # 音階が1つでなければ
                return f"「{text}」"
            else :
                notetemp = notetemp.pop()
                if notetemp in ENG_NOTE_STRING_MAP :            # 音階が英語表記なら
                    notetemp = ENGtoJPN_NOTE_MAP[notetemp]      # 日本語表記にする
                elif notetemp == "フ" :
                    notetemp = "ファ"
                note += notetemp
            sharpCount = text.count("#")        # シャープの数をカウント
            flatCount = text.count("b")         # フラットの数をカウント
            if (sharpCount == 1) and (flatCount == 0) :
                note += "#"
            elif (sharpCount == 0) and (flatCount == 1) :
                note += "b"
            elif (sharpCount != 0) and (flatCount != 0) :
                return f"「{text}」"
            notetemp = (set(text) & set("1234567890"))      # textに含まれている数字を抽出
            if (len(notetemp) == 0) :
                note += "4"
            elif (len(notetemp) >= 2) :           # 数字が2つ以上ならば
                return f"「{text}」"
            else :
                notetemp = notetemp.pop()
                note += notetemp
            note = note.replace("ミ#", "ファ")
            note = note.replace("ファb", "ミ")
            note = note.replace("シ#", "ド")
            note = note.replace("ドb", "シ")
            return note
        else :
            return f"「{text}」"
    else :
        return f"「{text}」"


# Sound DBからmidiを生成する関数
def generateMIDI(beats, isWeekMIDI) :
    piano_c_chord = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)

    if (beats == getHeadId()) or (beats == getHeadId() + 1) :       # 最初から再生の場合
        notelist = ["-1"] * NUMBER_OF_TRACKS            # 何も音階を入れない
    else :
        sound = Sound.objects.get(pk = beats - 2)       # 再生する行の手前を登録
        notelist = tracksToList(sound)
    lengthlist = [0] * NUMBER_OF_TRACKS               # 各音が費やす音階をトラックごとのリストで保存
    now = 0.25       # 音ズレ防止用
    start = beats - getHeadId() - 1
    if start < 0 :
        start = 0
    for row in Sound.objects.all()[start:getEndOfBeats()]:
        beforenotelist = notelist                       # 前の音階と比べる変数
        length = 60 * row.length / row.speed            # その行に費やす速さを計算
        notelist = tracksToList(row)

        i = 0                                           # トラック1から見る
        for note in notelist :
            lengthlist[i] += length                     # length分noteの音価を増やす
            if note == "" :                             # 音階が空白なら
                i += 1
                continue
            if note[0] == '「' :                        # 音階がコメントなら
                i += 1
                continue
            if note == beforenotelist[i] :              # 前の音階と同じならば
                if note[0] != '/' :                     # 最初の文字がスラッシュでなければ
                    i += 1
                    continue

            # 日本語音階から英語音階に変換
            if "フ" in set(note) :
                JPNnote = "ファ"
            else :
                JPNnote = set(note) & set(JPN_NOTE_STRING_LIST)       # textに含まれてる音階を抽出
                JPNnote = JPNnote.pop()
            notetemp = JPN_NOTE_STRING_LIST.index(JPNnote)
            note = note.replace(JPNnote, ENG_NOTE_STRING_MAP[notetemp]).replace("/", "")
            # try :
            note_number = pretty_midi.note_name_to_number(note)
            # volume = 120 - (min(60, note_number) * 0.5)
            # except :
            # print("The text", note, "is not note!")
            note = pretty_midi.Note(velocity = 96, pitch = note_number, start = now, end = now + lengthlist[i])
            piano.notes.append(note)

            i += 1
            lengthlist[i] = 0
        now += length

    piano_c_chord.instruments.append(piano)
    if isWeekMIDI :
        piano_c_chord.write(f"Dynamusic/static/week_audio/{datetime.date.today()}.mid")
    else :
        if (beats - getHeadId()) == 0 :
            beats += 1
        piano_c_chord.write(f"Dynamusic/static/week_audio/output_beats{beats - getHeadId()}.mid")


# Sound DBの初期化
def initsound(request):
    Sound.objects.all().delete()
    soundL = []
    for i in range(NUMBER_OF_ROWS) :
        soundL.append(Sound(beats = Id_to_beats(i)))
    Sound.objects.bulk_create(soundL)
    sounds = Sound.objects.all()
    changelogs = ["デバック：Sound DBを初期化しました"]
    soundDict = {'sounds' : sounds, 'changelogs' : changelogs}
    return render(request, 'Dynamusic/index.html', soundDict)


# Chat DBの初期化
def initchat(request) :
    chats = Chat.objects.all().delete()
    title = "デバック：チャットを全て削除しました"
    chatsDict = {'title':title, 'chats': chats}

    return render(request, 'Dynamusic/chat.html', chatsDict)


# DBの初期化に関する関数
def checkInit(request, lastView, isInitDB):
    lastView += datetime.timedelta(hours=9)     # ！！！何故か世界標準時になるので9時間足す！！！
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    now = datetime.datetime.now(JST)
    if (lastView.weekday() > now.weekday()) :       # 一週間経ったら
        initsound(request)
        initchat(request)
        generateMIDI(getHeadId(), True)     # 日付の名前付きのMIDIを生成
        Midi.objects.create(attach = f"Dynamusic/static/week_audio/{datetime.date.today()}.mid", filename = str(datetime.date.today()))

    if isInitDB :
        initsound(request)
        initchat(request)

    # 最後の閲覧日時を更新
    InformationSingleton = Information.objects.get(pk = 1)
    InformationSingleton.date = now
    InformationSingleton.save()


# index画面に関する関数
def index(request):
    if len(Information.objects.all()) :
        isInitDB = False
        generateMIDI(getHeadId(), False)
    else :          # DB本体を初期化したら
        JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        now = datetime.datetime.now(JST)
        Information.objects.create(date = now)        # Informationのレコード(シングルトン)を作成
        isInitDB = True
        generateMIDI(1, False)
        Midi.objects.create(attach = f"Dynamusic/static/week_audio/2021-01-10.mid", filename = "2021-01-10")
        Midi.objects.create(attach = f"Dynamusic/static/week_audio/2021-01-17.mid", filename = "2021-01-17")

    lastView = Information.objects.get(pk = 1).date
    checkInit(request, lastView, isInitDB)


    # get()メソッドは第1引数のキーの値を取得しますが、第2引数にはそのキーが存在しなかった場合のデフォルト値を指定することが出来ます。
    # 実際に送信されている値は(isFirst - 1)のことに気を付ける
    isFirst = request.COOKIES.get('isFirst', True)

    sounds = Sound.objects.all()
    soundDict = {'sounds' : sounds, 'autoscroll' : 0, 'autoplay' : '', "isFirst" : isFirst}
    response = render(request, 'Dynamusic/index.html', soundDict)

    max_age = 60 * 60 * 24
    response.set_cookie('isFirst', False, max_age=max_age)

    return response


# 自動再生する関数
def autoplay(request, beats):
    sounds = Sound.objects.all()
    generateMIDI(beats + getHeadId(), False)
    soundDict = {'sounds' : sounds, 'autoscroll' : beats, 'autoplay' : beats}
    return render(request, 'Dynamusic/index.html', soundDict)


# Soundテーブルを編集したり、edit画面を呼び出す関数
def edit(request, beats) :
    sound_id = getHeadId() + beats - 1
    sounds = Sound.objects.all()
    editedSound = Sound.objects.get(pk = sound_id)

    # 編集する行の前後2行を表示する前後
    previewSound = []
    tableWidth = 0
    if (sound_id <= getHeadId() + 2) :
        for previewSoundID in range(getHeadId(), getHeadId() + 5) :
            sound = Sound.objects.get(pk = previewSoundID)
            tableWidth += max(list(map(len, tracksToList(sound))))
            previewSound.append(sound)
    elif (getHeadId() + NUMBER_OF_ROWS - 2 <= sound_id) :
        for previewSoundID in range(getHeadId() + NUMBER_OF_ROWS - 5, getHeadId() + NUMBER_OF_ROWS) :
            sound = Sound.objects.get(pk = previewSoundID)
            tableWidth += max(list(map(len, tracksToList(sound))))
            previewSound.append(sound)
    else :
        for previewSoundID in range(sound_id - 2, sound_id + 3) :
            sound = Sound.objects.get(pk = previewSoundID)
            tableWidth += max(list(map(len, tracksToList(sound))))
            previewSound.append(sound)

    if tableWidth >= 32 :
        if (beats == 1) or (beats == 2)  :
            previewSound.pop(4)
            previewSound.pop(3)
        elif (beats == NUMBER_OF_ROWS - 1) or (beats == NUMBER_OF_ROWS) :
            previewSound.pop(0)
            previewSound.pop(0)
        else :
            previewSound.pop(4)
            previewSound.pop(0)
    changelogs = []
    problemlogs = []

    if request.method == 'POST':

        # フォームから読み取る
        newTrack = request.POST['input-track']
        newNote = request.POST['input-note']
        newLength = request.POST.get('input-length')
        newSpeed = request.POST['input-speed']
        newrows = request.POST['input-rows']

        newNote = textToNote(newNote)

        if newTrack == '' :
            newTrack = 1

        if newrows == '' :
            newrows = 1

        # DBへ登録する
        if (newLength != None) :
            editedSound.length = LENGRH_MAP[int(newLength)]
            changelogs.append(f"ビート{beats} の音の長さをを{newLength}にしました")
            editedSound.save()

        if newTrack != '' :     # トラックが空白でなければ
            endOfEditedSpeed = 0
            beforeNote = tracksToListI(editedSound, newTrack)
            if (newNote == "") and (newLength == None) and (newSpeed == "") :      # 空白なら音階をnewrows行削除する(連続していて同じ音階である行のみ)
                for i in range(sound_id, min(sound_id + int(newrows), getHeadId() + NUMBER_OF_ROWS)) :
                    editedSound = Sound.objects.get(pk = i)
                    if tracksToListI(editedSound, newTrack) == beforeNote :
                        setattr(editedSound, f"track{newTrack}", '')       # editedSound.trackXX = ''
                        editedSound.save()
                        endOfEditedSpeed = i - getHeadId() + 1
                    else :
                        problemlogs.append(f"ビート{endOfEditedSpeed + 1} トラック{newTrack}の音は削除した音{beforeNote}と違うため、ビート{endOfEditedSpeed + 1}~{beats + int(newrows) - 1}の音は削除しませんでした")
                        break
                if beats == endOfEditedSpeed :
                    changelogs.append(f"ビート{beats} トラック{newTrack}の音を削除しました")
                else :
                    changelogs.append(f"ビート{beats}~{endOfEditedSpeed} トラック{newTrack}の音を削除しました")

            elif newNote != "" :      # 音階が入力されたのなら音階をnewrows行追加する(連続していて同じ音階である行のみ)
                for i in range(sound_id, min(sound_id + int(newrows), getHeadId() + NUMBER_OF_ROWS)) :
                    setattr(editedSound, f"track{newTrack}", newNote)
                    editedSound = Sound.objects.get(pk = i)
                    if tracksToListI(editedSound, newTrack) in [beforeNote, ''] :
                        setattr(editedSound, f"track{newTrack}", newNote)         # editedSound.trackXX = newNote
                        editedSound.save()
                        endOfEditedSpeed = i - getHeadId() + 1
                    else :
                        if (beforeNote == "") :
                            problemlogs.append(f"ビート{endOfEditedSpeed + 1} トラック{newTrack}の音は追加した音{beforeNote}と違うため、ビート{endOfEditedSpeed + 1}~{beats + int(newrows) - 1}は音を追加しませんでした")
                        else :
                            problemlogs.append(f"ビート{endOfEditedSpeed + 1} トラック{newTrack}の音は変更した音{beforeNote}と違うため、ビート{endOfEditedSpeed + 1}~{beats + int(newrows) - 1}は音を変更しませんでした")
                        break
                if beats == endOfEditedSpeed :
                    if beforeNote == "":
                        changelogs.append(f"ビート{beats} トラック{newTrack}に音{newNote}を追加しました")
                    else :
                        changelogs.append(f"ビート{beats} トラック{newTrack}を音{newNote}に変更しました")

                else :
                    if beforeNote == "":
                        changelogs.append(f"ビート{beats}~{endOfEditedSpeed} トラック{newTrack}に音{newNote}を追加しました")
                    else :
                        changelogs.append(f"ビート{beats}~{endOfEditedSpeed} トラック{newTrack}を音{newNote}に変更しました")


        if newSpeed != "":       # 速さが空白で無いのなら
            beforeSpeed = editedSound.speed
            editedSound.speed = newSpeed
            editedSpeedList = []
            endOfEditedSpeed = 0
            for i in range(getHeadId(), getHeadId() + NUMBER_OF_ROWS) :
                editedSound = Sound.objects.get(pk = i)
                if i >= sound_id :
                    if beforeSpeed == editedSound.speed:      # 編集した行の次が同じなら続けて次の行を編集
                        editedSound.speed = newSpeed
                        endOfEditedSpeed = i
                    else :
                        break
                editedSpeedList.append(editedSound)
            Sound.objects.bulk_update(editedSpeedList, fields=["speed"])
            newTrack = None
            if endOfEditedSpeed == sound_id :      # 編集した行が1行なら
                changelogs.append(f"ビート{beats}の速さを{newSpeed}にしました")
            else :      # 編集した行が複数行なら
                changelogs.append(f"ビート{beats}~{endOfEditedSpeed}の速さを{newSpeed}にしました")
        editedSound.save()

        sounds = Sound.objects.all()
        generateMIDI(getHeadId(), False)        # MIDIを生成
        data = {'sounds' : sounds, 'changelogs' : changelogs, 'problemlogs' : problemlogs, 'autoscroll' : beats, 'editedtrack' : newTrack, 'editedbeatsEnd' : endOfEditedSpeed}
        return render(request, "Dynamusic/index.html", data)     # indexへ画面を遷移

    data = {'sounds' : previewSound, 'editedSound' : editedSound}
    return render(request, "Dynamusic/edit.html", data)     # editからの画面遷移以外のindex画面の読み込み


def chat(request) :
    guestName = request.COOKIES.get('guestName', "")        # ゲストネームを取得or生成
    guestNameLength = random.randint(3, 7)
    i = 0
    if guestName == "" :
        while i < guestNameLength :
            c = random.randint(ord('A'), ord('Z'))
            """
            c = random.randint(ord('ぁ'), ord('ヴ'))      #ゲストユーザーを日本語表記にする
            if (ord('ゕ') <= c) and (c <= ord("゠")) :
                continue
            """
            guestName += chr(c)
            i += 1

    if request.method == 'POST':
        newChat =request.POST['formChatText']
        newBeats = request.POST.get('formChatBeat')    # request.POST['formChatBeat']と同じ。formChatBeatに何も書かなかった場合Noneを返す。
        if newBeats :
            newSound = Sound.objects.get(pk = int(newBeats) + getHeadId() - 1)
            newSound.comment = True
            newSound.save()
        else :
            newSound = None
        if request.user.is_authenticated :
            newUser = User.objects.get(pk= request.user.id)
            newGuest = None
        else :
            newUser = None
            newGuest = guestName
        now = datetime.datetime.now()
        Chat.objects.create(sound = newSound, text = newChat, time = now, chatuser = newUser, guest = newGuest)
    chats = Chat.objects.all()

    title = "チャット"
    chatsDict = {'title':title, 'chats': chats, 'displayedName': guestName}

    response = render(request, 'Dynamusic/chat.html', chatsDict)
    max_age = 60 * 60 * 24
    response.set_cookie('guestName', guestName, max_age=max_age)

    return response


# indexからchatのbeatsへのリンクするための関数
def chatbeats(request, beats) :
    title = f"ビート{beats}の検索結果"
    chats = Chat.objects.filter(sound_id = beats + getHeadId() - 1)
    chatsDict = {'title':title, 'chats': chats}
    return render(request, 'Dynamusic/chat.html', chatsDict)


# chatからindexのbeatsへのリンクするための関数
def tobeats(request, beats) :
    sounds = Sound.objects.all()
    data = {'sounds' : sounds,  'autoscroll' : beats}
    return render(request, "Dynamusic/index.html", data)     # indexへ画面を遷移


def doc(request) :
    return render(request, 'Dynamusic/doc.html')


def midis(request) :
    generateMIDI(getHeadId(), True)
    week_midi = {"week_midi" : Midi.objects.all()[::-1], "today" : datetime.date.today().strftime("%Y-%m-%d")}
    return render(request, 'Dynamusic/midis.html', week_midi)


def terms(request) :
    return render(request, 'Dynamusic/terms.html')

# myapp/views.py
class Login(LoginView):
    form_class = forms.LoginForm
    template_name = "Dynamusic/login.html"


class Logout(LogoutView):
    template_name = "Dynamusic/index.html"


class UserCreateView(FormView):
    form_class = forms.SignUpForm
    template_name = 'Dynamusic/create.html'
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        if self.request.POST['next'] == '確認':
            return render(self.request, 'Dynamusic/create_confirm.html', {'form': form })
        elif self.request.POST['next'] == '戻る':
            return render(self.request, 'Dynamusic/create.html', {'form': form})
        elif self.request.POST['next'] == '作成':
            form.save()
            # 認証
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            # ログイン
            login(self.request, user)
            #userさんの作成番号表示
            Account.objects.create(user=self.request.user)
            return super().form_valid(form)
        else:
            # 通常このルートは通らない
            return redirect(reverse_lazy('index'))