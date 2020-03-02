#This class will get all the match data we need
#Newest things - KDA, Final Builds

import requests, json;

class Match:
	def __init__(self, match_id, api_key, sum_name):
		url='https://na1.api.riotgames.com/lol/match/v4/matches/'+str(match_id)+'?api_key='+api_key;
		getInfo = requests.get(url);
		data = getInfo.json();
		dump = json.dumps(data);

		self.game_id = match_id
		#self.platform_id = data['platformId']
		self.game_creation = data['gameCreation']
		self.game_duration = data['gameDuration']
		self.queue_id = data['queueId']
		self.map_id = data['mapId']
		self.season_id = data['seasonId']
		self.game_version = data['gameVersion']
		self.game_mode = data['gameMode']
		self.game_type = data['gameType']
		
		self.sum_name = sum_name;
		
		self.team = data['teams']
		self.participants = data['participants']
		self.participantIdentities = data['participantIdentities']
	
	def __call__(self):
		pass;

		#This method will take all the info and make it into easier to understand and useable terms
		#Mainly game_creation, game_duration, map_id, season_id, game_mode, game_type
	def printGameTime(self):
		#	// returns division with no remainder
		#	% returns division with only remainder
		#	simple way to get the gametime in a readable format
		gamedurationMinutes = str(self.game_duration // 60);
		gamedurationSeconds = str(self.game_duration % 60);
		gameTime = 'Game Time: '+gamedurationMinutes+':'+gamedurationSeconds;
		return gameTime

		#This is the method I want to use to call all other methods, at least for now. It allows the information to be more easily formatted all in one place. 
	def	gameInfo(self):
		map = self.jsonSearch('queueId', self.queue_id, 'map', 'queues.json');
		description = self.jsonSearch('queueId', self.queue_id, 'description', 'queues.json');
		gametype = self.game_type;
		gameTime = self.printGameTime();
		season = self.season_id;
		patch = self.game_version;
		mode = self.game_mode;
		type = self.game_type;
		
		
		PlayerInfo = self.findPlayer(self.sum_name);
		KDA = self.findKDA(PlayerInfo);
		Build = self.findFinalBuild(PlayerInfo);
		print(str(Build)+'\n'+str(KDA)+'\n'+str(gameTime)+"\n"+str(map)+"\n"+str(description)+"\n"+str(gametype)+"\n");
		
	#This one may look a little fucky, but its a super easy way to change numbers to corresponding words inside a .json file (or the other way around, as long as you give it what you want)
	#jsonSearch(self, a, b, c, filename): 
	#Basically, what you pass into this is a, b, c, and filename.
	#a = What you have from the .json - so things like queueId or mapId
	#b = The variable that you have already initialized in __init__
	#c = The part of the .json you want to have printed out to you
	#filename is the filename you're pulling data from
	#Speaking of which, I actually downloaded the .jsons with all the relevant information
	#I figured it would be faster than pulling from a website every single time I wanted something
	#All you'll have to do is change the hardcoded path I have set ('C:\RIOT API PYTHON\extradata') to whatever you want, alternatively this could probably be changed back to a URL fairly easily
	def jsonSearch(self, a, b, c, filename):
		with open('C:\RIOT API PYTHON\extradata'+'/'+filename) as json_file:
			data = json.load(json_file)
		for item in data:
			if(item[a] == b):
				b = item[c]
		givenInfo = str(b);
		return givenInfo
	
	#This is the big boy method
	#First, it goes through participantIdentities and compares each player with the summoner name the user inputs and gets the participant identity
	#Then it goes through participants, uses that participant ID until it finds the info from the participant
	#The pInfo in that second for loop holds just about all the information we could want about the match, besides in depth timeline that would need a different API call to retrieve
	#This is what can return the rune info, KDAs, who won, and literally so much else
	def findPlayer(self, sum_name):
		pIdentity = 0;
		for participant in self.participantIdentities:
			if(participant['player']['summonerName'] == sum_name):
				pIdentity = participant['participantId'];
				break;
		pInfo = [];
		for participant in self.participants:
			if(pIdentity == participant['participantId']):
				pInfo = participant;
		return pInfo;
		
	#uses pInfo to gather KDA
	#very straight forward
	def findKDA(self, pInfo):
		kills = pInfo['stats']['kills'];
		deaths = pInfo['stats']['deaths'];
		assists = pInfo['stats']['assists'];
		if(deaths == 0):
			KDA = (str(kills)+'/0/'+str(assists)+'\nPerfect');
		else:
			KDA = (str(kills)+'/'+str(deaths)+'/'+str(assists)+'\n'+str((kills+assists) / deaths));	
		return KDA;
		
	#uses pInfo to gather the final build
	#This one is a little more complex than the KDA one,
	#the line 'for a,b in data['data'].items():' is trouble spot, and it allowed the items in the json to be broken up into their name and the information contained within, allowing me to translate to names.
	#There is a good chance that this can be simplified by using the jsonSearch() method, but for now its good enough
	#One thing to note, I believe we could get in depth and sort the list by various things such as itemId number or by gold value if we wanted
	def findFinalBuild(self, pInfo):
		finalBuild = [];
		with open('C:\RIOT API PYTHON\extradata'+'/item.json') as json_file:
			data = json.load(json_file)
		x = 0;
		while(x < 7):
			finalBuild.append(pInfo['stats']['item'+str(x)]);
			for a,b in data['data'].items():
				if(str(a) == str(finalBuild[x])):
					finalBuild[x] = b['name'];
					x=x+1;
					break;
				elif(finalBuild[x] == 0):
					x=x+1;
					break;
		return finalBuild;