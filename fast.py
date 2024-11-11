from fastapi import FastAPI
import uvicorn
import random
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime
app = FastAPI()
data = []
last_date = datetime.today()
print('server init')
def fetch_data():
    url = "https://www.sec.gov/files/company_tickers.json"
    payload = {}
    headers = {
      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
      'priority': 'u=0, i',
      'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins)

def check_date_since_last_update():
    global data,last_date
    today = datetime.today()
    difference = today - last_date
    print(difference.days)
    if difference.days > 1:
        data = fetch_data()
        last_date = today
        print(last_date)



def search_by_ticker(data,ticker):
   l = list(data.values())
   for entry in l :
        test = entry.get('ticker')
        if test == ticker.upper() :
          cik = entry.get('cik_str')
          d = {}
          d['ticker']=ticker
          d['CIK'] = cik
          d['name'] = entry.get('title')
          return d
   return 'None Found'

@app.get("/{ticker}")
async def read_root(ticker=''):
    check_date_since_last_update()
    return search_by_ticker(data,ticker)

@app.get("/")
async def read_root():
    check_date_since_last_update()
    return data

if __name__ =='__main__' :
    data = fetch_data()
    uvicorn.run(app,host='0.0.0.0',port=8000)
