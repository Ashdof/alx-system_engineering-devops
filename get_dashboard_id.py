#!/usr/bin/python3
import requests

# Replace these with your actual API and application keys
api_key = '3a10d6fcf908711a135b398d7d668c32'
app_key = '9ab0f280692234387f2f018d83791d26eca72502'

url = 'https://api.datadoghq.com/api/v1/dashboard'
headers = {
    'DD-API-KEY': api_key,
    'DD-APPLICATION-KEY': app_key,
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    dashboards = response.json()
    for dashboard in dashboards['dashboards']:
        print(f"Dashboard Title: {dashboard['title']}, Dashboard ID: {dashboard['id']}")
else:
    print(f"Failed to retrieve dashboards: {response.status_code} - {response.text}")
