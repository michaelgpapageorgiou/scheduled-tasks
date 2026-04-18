import requests,os
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters_stock_site={
    'function':'TIME_SERIES_DAILY',
    'symbol':STOCK_NAME,
    'apikey':os.environ.get('STOCK_API_KEY'),
}
parameters_news_site={
    'q':COMPANY_NAME,
    'language':'en',
    'searchIn':'title,description',
    'apikey':os.environ.get('NEWS_API_KEY'),
}

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response_stock=requests.get(STOCK_ENDPOINT, params=parameters_stock_site)
response_stock.raise_for_status()
data=response_stock.json()
days=data['Time Series (Daily)']
print(days)
closing_prices=[close['4. close'] for (days,close) in days.items()]
#print(closing_prices)
new_price=float(closing_prices[0])
old_price=float(closing_prices[1])
difference=(new_price-old_price)/old_price*100
print(difference)
if difference<0:
    symbol='🔻'
else:
    symbol="🔺"
percent=round(abs(difference))
print(percent)
if percent >= 5 :
    response_news=requests.get(NEWS_ENDPOINT,params=parameters_news_site)
    response_news.raise_for_status()
    news=response_news.json()
    articles=news['articles'][:3]
    #print(articles)
    ready_to_send=[(arti['title'], arti['description']) for arti in articles]
    print(ready_to_send)
    client = Client(os.environ.get('ACCOUNT_SID'),os.environ.get('AUTH_TOKEN'))
    for title, description in ready_to_send:
        message=client.messages.create(
            from_=f"whatsapp:{os.environ.get('WHATSAPP_NUMBER')}",
            body=f'{STOCK_NAME}: {symbol} {percent}%\nHeadline: {title}.\n\nBrief: {description}',
            to=f"whatsapp:{os.environ.get('MY_NUMBER')}"
            )
        print(message.status)

