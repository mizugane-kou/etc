
# https://discord.com/api/oauth2/authorize?client_id=XXXXXXXXXXXXXXXXX&permissions=294912&scope=bot 

import discord
from discord.ext import commands
from discord.ui import Button, View
import csv
import os
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import japanize_matplotlib
import random

# Botのトークンを入力してください
TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# JSTのタイムゾーンを定義
JST = timezone(timedelta(hours=9))

# CSVファイル名を指定
SLEEP_CSV_FILE = 'sleep_messages.csv'
WAKE_CSV_FILE = 'ansleep_messages.csv'

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

class SleepButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="寝る時間を記録", style=discord.ButtonStyle.primary, custom_id="sleep_button"))
        self.add_item(Button(label="起きる時間を記録", style=discord.ButtonStyle.success, custom_id="wake_button"))

class GraphButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="睡眠グラフを生成", style=discord.ButtonStyle.primary, custom_id="graph_button"))




def get_random_image(folder_path):
    """指定フォルダ内の画像をランダムに取得"""
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if images:
        return os.path.join(folder_path, random.choice(images))
    return None


@bot.event
async def on_ready():
    print(f'ログインしました: {bot.user}')
    
    img_folder = "img"  # 画像フォルダのパス
    
    # 全サーバーに対して対応するチャンネルに埋め込みメッセージを投稿
    for guild in bot.guilds:
        sleep_channel = discord.utils.get(guild.text_channels, name="寝起きの記録")
        if sleep_channel:
            embed = discord.Embed(
                title="睡眠記録",
                description="ボタンを押して寝る時間と起きる時間を記録してください。",
                color=0x00ff00
            )
            img_path = get_random_image(img_folder)
            if img_path:
                file = discord.File(img_path, filename="sleep_image.png")
                embed.set_image(url=f"attachment://sleep_image.png")
                await sleep_channel.send(embed=embed, view=SleepButtonView(), file=file)
            else:
                await sleep_channel.send(embed=embed, view=SleepButtonView())

        graph_channel = discord.utils.get(guild.text_channels, name="睡眠グラフ")
        if graph_channel:
            embed = discord.Embed(
                title="グラフ生成",
                description="ボタンを押して自分の睡眠記録のグラフを生成してください。",
                color=0x0000ff
            )
            img_path = get_random_image(img_folder)
            if img_path:
                file = discord.File(img_path, filename="graph_image.png")
                embed.set_image(url=f"attachment://graph_image.png")
                await graph_channel.send(embed=embed, view=GraphButtonView(), file=file)
            else:
                await graph_channel.send(embed=embed, view=GraphButtonView())


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.data["custom_id"] == "sleep_button":
        # 寝る時間を記録
        now = datetime.now(JST)
        author = interaction.user.name

        # CSVに記録
        with open(SLEEP_CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            if os.stat(SLEEP_CSV_FILE).st_size == 0:  # ファイルが空ならヘッダーを追加
                csv_writer.writerow(['Date', 'Author'])
            csv_writer.writerow([now.strftime('%Y-%m-%d %H:%M'), author])

        # 記録処理後の確認メッセージを現在のチャンネルにのみ送信
        await interaction.response.send_message(f"{author}さんの寝る時間を記録しました: {now.strftime('%Y-%m-%d %H:%M')}", ephemeral=True)

        # # 現在のチャンネルに埋め込みメッセージを再投稿
        # channel = interaction.channel
        # embed = discord.Embed(title="睡眠記録", description="ボタンを押して寝る時間と起きる時間を記録してください。", color=0x00ff00)
        # await channel.send(embed=embed, view=SleepButtonView())

    elif interaction.data["custom_id"] == "wake_button":
        # 起きる時間を記録
        now = datetime.now(JST)
        author = interaction.user.name

        # CSVに記録
        with open(WAKE_CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            if os.stat(WAKE_CSV_FILE).st_size == 0:  # ファイルが空ならヘッダーを追加
                csv_writer.writerow(['Date', 'Author'])
            csv_writer.writerow([now.strftime('%Y-%m-%d %H:%M'), author])

        # 記録処理後の確認メッセージを現在のチャンネルにのみ送信
        await interaction.response.send_message(f"{author}さんの起きる時間を記録しました: {now.strftime('%Y-%m-%d %H:%M')}", ephemeral=True)

        # # 現在のチャンネルに埋め込みメッセージを再投稿
        # channel = interaction.channel
        # embed = discord.Embed(title="睡眠記録", description="ボタンを押して寝る時間と起きる時間を記録してください。", color=0x00ff00)
        # await channel.send(embed=embed, view=SleepButtonView())

    elif interaction.data["custom_id"] == "graph_button":
        # 睡眠グラフを生成
        author = interaction.user.name
        graph_path = await generate_graph(author)

        if graph_path:
            with open(graph_path, 'rb') as f:
                picture = discord.File(f)
                await interaction.response.send_message(file=picture, ephemeral=True)
        else:
            await interaction.response.send_message("記録がありません。", ephemeral=True)


async def generate_graph(user_name):

    if not os.path.exists(SLEEP_CSV_FILE) or not os.path.exists(WAKE_CSV_FILE):
        return None

    sleep_dates, sleep_times = [], []
    wake_dates, wake_times = [], []
    sleep_hour_distribution = [0] * 24  # 睡眠時刻ごとの頻度
    wake_hour_distribution = [0] * 24  # 起床時刻ごとの頻度
    now = datetime.now(JST)
    four_months_ago = now - timedelta(days=150)

    # 睡眠データの読み込み
    with open(SLEEP_CSV_FILE, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # ヘッダーをスキップ
        for row in csv_reader:
            date = datetime.strptime(row[0], '%Y-%m-%d %H:%M').replace(tzinfo=JST)
            author = row[1]
            if four_months_ago <= date <= now and author == user_name:
                sleep_dates.append(date)
                sleep_hour = date.hour
                sleep_times.append(sleep_hour)
                sleep_hour_distribution[sleep_hour] += 1

    # 起床データの読み込み
    with open(WAKE_CSV_FILE, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # ヘッダーをスキップ
        for row in csv_reader:
            date = datetime.strptime(row[0], '%Y-%m-%d %H:%M').replace(tzinfo=JST)
            author = row[1]
            if four_months_ago <= date <= now and author == user_name:
                wake_dates.append(date)
                wake_hour = date.hour
                wake_times.append(wake_hour)
                wake_hour_distribution[wake_hour] += 1

    if not sleep_dates and not wake_dates:
        return None

    # グラフの設定と描画
    plt.figure(figsize=(20, 16))

    # 折れ線グラフ
    plt.subplot(2, 1, 1)
    # 睡眠データのプロット
    for i in range(1, len(sleep_dates)):
        if (sleep_times[i-1] >= 20 and sleep_times[i] <= 3) or (sleep_times[i-1] <= 3 and sleep_times[i] >= 20):
            line_color = '#a0abad'
        else:
            line_color = 'b'

        if (sleep_dates[i] - sleep_dates[i - 1]).days > 1:
            plt.plot(sleep_dates[i-1:i+1], sleep_times[i-1:i+1], marker='o', markersize=2, linestyle='None', color='b')
        else:
            plt.plot(sleep_dates[i-1:i+1], sleep_times[i-1:i+1], marker='o', markersize=2, linestyle='-', color=line_color, alpha=0.7)

    # 起床データのプロット（赤色）
    for i in range(1, len(wake_dates)):
        if (wake_times[i-1] >= 20 and wake_times[i] <= 3) or (wake_times[i-1] <= 3 and wake_times[i] >= 20):
            line_color = '#a0abad'
        else:
            line_color = 'r'

        if (wake_dates[i] - wake_dates[i - 1]).days > 1:
            plt.plot(wake_dates[i-1:i+1], wake_times[i-1:i+1], marker='o', markersize=2, linestyle='None', color='r')
        else:
            plt.plot(wake_dates[i-1:i+1], wake_times[i-1:i+1], marker='o', markersize=2, linestyle='-', color=line_color, alpha=0.7)

    two_weeks = timedelta(weeks=2)
    current_date = four_months_ago
    while current_date <= now:
        plt.axvline(current_date, color='lightcoral', linestyle='--', alpha=0.5)
        current_date += two_weeks

    plt.title(f'{user_name}さんの睡眠・起床周期記録グラフ')
    plt.ylabel('時刻（時）')
    plt.xticks(rotation=45)
    plt.xlim([four_months_ago, now])
    plt.ylim(0, 23)
    plt.gca().invert_yaxis()

    # ヒストグラム
    plt.subplot(2, 1, 2)
    hours = range(24)
    bar_width = 0.4  # 棒の幅
    plt.bar([h - bar_width / 2 for h in hours], sleep_hour_distribution, bar_width, color='skyblue', label='睡眠時刻', alpha=0.7)
    plt.bar([h + bar_width / 2 for h in hours], wake_hour_distribution, bar_width, color='salmon', label='起床時刻', alpha=0.7)
    plt.xticks(hours)
    plt.xlabel('時刻（時）')
    plt.ylabel('頻度')
    plt.title(f'{user_name}さんの睡眠・起床時刻の分布')
    plt.legend()

    # グラフ間の余白設定
    plt.subplots_adjust(hspace=0.4, top=0.95, bottom=0.05, left=0.05, right=0.95)

    # グラフを保存
    graph_path = f"{user_name}_combined_sleep_wake_graph.png"
    plt.savefig(graph_path)
    plt.close()
    return graph_path





bot.run(TOKEN)
