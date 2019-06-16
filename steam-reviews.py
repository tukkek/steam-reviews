#!/usr/bin/python3
import requests,sys,json

URL='https://store.steampowered.com/appreviews/{}?json=1&day_range={}&review_type={}&num_per_page=100'
OUTPUT='result.txt'

if len(sys.argv)==1:
  print('Usage: ./steam-reviews.py appId [positive | negative | all] [last x days]')
  sys.exit(1)
appid=sys.argv[1]
feedback=sys.argv[2] if len(sys.argv)>=3 else 'all'
days=sys.argv[3] if len(sys.argv)>=4 else int(365.5*10)
url=URL.format(appid,days,feedback)
print(f'GET {url} ...')
reviews=requests.get(url).json()['reviews']
output=open(OUTPUT,'w')
for r in sorted(reviews,key=lambda x:int(x['votes_up']),reverse=True):
  header='RECOMMENDED' if r['voted_up'] else 'NOT RECOMMENDED'
  print(f'{header} ({r["votes_up"]} votes)\n',file=output)
  print(r['review'],file=output)
  print(f"\nLink: https://steamcommunity.com/profiles/{r['author']['steamid']}/recommended/{appid}/",file=output)
  print('-'*80,file=output)
print(f'{len(reviews)} reviews written to {OUTPUT}')
