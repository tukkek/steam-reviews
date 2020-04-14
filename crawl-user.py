#!/usr/bin/python3
import bs4,requests,time,steam_reviews,sys

if len(sys.argv)<3:
  print(f'Usage: {sys.argv[0]} "http://steamcommunity.com/id/USER/recommended/" from-last-x-days')
  sys.exit(1)

URL=sys.argv[1]
VISITED=set()
REVIEWS=[]
DAYS=sys.argv[2]

def crawl(url):
  print(f'GET {url}')
  time.sleep(3)
  return bs4.BeautifulSoup(requests.get(url).text,features='lxml')

def browse(url):
  #print('try '+url)
  if url in VISITED:
    return
  VISITED.add(url)
  page=crawl(url)
  for review in page.select('div.review_box_content'):
    #continue
    link=review.select('a')[0]['href']
    yield {
      'id':link.split('/')[-1],
      'rating':'negative' if 'Not Recommended' in review.select('div.title')[0].get_text() else 'positive',
      'name':crawl(link).head.title.get_text().split(':: ')[-1],
    }
  #print('navigation')
  for navigation in page.select('div.workshopBrowsePagingControls'):
    #print('div')
    for link in navigation.select('a'):
      #print(f'{URL}/{link["href"]}')
      for game in browse(f'{URL}/{link["href"]}'):
        yield game
      
def write():
  output=open('result.txt','w')
  for r in steam_reviews.sort(REVIEWS):
    print(r['text'],file=output)
      
for game in browse(f'{URL}/?p=1'):
  print(f'{game["name"]} ({game["rating"]})')
  #continue
  for text,data in steam_reviews.fetch(game['id'],game['rating'],DAYS):
    data['text']=game["name"]+'\n'+text
    REVIEWS.append(data)
  write()
