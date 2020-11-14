import discord
import asyncio
from discord.ext import commands
import random
from random import randrange
from discord.ext.commands import has_permissions
from datetime import datetime


#variable pour le jeu du nombre
global nombre
global ingame
global joueur
global score
score = 0
joueur = ""
nombre = 235
ingame = False
msg = 0



#list des gis pour la commande eat
global gif
gif = ["https://tenor.com/IX1k.gif" , "https://tenor.com/ZYAx.gif" , "https://tenor.com/bc8yr.gif" , "https://tenor.com/Z9ql.gif" , "https://tenor.com/7mx5.gif"]
id = ["<@703318094592081963>","<@!703318094592081963>"]

client = commands.Bot(command_prefix="i.")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
	global joueur
	global nombre
	global ingame
	global score
	if message.author != client.user:
		await client.process_commands(message)

		msg2 = str(message.content)
		msg2 = msg2.split()
		result = any(elem in id for elem in msg2)
		if result or str(message.content)=="Sahel":
			await message.channel.send("Oh **TABARNAK** on m’a appelé ?")
			print("ping de "+str(message.author))

		#Le jeu du nombre :
		if message.author.id == joueur:
			if message.content.startswith("i.play"):
				return
		

			if ingame == True:
				try:
					msg = int(message.content)
				except:
					await message.channel.send("eh ! tu es prié d'envoyer un nombre , pas autre chose compris ?")
					return
			

				if msg > nombre:
					await message.channel.send("trop grand !")
					score +=1
				if msg < nombre:
					await message.channel.send("trop petit !")
					score+=1
				if msg == nombre:
					score+=1
					await message.channel.send("bravo :p !")
					await asyncio.sleep(1)
					await message.channel.send("tu as trouvé en "+str(score)+" essais")
					await client.change_presence(activity = None)
					ingame = False
					joueur = 0

			else:
				return
			

@client.event
async def on_member_remove(member):
	if member.guild.id !=702207953775624233:
		return
	channel = client.get_channel(702250883534291014)
	async for message in channel.history(limit = 1000):
		if message.author == member:
			await message.delete()



@client.command()
@has_permissions(administrator=True)
async def ban(ctx , member:discord.User = None , reason = None):
	if member == None:
		await ctx.send("il faut indiquer quelqu’un à ban sinon ça ne marchera pas :sweat_smile:")
		return
	if member == ctx.author:
		await ctx.send("c'est bête de vouloir s'auto ban :')")
		return

	try:

		await ctx.guild.ban(member)
		await ctx.send(str(member) + " a été banni")
	except:
		await ctx.send("une erreur c'est produite")



@client.command()
@has_permissions(administrator=True)
async def kick(ctx , member:discord.User = None , reason = None):
	if member == None:
		await ctx.send("il faut indiquer quelqu’un à kick sinon ça ne marchera pas :sweat_smile:")
		return
	if member == ctx.author:
		await ctx.send("c'est bête de vouloir s'auto kick  :')") 
		return

	try:

		await ctx.guild.kick(member)
		await ctx.send(str(member) + " a été kick")
	except:
		await ctx.send("une erreur c'est produite")


@client.command()
@has_permissions(administrator=True)
async def warn(ctx , member:discord.User = None , reason = None):
	if member == None:
		await ctx.send('veuillez spécifier quelqu’un à warn')
		return
	if member == ctx.author:
		await ctx.send('vous ne pouvez pas vous warn vous même')
		return

	await ctx.send(str(member)+" à été warn pour la raison suivant : " + "`" +reason + "`")
	await member.send("vous avez été warn pour la raison suivant : " + "`" +reason + "`" )
	return


@client.command()
async def eat(ctx , member:discord.User = None):
	if member == None:
		return
	await ctx.send("**"+str(ctx.author.name)+"**" + " mange " + "**"+str(member.name)+"**"+"\n" +random.choice(gif))
	#await ctx.send(random.choice(gif))
	return 


@client.command()
async def tabarnak(ctx):
	msg = await ctx.send("***TABARNAK***")
	await msg.add_reaction('🇨🇦')


@client.command()
@has_permissions(administrator=True)
async def mp(ctx , member:discord.User ,*, msg):
	await ctx.message.delete()
	await member.send(msg)
	print("mp envoyé à "+str(member) + " contenant " + str(msg))





@client.command()
@has_permissions(administrator=True)
async def say(ctx , *, arg):
	await ctx.message.delete()
	await ctx.send(arg)

	
@client.command()
@has_permissions(administrator = True)
async def pub_mp_everyone(ctx , *, arg):
	serveur = ctx.guild
	for member in serveur.members:
		if member.id != client.user.id:
			await member.send(arg)
			print("pub mp envoyé à " + str(member))
	await ctx.send("mp envoyés")
	return


#commande du_ jeu du nombre :

@client.command()
async def play(ctx):
	global nombre
	global ingame
	global joueur
	global score
	if str(ctx.channel.type) == "private":

		await ctx.send("désolé il n'est pas possible de démarrer une partie en mp")
		return

	if ingame == False:
		ingame = True
		nombre = randrange(0,1000)
		score = 0
		joueur = ctx.author.id
		print(ctx.author)
		print(nombre)
		await client.change_presence(activity = discord.Game(name="avec "+str(ctx.author)))
		await ctx.send('hey salut ' + ctx.author.mention)
		await asyncio.sleep(1)
		await ctx.send("on va jouer au jeu du nombre")
		await asyncio.sleep(1)
		await ctx.send("essais de trouver le chiffre mystère compris entre 0 et 1000")	
		await asyncio.sleep(1)
		return
	else:
		await ctx.send("une partie est déjà en cours")

@client.command()
async def stop(ctx):
	global ingame
	if ctx.author.id == joueur:

		if ingame == True:
			await ctx.send("pas de problème on arrête")
			ingame = False
			await client.change_presence(activity = None)
		else:
			await ctx.send("aucune partie n'est en cours")

@client.command()
@has_permissions(administrator=True)  
async def adminstop(ctx):
	global ingame
	if ingame == True:
		await ctx.send("partie arrêté")
		ingame = False
		await client.change_presence(activity = None)
	else:
		await ctx.send("aucune partie n'est en cours")

@client.command()
async def ownerstop(ctx):
	global ingame
	if ctx.author.id == 199161871004205056:
		if ingame == True:
			await ctx.send("partie arrêté")
			ingame = False
			await client.change_presence(activity = None)
		else:
			await ctx.send("aucune partie n'est en cours")



@client.command()
async def ping(ctx):
	dt1= ctx.message.created_at
	msg =await ctx.send("**pinging...**")
	dt2 = msg.created_at

	dt = dt2 - dt1
	ms = int(dt.microseconds /1000)
	edit = "**" +str(ms) + "**" + " ms"
	await msg.edit(content = edit)






client.run("NzAzMzE4MDk0NTkyMDgxOTYz.XqM2BA.0O4wIAVvVxk7FBsB-TgiysUmf90")


