import requests
import json
import discord
from discord.ext import commands
from paginas import Pages

#mensagen automatica quando passa de nivel
#mundo, guild, guild membership, last login, status
#coluna da esquerda em negrito, status verde pra online e vermelho pra offline
#mostrar membros da guild com api e guildhall se nao tiver guildhall dizer que nao possui

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def char(ctx, *, nome):
    try:
        n = nome.split(" ")
        char = "+".join(n)
        response = requests.get("https://api.tibiadata.com/v2/characters/" + char + ".json")
        api = json.loads(response.content)
        if api["characters"]["data"]["status"] == "online":
            stat = '```css\n-{str}```'.format(str=api["characters"]["data"]["status"])
        else:
            stat = '```diff\n-{str}```'.format(str=api["characters"]["data"]["status"])
        inf = ('**Nome: **' + api["characters"]["data"]["name"] + '\n' +
        '**Sexo: **' + api["characters"]["data"]["sex"] + '\n' +
        '**Vocação: **' + api["characters"]["data"]["vocation"] + '\n' +
        '**Mundo: **' + api["characters"]["data"]["world"] + '\n' +
        '**Guild: **' + api["characters"]["data"]["guild"]["name"] + '\n' +
        '**Último login: **' + api["characters"]["data"]["last_login"][0]["date"] + 
         stat)
        await ctx.send(inf)
    except:
        await ctx.send("Esse personagem não existe")

@client.command()
async def guild(ctx, *, guilda):
    
    g = guilda.split(" ")
    gui = "+".join(g)
    response = requests.get("https://api.tibiadata.com/v2/guild/" + gui + ".json")
    api = json.loads(response.content)
    if api["guild"]["data"]["guildhall"]["name"]:
        await ctx.send("**Guild House: **" + api["guild"]["data"]["guildhall"]["name"])
    else:
        await ctx.send("Essa guilda não possui uma casa")
    await ctx.send("Essa guilda possui " + str(api["guild"]["data"]["totalmembers"]) + " membros representados pela seguinte lista:")
    members = []
    for index in api["guild"]["members"]:
        for index2 in index["characters"]:
            m = ("**Nome: **" + index2["name"] + "**   Level: **" + str(index2["level"]) +
            "**   Vocação: **" + index2["vocation"] + "**   Status: **" + index2["status"])
            members.append(m)
    pages = Pages(ctx, entries=members, per_page=6)
    try:
        await pages.paginate()
    except:
        await ctx.send("Não paginou")
            
    
    

client.run("NzEwMzI1NTkxNTc1ODg3OTQz.Xr2lNA.Z1aDTxJlkhsH9zVFDJ_cZRLZYtM")

