#This class will get all the match data we need




import requests, json;

class Match:
	def __init__(self, match_id, api_key):
		url='https://na1.api.riotgames.com/lol/match/v4/matches/'+match_id+'?api_key='+api_key;
		getInfo = requests.get(url);
		data = getInfo.json();
		dump = json.dumps(data);

		self.game_id = match_id
		self.platform_id = data['platformId']
		self.game_creation = data['gameCreation']
		self.game_duration = data['gameDuration']
		self.queue_id = data['queueId']
		self.map_id = data['mapId']
		self.season_id = data['seasonId']
		self.game_version = data['gameVersion']
		self.game_mode = data['gameMode']
		self.game_type = data['gameType']

	def __call__(self):
		pass;

		#This method will take all the info and make it into easier to understand and useable terms
		#Mainly game_creation, game_duration, map_id, season_id, game_mode, game_type
	def printGameTime(self):
		#	// returns division with no remainder
		#	% returns division with only remainder
		gamedurationMinutes = str(self.game_duration // 60);
		gamedurationSeconds = str(self.game_duration % 60);
		print('Game Time: '+gamedurationMinutes+':'+gamedurationSeconds);

	def	gameInfo(self):
		#This method will give queue, map, season, patch, mode, and type
		givenInfo = self.jsonSearch('queueId', self.queue_id, 'map', 'queues.json');
		print('This game was played on the '+givenInfo);
		self.jsonSearch('id', self.season_id, 'season', 'seasons.json');
		givenInfo = self.jsonSearch('gameMode', self.game_mode, 'description', 'gameModes.json');
		print('An ' + givenInfo);
		givenInfo = self.jsonSearch('mapId', self.map_id, 'mapName', 'maps.json');
		print(givenInfo);
		map = self.map_id;
		season = self.season_id;
		patch = self.game_version;
		mode = self.game_mode;
		type = self.game_type;
		print('Played on patch '+patch);
	#This one may look a little fucky, but its a super easy way to change numbers to corresponding words
	#Basically, what you pass into this a, b, c, and filename.
	#a = What you have from the .json - so things like queueId or mapId
	#b = The variable that you have already initialized in __init__
	#d = The part of the .json you want to have printed out to you
	#filename is the filename you're pulling data from
	#Speaking of which, I actually downloaded the .jsons with all the relevant information
	#I figured it would be faster than pulling from a website every single time I wanted something
	#All you'll have to do is change the hardcoded path I have set ('C:\RIOT API PYTHON\extradata') to whatever you want
	def jsonSearch(self, a, b, c, filename):
		with open('C:\RIOT API PYTHON\extradata'+'/'+filename) as json_file:
			data = json.load(json_file)
			for item in data:
				if(item[a] == b):
					b = item[c]
			givenInfo = str(b);
			return givenInfo
		
		
		
		
		
		
		
			