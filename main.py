import discord
from discord.ext import commands
import spotipy
import spotipy.util as util
import asyncio
import random
random.random()
disToken = "###" # discord api token
scope = 'user-read-playback-state%20' + \
    'playlist-read-private%20' + 'user-modify-playback-state'

bot = commands.Bot(command_prefix='.')

def sp_api_getter():
    sptoken = util.prompt_for_user_token(username="####", scope=scope, client_id="####",
                                         client_secret="#####", redirect_uri="http://localhost:8888/callback")
    spotify = spotipy.Spotify(auth=sptoken, language='ja')
    return spotify

@bot.command()
async def イントロクイズ(ctx, *arg):
    await ctx.send("イントロクイズを開始します！")
    if(1 > len(arg)):
        plid = "37i9dQZEVXbKXQ4mDTEBXq" #引数が指定されてない場合は日本 TOP50のプレイリストが指定されています。
    elif(1 == len(arg)):
        if("https://open.spotify.com/playlist/" in arg[0]):
            plid = arg[0].split(
                'https://open.spotify.com/playlist/')[-1].split('?si=')[0]
        elif("spotify:playlist:" in arg[0]):
            plid = arg[0].split(':playlist:')[-1]
    else:
        return await ctx.send("コマンドの引数の数が一致していません")
    spotify = sp_api_getter()
    playlist = spotify.playlist_tracks(
        playlist_id=plid, market="JP")
    if(100 < playlist['total']):
        mx = 100
    else:
        mx = playlist['total']
    mx1 = mx - 1
    ans = {}
    i = rand_ints_nodup(0, mx1, mx)
    for j in range(mx):
        spotify = sp_api_getter()
        playlist = spotify.playlist_tracks(
            playlist_id=plid, market="JP", limit=mx)
        num = int(i[int(j)])
        name = playlist['items'][num]['track']['name']  # 曲名
        uri = playlist['items'][num]['track']['uri']  # SpotifyTrackUri
        # SpotifyOpenURL
        opurl = playlist['items'][num]['track']['external_urls']['spotify']
        # アーティスト名
        artists = playlist['items'][num]['track']['artists'][0]['name']
        # アートワーク
        artwork = playlist['items'][num]['track']['album']['images'][0]['url']
        spotify.start_playback(uris=[uri])
        await ctx.send('この曲名は何でしょうか〜？')
        def check(m):
            return m.content == name or m.content == "CExit" or m.content == "CSkip"
        try:
            msg = await bot.wait_for('message', timeout=25.0, check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed()
            embed.set_author(
                name="曲情報", url=opurl, icon_url="https://img.icons8.com/plasticine/2x/spotify.png")
            embed.add_field(
                name="曲名", value=name)
            embed.add_field(
                name="アーティスト名", value=artists)
            embed.set_thumbnail(
                url=artwork)
            text = f'正解は{name}でした'
            await ctx.send(embed=embed, content=text)
        else:
            #強制終了
            if(msg.content == "CExit"):
                await ctx.send("イントロクイズを強制終了しました。")
                return
            #スキップ機能
            elif(msg.content == "CSkip"):
                await ctx.send("スキップします")
                embed = discord.Embed()
                embed.set_author(
                    name="曲情報", url=opurl, icon_url="https://img.icons8.com/plasticine/2x/spotify.png")
                embed.add_field(
                    name="曲名", value=name)
                embed.add_field(
                    name="アーティスト名", value=artists)
                embed.set_thumbnail(
                    url=artwork)
                text = f'正解は{name}でした'
                await ctx.send(embed=embed, content=text)
                continue
            else:
                embed = discord.Embed()
                embed.set_author(
                    name="曲情報", url=opurl, icon_url="https://img.icons8.com/plasticine/2x/spotify.png")
                embed.add_field(
                    name="曲名", value=name)
                embed.add_field(
                    name="アーティスト名", value=artists)
                embed.set_thumbnail(
                    url=artwork)
                text = f'{msg.author.mention}さん正解！'
                await ctx.send(embed=embed, content=text)
                ans[msg.author.name] = ans.get(msg.author.name, 0) + 1
    embed = discord.Embed()
    embed.set_author(
        name=f"結果発表！ - 合計{mx}曲", url=f"https://open.spotify.com/playlist/{plid}")
    rank = 1
    for k, v in sorted(ans.items(), key=lambda x: -x[1]):
        embed.add_field(name=f"{rank}位", value=f'{str(k)}さん 正解数:{str(v)}')
        rank += 1
    await ctx.send(embed=embed, content="お疲れ様でした、イントロクイズ終了です！")

# 乱数生成 重複なし
def rand_ints_nodup(a, b, k):
    ns = []
    while len(ns) < k:
        n = random.randint(a, b)
        if not n in ns:
            ns.append(n)
    return ns

bot.run(disToken)
