#Imports the packages necessary.
import requests, json;

class Summoner:
	#This method is required for every
	#object that contains any data. Think 
	#of it as writing the header of an object.
	def __init__(self, sum_name, api_key):
		url='https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+sum_name+'?api_key='+api_key;
		getInfo = requests.get(url);
		data = getInfo.json();

		self.sum_name = sum_name;
		self.sum_icon = data['profileIconId'];
		self.acc_id = data['accountId'];
		self.acc_lvl = data['summonerLevel'];
		self.eId = data['id'];

		del data, url, getInfo;

		url = 'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{0}/?api_key={1}'.format(self.eId, api_key);
		response = requests.get(url);
		data = response.json();

		data = {value['queueType']: value for value in data};
		data.get('RANKED_SOLO_5x5', None);

		data2 = data['RANKED_SOLO_5x5'];

		self.wins = data2['wins'];
		self.losses = data2['losses'];
		self.tier = data2['tier'];
		self.rank = data2['rank'];
		self.lp = data2['leaguePoints'];
		self.leagueId = data2['leagueId']
		self.streak = data2['hotStreak'];
		self.inactive = data2['inactive'];

	def levelString(self):
		lvlString = str(self.acc_lvl);
		return lvlString;

	def printSummoner(self):
		lvl = self.levelString();
		wr = str(round(100*(self.wins/(self.losses+self.wins))))+'%';
		rankString = self.tier+" "+self.rank+"\n"+str(self.wins)+"W "+str(self.losses)+'L   '+str(self.lp)+" LP\n"+wr;
		statString = self.sum_name+"'s Stats";

		print(statString+'\n'+'\nLevel '+str(self.acc_lvl)+'\n'+rankString)

	def makeMatchList(self, api_key):
		matchlist = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + self.acc_id + '?api_key=' + api_key);
		matchlistJson = matchlist.json();
		return matchlistJson;
