#! /usr/bin/env python3

import sys
import json
import requests
from operator import itemgetter
# sys.path.insert(1,'/usr/local/lib/python3.5/site-packages/')
from bs4 import BeautifulSoup

NHL_LINK = "https://www.ifortuna.cz/cz/sazeni/hokej/nhl"
PREMIER_LEAGUE_LINK = "https://www.ifortuna.cz/cz/sazeni/fotbal/evropska-liga"

if __name__ == '__main__' :
	response_nhl = requests.get(NHL_LINK)
	response_premier = requests.get(PREMIER_LEAGUE_LINK)

	result = {}
	for response, name in zip([response_nhl,response_premier], ['NHL', "PREMIER_LEAGUE"]):
		list_tmp = []
		c = response.content
		soup = BeautifulSoup(c, 'html.parser')
		table = soup.find_all('table', attrs={'class':'bet_table'})
		table_body = table[0].find_all('tbody')
		table_tr = table_body[0].find_all('tr')

		for i in table_tr:
			dict_tmp = {}
			bet = i.find_all('a', attrs={'class':'add_bet_link'})
			match = i['data-gtm-enhanced-ecommerce-match']
			rate = bet[0]['data-rate']

			team1 = match[:match.find('-') - 1]
			team2 = match[match.find('-') + 2:]
			dict_tmp['team1'] = team1
			dict_tmp['team2'] = team2
			dict_tmp['rate'] = rate
			list_tmp.append(dict_tmp)

		sorted_list = sorted(list_tmp, key=itemgetter('rate'))
		result[name] = sorted_list
	
	parsed = json.loads(json.dumps(result))
	with open('kurz.json', 'w') as outfile:
		json.dump(parsed, outfile, sort_keys = True, indent = 4)