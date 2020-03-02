#Imports the needed libraries.
#Collections lets us use the Counter method,
#which counts the number of unique instances in
#data structures.
import requests, json, collections;

#Summoner is a module object, which means
#it normally cannot be called. To get around
#this, we import it straight from its file instead
#of importing the whole file. (Idk man,  it works.)
from Summoner import Summoner;
from Match import Match;
print("Enter your Summoner Name: ");
sum_name = input();

#The API Key is the only truly necessary initial
#variable needed because of encapsulation with
#the Summoner method. Hop over there for details.
apikey='RGAPI-225dd131-5096-4c70-945e-d961682f3844';

#Makes a method call to initialize a new Summoner object
#Also uses a method I wrote that displays the Summoner information
thisSummoner = Summoner(sum_name, apikey);
thisSummoner.printSummoner();

#Pulls the champion names and IDs to create a list object
champ = requests.get('https://ddragon.leagueoflegends.com/cdn/10.4.1/data/en_US/champion.json');
champlist = champ.json();
CLIST = json.dumps(champlist);
champData = champlist['data'];

#Storing the champion keys and names in parallel arrays
#I think this should be switched to a list of tuples
ckey = [];
cid = [];
for x in champData:
	ckey.append(champData[x]['key']);
	cid.append(champData[x]['name']);

#This makes a call to the Summoner object previously
#initialized for it to make a list of its match history
#with a method written in Summoner.
matchlistRead = thisSummoner.makeMatchList(apikey);
#to hold the gameIds of the last 100 games
matchlistIds = [];

CHAMPS_PLAYED = [];
CHAMPION_ID = '';
x=0;
#I hate this block of code. It makes my head hurt.
i = 0;
for match in matchlistRead["matches"]:
	CHAMPION_ID = match['champion'];
	if (i < 10):
		matchlistIds.append(match['gameId']);
		i += 1;
	for key in ckey:
		if (str(CHAMPION_ID) == str(key)):
			x = ckey.index(key);
			CHAMPS_PLAYED.append(cid[x]);

#Displays the list of champions played in 
#the last x amount of games.
print('These are the champions that '+sum_name+' has played in the last '+str(len(CHAMPS_PLAYED))+' games: ');
print(str(CHAMPS_PLAYED)+"\n");
CHAMPIONS = []
CHAMPIONS = CHAMPS_PLAYED;

#Sorts the list and is able to display how
#many games played on each(!). Not pretty. Will work for now.
#CHAMPS_PLAYED.sort();
test = collections.Counter(CHAMPS_PLAYED);
print("These are the number of games played on each unique champion in the last "+str(len(CHAMPS_PLAYED))+" games: \n"+str(test));
#test print

print(matchlistIds);
listMatchIndex = 0;
listMatchStats = [];
print("This is CHAMPSPLAYED:");
print(CHAMPIONS);

incre = 0;

while(incre < len(matchlistIds)):
	thisMatch = Match(matchlistIds[incre], apikey, sum_name);
	print("Game "+str(incre)+":"+"\n"+CHAMPIONS[incre]);
	thisMatch.gameInfo();
	incre += 1;


#This little bit is just thrown together to see how far back you can get matches, which seems to be roughly march 2018
#Just a general test for seeing how adding extra parameters to a URL works, overall pretty simple
#One interesting thing to note is that if your beginning index is larger than the number of matches it has recorded it doesn't really care, it just keep going through the loop without any kind of errors
"""
CHAMPIONESEPLAYED = [];
beginIndex = 5000;
while(beginIndex > 0):
	if(sum_name == "Random1227"):
		accountID = '2IqZ3-UXzFCyihgopqFNVH4iCplNeortvBQw5VnwjYJqRg';
	elif(sum_name == "Storm Raizer"):
		accountID = 'xDjAQMxnnd1hEIN9UrljVpsob_UcPhn0LS-U1guHDIIPYNI';
	elif(sum_name == "Zadaki"):
		accountID = 'ObF4h-ATOFjzfKkCPKvzujy1Xe5ziftI2Do8oumlXj9Pf8I';
	elif(sum_name == "cba"):
		accountID = 'fv17L-51zsd2bB6F9hJK_355iRVg4_uWA02u7io9LbZ936wTWlmUYpXo';


	farmatchlist = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/'+str(accountID)+'?beginIndex='+str(beginIndex)+'&api_key=RGAPI-4ebc6daa-1109-4f8c-9f60-65f1f5efe1eb')
	farmatchlist2 = farmatchlist.json();

	x=0;
	#I hate this block of code. It makes my head hurt.
	i = 0;
	for match in farmatchlist2["matches"]:
		CHAMPION_ID = match['champion'];
		for key in ckey:
			if (str(CHAMPION_ID) == str(key)):
				x = ckey.index(key);
				CHAMPIONESEPLAYED.append(cid[x]);
	beginIndex = beginIndex -100;
	test2 = collections.Counter(CHAMPIONESEPLAYED);
print('These are the champions played in the last '+str(len(CHAMPIONESEPLAYED))+'\n'+str(test2));
"""

