import requests
import json

url = "https://api.bondradar.com/oauth/token"
client_id = input('Please input id: ')
client_secret = input('Please input secret: ')

params = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
}

token = requests.post(url=url, params=params)
headers = {"Authorization": f"Bearer {token.json()['access_token']}"}

deals = ['expected-deal', 'priced-deal']
market_data = {
    'bond': ['em', 'ig', 'hy'],
    'loan': ['af', 'cf', 'll']
}

# Get bond and loan deals data and output as json files
for deal in deals:
    for market_type, markets in market_data.items():
        for market in markets:
            try:
                endpoint = f'https://api.bondradar.com/v3/{market_type}/{market}/{deal}'
                data = requests.get(url=endpoint, headers=headers).json()
                with open(f'{market_type}_{market}_{deal}_1.txt', 'w') as text_file:
                    json.dump(data, text_file)

                count = 2
                next_endpoint = data['_links']['next']['href']
                while next_endpoint != '':
                    try:
                        next_endpoint = data['_links']['next']['href']
                        print(next_endpoint)
                        data = requests.get(url=next_endpoint, headers=headers).json()
                        with open(f'{market_type}_{market}_{deal}_{count}.txt', 'w') as text_file:
                            json.dump(data, text_file)
                        next_endpoint = data['_links']['next']['href']
                        count += 1
                    except KeyError:
                        break
            except KeyError:
                continue
