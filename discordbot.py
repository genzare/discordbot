# discord.py の読み込み
import discord
import random
import numpy as np
from parse import *
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# 辞書オブジェクト。認証に必要な情報をHerokuの環境変数から呼び出している
credential = {
                "type": "service_account",
                "project_id": os.environ['SHEET_PROJECT_ID'],
                "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
                "private_key": os.environ['SHEET_PRIVATE_KEY'],
                "client_email": os.environ['SHEET_CLIENT_EMAIL'],
                "client_id": os.environ['SHEET_CLIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
             }
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential, scope)
gc = gspread.authorize(credentials)
wks = gc.open('fairyCircle').sheet1
wks.update_acell('A1', '隠蔽工作です！')
print(wks.acell('A1'))

TOKEN = os.environ["DISCORD_TOKEN"]
MEGAMI_LIST =["刀","扇","銃","薙","忍","書","傘","槌","毒","枢","騎","爪","鎌","旗","橇","鏡","古","琵","炎","笛","戦","絆","塵","拒","経","機"]
FE0SYMBOL_LIST = ["光の剣","聖痕","暗夜","白夜","メダリオン","聖戦旗","神器","シンボルなし"]

#接続に必要なオブジェクト生成
client = discord.Client()

#起動時の動作処理
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("おはよーございます！")
    print('------')

@client.event
async def on_message(message):
    #メッセージ送信部
    async def send_channel(sendms):
        await message.channel.send(sendms)
    # 「おはよう」で始まるか調べる
    if message.content.startswith("おはよう"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージを書きます
            m = f'おはよーございます！{message.author.name}さん！'
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await send_channel(m)
    # 先行後攻ぎめ
    if message.content.startswith("/y turn"):
        if client.user != message.author:
            if random.random()<0.5:
                m = f'{message.author.name}さんが先行です。'
            else:
                m = f'{message.author.name}さんが後攻です。'
            await send_channel(m)
    # ダイス一個ふる
    def roll_dice(dice_size):
        num = np.random.randint(1,int(dice_size))
        return num
    # ダイス結果をテキストで
    def get_diceresult(dice_size,dice_num):
        dice_val = np.array([],dtype=np.int64)
        for i in range(dice_num):
            dice_val =np.append(dice_val, roll_dice(dice_size))
        ms = str(np.sum(dice_val)) + ' = ' + str(dice_val) 
        return ms
    # ダイス
    if message.content == "/y dice":
        if client.user != message.author:
            result = roll_dice(6)
            m = f'{str(result)}の目が出ました。6面ダイスですよ'
            await send_channel(m)
     #複数ダイス
    elif message.content.startswith("/y dice"):
        if client.user != message.author:
            info = parse('/y dice {}d{}',message.content)
            dice_num = int(info[0])
            dice_size = int(info[1])
            if dice_num >= 500:
                m = "おいふざけるなよその個数"
                await send_channel(m)
            if (dice_num<500 and dice_num >= 100):
                m = "そんなに何個も振れないです..."
                await send_channel(m)
            if dice_num <100:
                m = get_diceresult(dice_size,dice_num)
                await send_channel(m)
    #--- ふるよに機能 ---
    #メガミ選択
    if message.content.startswith("/y megami"):
        if client.user != message.author:
            if message.content == "/y megami":
                megami_num = 1 
            else:
                info = parse('/y megami{}',message.content)
                megami_num = int(info[0])
            if megami_num <= len(MEGAMI_LIST):
                megami_result = '.'.join(random.sample(MEGAMI_LIST,megami_num))
                m = f'{megami_result}とかどうでしょう'
                await send_channel(m)
            else:
                m = f'現在のメガミの総数は{len(MEGAMI_LIST)}柱です。更新不足ですか・・・？'
                await send_channel(m)
    #---サイファ機能----
    #おすすめデッキ
    if message.content == "/y fedeck":
        if client.user != message.author:
            deck_result = random.choice(FE0SYMBOL_LIST)
            m = f'{deck_result}のカードが入ったデッキとかオススメでーす！'
            await send_channel(m)

    #リプ処理
    if client.user in message.mentions:
        #　ヘルプ
        if "help" in message.content:
            m = f'{client.user.name}のことを知りたいのですね\n先行後攻などランダム要素がほしい時にお手伝いさせていただきます。\n\nコマンド一覧：\n@{client.user.name} help  使い方やコマンド一覧を表示します\n/y turn                   先行後攻を決めます\n/y dice                   6面ダイスを振ります\n/y dice <number>d<number> <number>d<number>のダイスを振ります\n~ふるよに用~\n/y megami                 メガミを一柱選びます\n/y megami<number>         メガミを<number>柱選びます\n\n~サイファ用~\n/y fedeck                 オススメデッキ\nこんな感じです'
            await send_channel(m)
        else:
            m = f'{message.author.mention} はいはいー 使い方知りたければhelpでメンションくださーい'
            await send_channel(m)
   
        


client.run(TOKEN)