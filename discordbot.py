# discord.py の読み込み
import discord
import random

TOKEN = 'NTgyNDc1MTg3NDUxMzMwNTgw.XOuWoQ.6jV2cYi_0isAYj5AfhaTxv918L8'
MEGAMI_LIST =["刀","扇","銃","薙","忍","書","傘","槌","毒","枢","騎","爪","鎌","旗","橇","鏡","古","琵","炎","笛","戦","絆","塵","拒","経","機"]

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
            m = f'おはよーございます{message.author.name}さん！'
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
    # ダイス
    if message.content == "/y dice":
        if client.user != message.author:
            result = random.randint(1,6)
            m = f'{str(result)}の目が出ました。6面ダイスですよ'
            await send_channel(m)

    #--- ふるよに機能 ---
    #メガミ選択
    if message.content.startswith("/y megami"):
        if client.user != message.author:
            if message.content == "/y megami":
                m = f'{random.choice(MEGAMI_LIST)}とかどうでしょう'
                await send_channel(m)

    #リプ処理
    if client.user in message.mentions:
        #　ヘルプ
        if "help" in message.content:
            ms = f'{client.user.name}のことを知りたいのですね\n先行後攻などランダム要素がほしい時にお手伝いさせていただきます。\n使い方: /y [command]\nコマンド一覧：\n@{client.user.name} help  使い方やコマンド一覧を表示します\n/y turn                   先行後攻を決めます\nこんな感じです'
            await send_channel(ms)
        else:
            reply  = f'{message.author.mention} はいはいー 使い方知りたければhelpでメンションくださーい'
            await send_channel(reply)


client.run(TOKEN)