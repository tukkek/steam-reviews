#!/usr/bin/python3
import requests,sys,json,datetime

URL='https://store.steampowered.com/appreviews/{}?json=1&day_range={}&review_type={}&num_per_page=100'
OUTPUT='result.txt'
TODAY=datetime.datetime.now()

def sort(reviews):
  return sorted(reviews,key=lambda x:int(x['votes_up']),reverse=True)

def fetch(appid,feedback,days):
  url=URL.format(appid,days,feedback)
  print(f'GET {url} ...')
  for r in sort(requests.get(url).json()['reviews']):
    date=datetime.datetime.fromtimestamp(int(r['timestamp_created']))
    if TODAY-date>datetime.timedelta(days=int(days)):
      continue #don't trust Steam day_range API
    header='RECOMMENDED' if r['voted_up'] else 'NOT RECOMMENDED'
    playtime=round(int(r["author"]["playtime_forever"])/60)
    text=f'{header} ({r["votes_up"]} votes, {playtime} total hours played)\n'
    text+=f'\n{r["review"]}\n'
    text+=f"\nLink: https://steamcommunity.com/profiles/{r['author']['steamid']}/recommended/{appid}/\n"
    text+='-'*80
    yield text,r

if __name__=='__main__':
  if len(sys.argv)==1:
    print('Usage: ./steam-reviews.py appId [positive | negative | all] [last x days]')
    sys.exit(1)
  appid=sys.argv[1]
  feedback=sys.argv[2] if len(sys.argv)>=3 else 'all'
  days=sys.argv[3] if len(sys.argv)>=4 else int(365.5*10)
  output=open(OUTPUT,'w')
  count=0
  for text,data in fetch(appid,feedback,days):
    print(text,file=output)
    count+=1
  print(f'{count} reviews written to {OUTPUT}')
