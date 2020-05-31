from __future__ import unicode_literals
import discord
from discord.voice_client import VoiceClient
import urllib
from bs4 import BeautifulSoup
import youtube_dl
import string
import random
import time
import asyncio
import os
import shutil
import sys
import subprocess

client = discord.Client()

PATH = os.path.dirname(os.path.abspath(__file__))

class VideoInfo:
    title = ""
    path = ""
    def __init__(self, title, path):
        self.title = title
        self.path = path

class SearchResult:
    title = ""
    link = ""
    def __init__(self, title, link):
        self.title = title
        self.link = link

Q = []
SR = []

ignore = False

flag = True
class AsyncPlayer:
    vc : VoiceClient
    def __init__(self, vc_):
        self.vc = vc_
    async def start(self):
        while True:
            if self.vc.is_playing() is False and len(Q) != 0:
                if flag:
                    flag = False
                else:
                    Q.pop(0)
                self.vc.play(discord.FFmpegPCMAudio(Q[0].path))
            time.sleep(1)
    def __del__(self):
        pass

def ClearYoutubeDL():
    path = os.path.join(PATH, "youtubedl")
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    print("Cleared folder [youtubedl]")

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")
    game = discord.Game("!명령어")
    await client.change_presence(status=discord.Status.online, activity=game)
    ClearYoutubeDL()

