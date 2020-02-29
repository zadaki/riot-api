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
apikey='RGAPI-6aa1bffb-74b9-44e0-91f1-8339913cd2ef';

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
	if (i < 2):
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


#Sorts the list and is able to display how
#many games played on each(!). Not pretty. Will work for now.
CHAMPS_PLAYED.sort();
test = collections.Counter(CHAMPS_PLAYED);
print("These are the number of games played on each unique champion in the last "+str(len(CHAMPS_PLAYED))+" games: \n"+str(test));
#test print
print(matchlistIds);
listMatchIndex = 0;
listMatchStats = [];
for matchid in matchlistIds:
	responsematchstats = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/'+str(matchlistIds[0])+'?api_key='+apikey)
	listMatchJson = responsematchstats.json();
	listMatchStats.append(listMatchJson);
listMatchStat = str(3310067183);

thisMatch = Match(listMatchStat, apikey);

#print(Summoner.);

#print(gameduration);

#print(listMatchStat);

thisMatch.gameInfo();



