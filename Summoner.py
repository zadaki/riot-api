#Imports the packages necessary.
#Requests and JSON are here because 
#I encapsulated the API calls to the methods where
#they are made. No more random URLs lying around 
#in the main code, just the API key. 
import requests, json;

class Summoner:
	#This method is required for every
	#object that contains any data. Think 
	#of it as writing the header of an object.
	def __init__(self, sum_name, api_key):
		url='https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+sum_name+'?api_key='+api_key;
		getInfo = requests.get(url);
		data = getInfo.json();
		dump = json.dumps(data);

		#Python gets wacky here because you don't have to declare instance
		#variables for classes/objects like you do in Java. Instead, you use
		#the self. to designate that you are assigning a value to the variables
		#that belong to the Summoner object. Here, we're just storing the player
		#data that we used to have in the main program.
		self.sum_name = sum_name;
		self.sum_icon = data['profileIconId'];
		self.acc_id = data['accountId'];
		self.acc_lvl = data['summonerLevel'];

	#This method is super stupid.
	#This lets it be called. May not be necessary.
	def __call__(self):
		pass;

	#Quick little method that returns the level
	#as a string instead of a long. Was originally
	#for the printSummoner method, but may be useful.
	#It can be moved there if not.
	def levelString(self):
		lvlString = str(self.acc_lvl);
		return lvlString;

	#This method displays the player information as we
	#currently have it in a nicely formatted string to 
	#the command line.
	def printSummoner(self):
		lvl = self.levelString();
		print("\nSummoner Name: {0}\nLevel: {1}\nAccount ID: {2}\nSummoner Icon: {3}\n".format(self.sum_name, self.acc_lvl, self.acc_id, self.sum_icon));

	#Generates the match list for the player when called.
	#Takes in the API key as a parameter to send the query
	#to the API and return the data.
	def makeMatchList(self, api_key):
		matchlist = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + self.acc_id + '?api_key=' + api_key);
		matchlistJson = matchlist.json();
		return matchlistJson;
	
	def getSeasonStats(self, api_key):
		url = 'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{0}/?api_key={1}'.format(self.eId, api_key);
		grabStats = requests.get(url);

		#This grabs the API pull for Summoner ranked informatio and displays the file type after using .json() method call and displays the file.
		data = grabStats.json();
		print(type(data));
		print(data);

		#This commented segment is the converting method I've been using that works, but returns it as an empty dictionary. Ignore it for now.
		#it = iter(data);
		#convert = dict(zip(it, it));

		#print(convert);
		#print(type(convert));