@client.event
async def on_message(message):
    global ignore
    if ignore == True and message.author.id != 351677960270381058:
        return
    if message.content.startswith("!") and message.content.startswith("!!") is False:
        print("[", end='')
        print(message.author, end="] ")
        print(message.content)
        if message.content == "!명령어":
            await message.channel.send("```\n"
                                       "[봇 명령어]\n\n"
                                       "[!관리자] : 관리자만.\n"
                                       "[!명령어] : 봇의 명령어를 보여줍니다.\n"
                                       "[!안녕] : 봇에게 인사합니다.\n"
                                       "[!아침] : 봇이 아침인사를 합니다.\n"
                                       "[!노예야] : 노예를 부릅니다.\n"
                                       "[!말해라 [말]] : 봇이 하고 싶은 말을 해줍니다.\n"
                                       "[!레식전적 [닉네임]] : 레식 전적을 보여줍니다.\n"
                                       "[!롤전적 [닉네임]] : 롤 전적을 보여줍니다.\n"
                                       "[!롤체전적 [닉네임]] : 롤체 전적을 보여줍니다.\n"
                                       "[!구글/유튜브/네이버/나무위키/다나와 [검색]] : 해당 사이트에서 검색합니다.\n"
                                       "[!번역 [한/영] [문장]] : 한국어->영어, 영어->한국어로 번역합니다.\n"
                                       "[!영어사전 [단어]] : 네이버 영어사전에 단어를 검색합니다.\n"
                                       "[!날씨 [지역이름]] : 오늘 날씨를 검색합니다.\n"
                                       "[!거리 [지역이름] [지역이름]] : 지역과 지역 사이의 거리를 검색합니다.\n"
                                       "[!전화번호 [지역이름]] : 전화번호를 검색합니다.\n"
                                       "[!가사 [노래]] : 노래 가사를 검색합니다.\n"
                                       "[!상태메시지 [말]] : 봇의 상태메시지를 바꿉니다.\n"
                                       "[!텍스트 [텍스트]] : 텍스트를 멋있게 바꿔줍니다!\n"
                                       "[!명령어 노래봇] : 노래봇 명령어를 보여줍니다.\n```")
        elif message.content.startswith("!명령어 노래봇"):
            await message.channel.send("```\n"
                                       "[노래봇 명령어]\n\n"
                                       "[!참가] : 봇이 음성 채널에 참여합니다.\n"
                                       "[!나가] : 봇이 음성 채널에서 나갑니다.\n"
                                       "[!재생 [URL]] : 유튜브에서 노래를 재생합니다.\n"
                                       "[!검색 [제목]] : 유튜브에서 영상을 검색해 결과를 보여줍니다.\n"
                                       "[!선택 [번호]] : 검색 결과 중에서 선택합니다.\n"
                                       "[!일시정지] : 노래를 일시정지합니다.\n"
                                       "[!다시재생] : 노래를 다시 재생합니다.\n"
                                       "[!정지] : 노래를 정지합니다.\n"
                                       "[!재생목록] : 재생목록을 보여줍니다.\n```")
        elif message.content.startswith("!관리자"):
            if message.author.id != 351677960270381058:
                await message.channel.send("관리자가 아니에요.")
                return
            msg = message.content.split(" ")
            query = msg[1]
            if query is None:
                await message.channel.send("명령어를 입력해주세요.")
            elif query == "잠금":
                ignore = True
                await message.channel.send("봇이 대답하지 않습니다.")
            elif query == "잠금해제":
                ignore = False
                await message.channel.send("봇이 대답합니다.")
            elif query == "실행": #!관리자 실행 []
                cmd = message.content[8:]
                if cmd is None:
                    await message.channel.send("명령어를 입력해주세요.")
                    return
                result = subprocess.check_output(cmd, shell=True)
                await message.channelsend(result)
        elif message.content.startswith("!안녕"):
            await message.channel.send("안녕하세요!")
        elif message.content.startswith("!아침"):
            await message.channel.send("좋은 아침이에요!")
        elif message.content.startswith("!노예야"):
            await message.channel.send("예 주인님!")
        elif message.content.startswith("!말해라"):
            msg = message.content
            if len(msg) == 0:
                await message.channel.send("말을 입력해주세요.")
            else:
                await message.channel.send(msg[5:])
        elif message.content.startswith("!레식전적"):
            msg = message.content
            username = msg[6:]
            if len(username) == 0:
                await message.channel.send("닉네임을 입력해주세요.")
            else:
                username = urllib.parse.quote(username)
                link = "https://r6.tracker.network/profile/pc/" + username
                link += "\nhttps://r6.op.gg/search?search=" + username
                await message.channel.send(link)
        elif message.content.startswith("!롤전적"):
            msg = message.content
            username = msg[5:]
            if len(username) == 0:
                await message.channel.send("닉네임을 입력해주세요.")
            else:
                username = urllib.parse.quote(username)
                link = "https://www.op.gg/summoner/userName=" + username
                await message.channel.send(link)
        elif message.content.startswith("!롤체전적"):
            msg = message.content
            username = msg[6:]
            if len(username) == 0:
                await message.channel.send("닉네임을 입력해주세요.")
            else:
                username = urllib.parse.quote(username)
                link = "https://lolchess.gg/profile/kr/" + username
                await message.channel.send(link)
        elif message.content.startswith("!구글"):
            msg = message.content
            query = msg[4:]
            query = urllib.parse.quote(query)
            if len(query) == 0:
                await message.channel.send("https://www.google.com/")
            else:
                link = "https://www.google.com/search?q=" + query
                await message.channel.send(link)
        elif message.content.startswith("!유튜브"):
            msg = message.content
            query = msg[5:]
            query = urllib.parse.quote(query)
            if len(query) == 0:
                await message.channel.send("https://www.youtube.com/")
            else:
                link = "https://www.youtube.com/results?search_query=" + query
                await message.channel.send(link)
        elif message.content.startswith("!네이버"):
            msg = message.content
            query = msg[5:]
            query = urllib.parse.quote(query)
            if len(query) == 0:
                await message.channel.send("https://www.naver.com/")
            else:
                link = "https://search.naver.com/search.naver?query=" + query
                await message.channel.send(link)
        elif message.content.startswith("!나무위키"):
            msg = message.content
            query = msg[6:]
            original = query
            query = urllib.parse.quote(query)
            if len(query) == 0:
                await message.channel.send("https://namu.wiki/w/")
            else:
                link = "https://namu.wiki/w/" + query
            reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
            code = soup.find_all("div", {"class": "wiki-heading-content"})
            result = code[0].getText(' ', strip=True)

            S = "**" + original + "** 검색 결과입니다.\n"
            await message.channel.send(S)
            if len(result) >= 1999:
                S = ""
                l = 1999
                s = 0
                e = l
                while True:
                    S = result[s:e]
                    if S is None:
                        break
                    await message.channel.send(S)
                    s = e + 1
                    e = e + l
            await message.channel.send(result)
        elif message.content.startswith("!이미지"):
            msg = message.content
            query = msg[5:]
            query = urllib.parse.quote(query)
            if len(query) == 0:
                await message.channel.send("검색할 내용을 입력해주세요.")
                return
            link = "https://www.google.com/search?hl=ko&tbm=isch&sclient=img&q=" + query
            reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
        elif message.content.startswith("!다나와"):
            msg = message.content
            query = msg[5:]
            query = urllib.parse.quote(query)
            if len(query) == 0:
                await message.channel.send("http://danawa.com/")
            else:
                link = "http://search.danawa.com/dsearch.php?query=" + query
                await message.channel.send(link)
        elif message.content.startswith("!번역"): #!번역 한 안녕하세요.
            msg = message.content
            lang = msg[4:5]
            link =" https://papago.naver.com/"
            if len(lang) == 0:
                await message.channel.send("언어를 입력해주세요.")
            elif lang == "한":
                link += "?sk=ko&tk=en&st="
            elif lang == "영":
                link += "?sk=en&tk=ko&st="
            query = msg[6:]
            query = urllib.parse.quote(query)
            link += query
            reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
            code = soup.find("div", id="txtTarget")
            if code is None:
                await message.channel.send("번역 오류.")
            else:
                result = code.text
                await message.channel.send(result)
        elif message.content.startswith("!오퍼레이터"): # ############################################
            msg = message.content.split(" ")
            type = msg[1]
            query = msg[2]
            if len(query) == 0:
                await message.channel.send("이름을 입력해주세요.")
            query = urllib.parse.quote(query)
            link = "https://namu.wiki/w/" + query
            reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
            code = soup.find_all("div", {"class" : "wiki-heading-content"})
            #weaponinfo = code[1].getText('\n', strip=True)
            if type == "무기":
                html = code[1]
                soup = BeautifulSoup(html, 'html.parser')
                code = soup.find_all("div", {"class" : "wiki-paragraph"})
                await message.channel.send(code[1].text)
        elif message.content.startswith("!영어사전"):
            msg = message.content
            query = msg[6:]
            query = urllib.parse.quote(query)
            link = "https://en.dict.naver.com/#/search?query=" + query
            reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
            code = soup.find("div", class_="row")

            if code is None:
                await message.channel.send("단어를 찾을 수 없습니다.")
            else:
                #result = code.getText('\n', strip=True)
                result = code.text
                await message.channel.send(result)
        elif message.content.startswith("!날씨"):
            location = message.content[4:]
            if len(location) == 0:
                await message.channel.send("지역을 입력해주세요.")
            else:
                query = location + " 날씨"
                query = urllib.parse.quote(query)
                link = "https://search.naver.com/search.naver?query=" + query
                reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
                code1 = soup.find("span", class_="todaytemp") #온도
                if code1 is None:
                    await message.channel.send("지역을 찾을 수 없어요.")
                temp = "기온 : "
                temp += code1.text
                temp += "℃"
                code2 = soup.find("span", class_="btn_select") #지역명
                if code2 is None:
                    code3 = soup.find("a", class_="btn_select _selectLayerTrigger") #해외 날씨
                    tloc = code3.text
                else:
                    tloc = code2.text #국내 날씨
                code4 = soup.find("span", class_="min") #최저기온
                if code4 is None:
                    code4 = "Null"
                else:
                    code4 = code4.text
                min = "최저기온 : "
                min += code4
                # min += "C"
                code5 = soup.find("span", class_="max") #최고기온
                if code5 is None:
                    code5 = "Null"
                else:
                    code5 = code5.text
                max = "최고기온 : "
                max += code5
                # max += "C"
                code6 = soup.find("span", class_="sensible") #체감온도
                if code6 is None:
                    code6 = "Null"
                else:
                    code6 = code6.text
                sensible = code6
                # sensible += "C"
                code7 = soup.find("span", class_="rainfall") #시간당 강수량
                if code7 is None:
                    code7 = "Null"
                else:
                    code7 = code7.text
                rainfall = code7
                code8 = soup.find("div", class_="detail_box") #미세먼지, 초미세먼지, 오존지수
                if code8 is None:
                    code8 = "Null"
                else:
                    code8 = code8.text
                detail = code8
                detail = detail[2:]
                detail.replace(" ", "\n")
                S = tloc + "\n" + temp + "\n" + min + "\n" + max + "\n" + sensible + "\n" + rainfall + "\n" + detail
            await message.channel.send(S)
        elif message.content.startswith("!거리"):
            msg = message.content
            query = msg[1:]
            query = urllib.parse.quote(query)
            link = "https://www.google.com/search?q=" + query
            reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
            code = soup.find("div", class_="dDoNo vk_bk") #dDoNo vk_bk
            if code is None:
                await message.channel.send("거리를 찾을 수 없어요.")
            distance = code.text
            await message.channel.send(distance)
        elif message.content.startswith("!계산기"):
            msg = message.content
            query = msg[5:]
            # result = eval(query)
            result = 0
            S = query + " = **" + str(result) + "**"
            await message.channel.send(S)
        elif message.content.startswith("!전화번호"):
            query = message.content[6:]
            if len(query) == 0:
                await message.channel.send("검색 대상을 입력해주세요.")
            else:
                query = query + " 전화번호"
                query = urllib.parse.quote(query)
                link = "https://search.naver.com/search.naver?query=" + query
                reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
                code1 = soup.find("a", class_="tit _title _sp_each_url _sp_each_title")
                if code1 is None:
                    await message.channel.send("지역을 찾을 수 없어요.")
                place = code1.text
                code2 = soup.find("span", class_="tell")
                tell = code2.text
                S = place
                S += "\n"
                S += tell
            await message.channel.send(S)
        elif message.content.startswith("!가사"):
            query = message.content[4:]
            query = query + " 가사"
            query = urllib.parse.quote(query)
            link = "https://search.naver.com/search.naver?query=" + query
            reqUrl = urllib.request.Request(link, headers={'User-Agent' : 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
            code = soup.find("div", class_="lyrics_area")
            if code is None:
                await message.channel.send("노래 가사를 찾을 수 없습니다.")
            lyrics = code.getText('\n', strip=True)
            lyrics = lyrics[:lyrics.rfind('\n')]
            lyrics = lyrics[:lyrics.rfind('\n')]
            await message.channel.send(lyrics)
        elif message.content.startswith("!상태메시지"):
            msg = message.content
            q = msg[7:]
            if len(q) != 0:
                game = discord.Game(q)
                await client.change_presence(status=discord.Status.online, activity=game)
                await message.channel.send("상태메시지를 바꿨어요.")
            else:
                await message.channel.send("상태메시지를 써주세요.")
        elif message.content.startswith("!텍스트"):
            msg = message.content
            q = msg[5:]
            if len(q) == 0:
                await message.channel.send("텍스트를 입력해주세요.")
                return
            q = urllib.parse.quote(q)
            link = "http://qaz.wtf/u/convert.cgi?text=" + q
            reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
            code = soup.find_all("td")
            S = ""
            flag = False
            for X in code:
                if flag is True:
                    T = X.text
                    T = T[:T.rfind('\n')]
                    S += T
                    flag = False
                else:
                    flag = True
            await message.channel.send(S)
        elif message.content == "!참가":
            if message.author.voice is None:
                await message.channel.send("먼저 음성 채널에 들어와 주세요.")
            channel = message.author.voice.channel
            vc = await channel.connect()
            # P = AsyncPlayer(vc)
            # await P.start()
            await message.channel.send("음성 채널에 참가했어요.")
        elif message.content == "!나가":
            vc = message.guild.voice_client
            if vc is None:
                await message.channel.send("봇이 음성 채널에 들어와 있지 않아요.")
                return
            await vc.disconnect()
            await message.channel.send("음성 채널을 나갔어요.")
            ClearYoutubeDL()
        elif (message.content.startswith("!재생") or message.content.startswith("!선택")) and message.content != "!재생목록":
            msg = message.content
            if msg.startswith("!재생"):
                url = msg[4:]
                if len(url) == 0:
                    await message.channel.send("URL을 입력해 주세요.")
                    return
            elif msg.startswith("!선택"):
                if len(SR) == 0:
                    await message.channel.send("먼저 **!검색** 을 통해 검색해주세요.")
                choice = int(msg[4:])
                choice -= 1
                url = SR[choice].link
                SR.clear()
            channel = message.author.voice.channel
            server = message.guild
            vc = message.guild.voice_client

            if vc is None:
                await message.channel.send("봇이 음성 채널에 들어와 있지 않아요.")
                return

            if vc.is_playing():
                await message.channel.send("노래가 이미 재생 중입니다.")
                return
            elif len(Q) != 0:
                Q.pop(0)

            reqUrl = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
            title = soup.find("span", id="eow-title").text
            title = title.strip()

            download_path = os.path.join(PATH, "youtubedl")
            download_path += "\\"
            string_pool = string.ascii_letters
            _LENGTH = 10
            for i in range(_LENGTH) :
                download_path += random.choice(string_pool)
            download_path += ".mp3"

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': download_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            S = "**" + title + "** 을 다운로드 중..."
            await message.channel.send(S)

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # download_path, title

            Q.append(VideoInfo(title, download_path))
            vc.play(discord.FFmpegPCMAudio(Q[0].path))
            #await AsyncCheck()

            S = "**" + Q[0].title + "** 을 재생 목록에 추가했습니다."
            await message.channel.send(S)
        elif message.content.startswith("!검색"):
            msg = message.content
            query = msg[4:]
            if len(query) == 0:
                await message.channel.send("검색할 영상 제목을 입력해주세요.")
                return
            S = "**" + query + "** 을 검색하는 중..."
            await message.channel.send(S)
            query = urllib.parse.quote(query)
            link = "https://www.youtube.com/results?search_query=" + query
            reqUrl = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urllib.request.urlopen(reqUrl).read(), 'html.parser')
            SR.clear()
            for vid in soup.find_all(attrs={"class": "yt-uix-tile-link"}, limit=5):
                URL = "https://www.youtube.com"
                URL += vid['href']
                Title = vid['title']
                SR.append(SearchResult(Title, URL))
            S = "**!선택 [1-5]** 로 선택해주세요.\n"
            i = 1
            for X in SR:
                S += "**"
                S += str(i) + ". " + X.title
                S += "**\n"
                i += 1
            await message.channel.send(S)
        elif message.content == "!일시정지":
            vc = message.guild.voice_client
            if vc is None:
                await message.channel.send("먼저 음악을 재생해주세요.")
                return
            vc.pause()
            await message.channel.send("음악을 일시정지했어요.")
        elif message.content == "!다시재생":
            vc = message.guild.voice_client
            if vc is None:
                await message.channel.send("먼저 음악을 재생해주세요.")
                return
            vc.resume()
            await message.channel.send("음악을 다시 재생합니다.")
        elif message.content == "!정지":
            vc = message.guild.voice_client
            if vc is None:
                await message.channel.send("먼저 음악을 재생해주세요.")
                return
            vc.stop()
            Q.pop(0)
            await message.channel.send("음악을 정지했어요.")
            ClearYoutubeDL()
        elif message.content == "!재생중":
            vc = message.guild.voice_client
            if vc is None:
                await message.channel.send("먼저 음악을 재생해주세요.")
                return
            S = Q[0].title
            await message.channel.send(S)
        elif message.content == "!재생목록":
            vc = message.guild.voice_client
            if vc is None:
                await message.channel.send("먼저 음악을 재생해주세요.")
                return
            l = len(Q)
            i = 1
            S = "**"
            for X in Q:
                S += str(i)
                S += ": "
                S += X.title
                S += "\n"
                i += 1
            S += "**"
            await message.channel.send(S)
        else:
            await message.channel.send("무슨 말인지 모르겠어요.")

    elif message.content == "홀리쓋":
        await message.channel.send("보여주는부분이네")
    elif message.content == "사발":
        await message.channel.send("면")
    #elif message.content.startswith("ㅋ"):
    #    if message.author.bot is False:
    #        await message.channel.send("ㅋㅋㅋㅋㅋㅋㅋ")


file = os.path.join(PATH, "token")
f = open(file, "r")
TOKEN = f.readline()
f.close()
client.run(TOKEN)
