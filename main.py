import discord
from discord.ext import commands
import datetime
import requests
import json
import random
import threading
import asyncio
import aiohttp
from discord.ext import tasks
from discord import Member

from urllib import parse, request
import re

bot = commands.Bot(command_prefix='your prefix')

#you can dm a mentioned member with this command example: !dm @uesename hi
@bot.command()
async def dm(ctx, user: discord.User, *, value):

    await user.send(f"**{value} Sent by {ctx.author.display_name}**")

#fortnite user stats example: !stats ninja
@bot.command()
async def stats(ctx, arg):
	r = requests.get(
	    f'https://fortnite-api.com/v1/stats/br/v2?name={arg}&image=all')
	rr = r.json()
	embed = discord.Embed()
	embed.set_image(url=f"{rr['data']['image']}")
	await ctx.send(embed=embed)

#gets the responce time for the bot
@bot.command()
async def ping(ctx):
	if round(bot.latency * 1000) <= 50:
		embed = discord.Embed(
		    title="leaks bot ping",
		    description=
		    f"my ping is **{round(bot.latency *1000)}** milliseconds!",
		    color=0x44ff44)
	elif round(bot.latency * 1000) <= 100:
		embed = discord.Embed(
		    title="leaks bot ping",
		    description=
		    f"my ping is **{round(bot.latency *1000)}** milliseconds!",
		    color=0xffd000)
	elif round(bot.latency * 1000) <= 200:
		embed = discord.Embed(
		    title="leaks bot ping",
		    description=
		    f"my ping is **{round(bot.latency *1000)}** milliseconds!",
		    color=0xff6600)
	else:
		embed = discord.Embed(
		    title="leaks bot ping",
		    description=
		    f" my ping is **{round(bot.latency *1000)}** milliseconds!",
		    color=0x990000)
	await ctx.send(embed=embed)

