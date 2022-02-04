# 新しいDB

from typing import DefaultDict
from django.db import models
from django.contrib.auth.models import User                     # ユーザー認証
from datetime import datetime, timezone, timedelta
from django.core.validators import FileExtensionValidator


class Information(models.Model) :
    date = models.DateTimeField(default = datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=9))))       # Soundが作られた日時を保存
    title = models.CharField(max_length=100, default="")        # 曲のタイトル


class Sound(models.Model) :
    beats = models.IntegerField(default = 0)                    # 何行目か(idとは違い、毎週1024づつ増える)
    bpm = models.IntegerField(default = 120)                    # 曲の速さ(Beats par minutes)
    length = models.FloatField(default = 1)                     # 音の長さ(ビート長)
    speed = models.IntegerField(default = 120)                  # スクロールする速さ
    comment = models.BooleanField(default = False)              # コメントがあるかどうか
    track1 = models.CharField(max_length = 20, default = "")     # 音階
    track2 = models.CharField(max_length = 20, default = "")
    track3 = models.CharField(max_length = 20, default = "")
    track4 = models.CharField(max_length = 20, default = "")
    track5 = models.CharField(max_length = 20, default = "")
    track5 = models.CharField(max_length = 20, default = "")
    track6 = models.CharField(max_length = 20, default = "")
    track7 = models.CharField(max_length = 20, default = "")
    track8 = models.CharField(max_length = 20, default = "")
    track9 = models.CharField(max_length = 20, default = "")


class Account(models.Model):                                    # ユーザーアカウントのモデルクラス
    user = models.OneToOneField(User, on_delete=models.CASCADE) # ユーザー認証のインスタンス
    edited = models.IntegerField(default = 0)                   # 編集した
    
    def __str__(self):
        return self.user.username


class Chat(models.Model) :
    sound = models.ForeignKey(Sound, null= True, on_delete=models.SET_NULL)     # beatsを参照するための外部キー
    chatuser = models.ForeignKey(User, null= True, unique=False, on_delete=models.CASCADE)           # ユーザー認証のインスタンス
    guest = models.CharField(null= True, max_length = 6, default="")           # ユーザー認証のインスタンス
    text = models.CharField(max_length = 500, default="")       # チャット本文
    time = models.DateTimeField(default = datetime.now())


class Midi(models.Model):
    filename = models.CharField(max_length = 25, default = "")
    attach = models.FileField(      # generateMIDI()で作ったMIDIファイルを保存し、列挙する
        null=True,
        blank=True,
        upload_to='midi/',
        verbose_name='midiファイル',
        validators=[FileExtensionValidator(['mid'])],
    )