#gets info on any fortnite item exapmple: !search scenario
@bot.command()
async def search(ctx, cosnamee):
	r = requests.get(
	    f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={cosnamee}')
	rr = r.json()
	if rr['status'] == 200:
		for sub_dict in rr['data']:
			embed = discord.Embed(color=0x0d95fd)
			embed.add_field(name='Name',
			                value=f"``{sub_dict['name']}``",
			                inline=False)
			embed.add_field(name='ID',
			                value=f"``{sub_dict['id']}``",
			                inline=False)
			embed.add_field(name='Rarity',
			                value=f"``{sub_dict['description']}``",
			                inline=False)
			embed.add_field(name='Type',
			                value=f"``{sub_dict['type']['value']}``",
			                inline=False)
			embed.add_field(name='Display Type',
			                value=f"``{sub_dict['type']['displayValue']}``",
			                inline=False)
			embed.add_field(name='Backend Value',
			                value=f"``{sub_dict['type']['backendValue']}``",
			                inline=False)
			embed.add_field(name='Rarity',
			                value=f"``{sub_dict['rarity']['value']}``",
			                inline=False)
			embed.add_field(name='Backend Rarity',
			                value=f"``{sub_dict['rarity']['backendValue']}``",
			                inline=False)
			embed.add_field(name='Series',
			                value=f"``{sub_dict['series']}``",
			                inline=False)
			if sub_dict['introduction'] == None:
				pass
			else:
				embed.add_field(
				    name='Introduction',
				    value=f"``{sub_dict['introduction']['text']}``",
				    inline=False)
				embed.add_field(name='Display Asset Path',
				                value=f"``{sub_dict['displayAssetPath']}``",
				                inline=False)
				embed.add_field(name='Definition Path',
				                value=f"``{sub_dict['definitionPath']}``",
				                inline=False)
				embed.set_thumbnail(
				    url=
				    f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/icon.png"
				)
				embed.set_footer(text=f"{bot.user.name} | Made By Glitchlux")
				message = await ctx.send(embed=embed)
	else:
		embed = discord.Embed(color=0xff0f0f)
		embed.add_field(name='Error', value=f"``{rr['error']}``", inline=False)
		message = await ctx.send(embed=embed)
		await message.delete()

#gets the current battle royale news
@bot.command()
async def brnews(ctx):
	response = requests.get('https://fortnite-api.com/v2/news/br').json()
	embed = discord.Embed(title='Br News')
	embed.set_image(url=response['data']['image'])
	await ctx.send(embed=embed)
#gets the current save the world news
@bot.command()
async def stwnews(ctx):
	response = requests.get('https://api.peely.de/v1/stw/news').json()
	embed = discord.Embed(title='Save The World News')
	embed.set_image(url=response['data']['image'])
	await ctx.send(embed=embed)

#gets the progress of the current fortnite season
@bot.command()
async def progress(ctx):
	await ctx.send('https://api.peely.de/v1/br/progress')

#gets the profile picture of the mentioned user
@bot.command()
async def getpfp(ctx, member: Member = None):
	if not member:
		member = ctx.author
	await ctx.send(member.avatar_url)

#gets the battle royale item shop
@bot.command()
async def shop(ctx, aliases=['shop', 'itemshop']):
	response = requests.get('https://api.peely.de/v1/shop').json()
	embed = discord.Embed(title=response['time'])
	embed.set_image(url=response['uniqueurl'])
	await ctx.send(embed=embed)

#server infomation
@bot.command()
async def serverinfo(ctx):
	name = str(ctx.guild.name)
	description = str(ctx.guild.description)

	owner = str(ctx.guild.owner)
	id = str(ctx.guild.id)
	region = str(ctx.guild.region)
	memberCount = str(ctx.guild.member_count)

	icon = str(ctx.guild.icon_url)

	embed = discord.Embed(title=name + " Server Information",
	                      description=description,
	                      color=discord.Color.blue())
	embed.set_thumbnail(url=icon)
	embed.add_field(name="Server ID", value=id, inline=True)
	embed.add_field(name="Region", value=region, inline=True)
	embed.add_field(name="Member Count", value=memberCount, inline=True)
	await ctx.send(embed=embed)

 #repeats anything you say
@bot.command()
async def repeat(ctx, arg):
	await ctx.send(arg)

#gets the roles of the mentioned user
@bot.command()
async def roles(ctx, *, member: MemberRoles):
	await ctx.send('they have the following roles: ' + ', '.join(member))

#member count for the server
@bot.command(aliases=["mc"])
async def member_count(ctx):
  a = ctx.guild.member_count
  b = discord.Embed(title=f"current members in {ctx.guild.name}",
 	       description=a,
	        color=discord.Color((0)))
  await ctx.send(embed=b)

#gets the battle royale aes keys
@bot.command()
async def aes(ctx):
	r = requests.get('https://benbotfn.tk/api/v1/aes')
	rr = r.json()

	mainkey = rr['mainKey']
	version = rr['version']
	embed = discord.Embed(title=f"{version} Aes", description="")
	embed.add_field(name='MainKey', value=f'``{mainkey}``', inline=False)
	for sub_dict in rr['dynamicKeys']:
		embed.add_field(name=sub_dict.split('FortniteGame/Content/Paks/')
		                [1].strip().replace('"', ''),
		                value=f"``{rr['dynamicKeys'][sub_dict]}``",
		                inline=False)
		embed.set_footer(text=f'{ctx.guild.name}',
		                 icon_url=f'{ctx.guild.icon_url}member_count')
	await ctx.send(embed=embed)

#credits
@bot.command()
async def credits(ctx):
	embed = discord.Embed(
	    title="Credits for leaks bot",
	    description="",
	    body="fortnite-api, benbot, nitestats and stackoverflow")

	embed.set_footer(text="fortnite-api, benbot, nitestats and stackoverflow")
	await ctx.send(embed=embed)

#gets the latest fortnite version
@bot.command()
async def version(ctx):
	r = requests.get('https://api.nitestats.com/v1/epic/builds/fltoken')
	rr = r.json()

	version = rr['version']
	embed = discord.Embed(title=f"{version} ", description="")
	await ctx.send(embed=embed)

@bot.command()
async def fltoken(ctx):
	r = requests.get('https://api.nitestats.com/v1/epic/builds/fltoken')
	rr = r.json()

	fltoken = rr['fltoken']
	embed = discord.Embed(title=f"fortnite current fltoken {fltoken} ", description="")
	await ctx.send(embed=embed)

#gets the count of fortnites pak files
@bot.command()
async def pakcount(ctx):
	r = requests.get('https://benbotfn.tk/api/v1/status')
	rr = r.json()

	totalPakCount = rr['totalPakCount']
	dynamicPakCount = rr['dynamicPakCount']

	embed = discord.Embed(title=f"total pak count {totalPakCount} ",
	                      description="")
	embed.add_field(name='dynamic Pak Count',
	                value=f'{dynamicPakCount}',
	                inline=False)
	await ctx.send(embed=embed)

#gets the latest version for fall guys
@bot.command()
async def fgversion(ctx):
	r = requests.get('https://fallguysapi.tk/api/version')
	rr = r.json()

	currentVersion = rr['currentVersion']
	gameSize = rr['gameSize']

	embed = discord.Embed(title=f"current fall guys Version is V{currentVersion} ",
	                      )
	embed.add_field(name='fall guys game size',
	                value=f'{gameSize}',
	                inline=False)
	await ctx.send(embed=embed)

#gets the build info for fall guys
@bot.command()
async def fgbuild(ctx):
	r = requests.get('https://fallguysapi.tk/api/version')
	rr = r.json()

	manifestId = rr['manifestId']
	buildId = rr['buildId']

	embed = discord.Embed(title=f"current fall guys manifest Id is {manifestId} ",
	                      )
	embed.add_field(name='fall guys build Id is ',
	                value=f'{buildId}',
	                inline=False)
	await ctx.send(embed=embed)

# Events
#log in event
@bot.event
async def on_ready():
	print('Bot Ready/Logged In')
	status = requests.get('https://benbotfn.tk/api/v1/status').json()
	await bot.change_presence(activity=discord.Game(
	    name=f"{status['currentFortniteVersion']}"))

bot.run('your token')
