#1. Помотреть документацию к API Гитхаба.
# Разобраться и вывести список всех репозиториев для конкретного пользователя.

import requests
import json

main_link='https://api.github.com/'
login='kirill50'
token='9ab7bab9f2cb6535fe508bf6bd21d88d40622379'

req=requests.get(f'{main_link}users/{login}/repos', auth=(login,token))

print(f'The user {login} have the following non-private repositories:\n')

for repo in req.json():
    if not repo['private']:
        print(repo['html_url'])

#2. Выполнить запрос методом GET к ресурсам, использующим любой тип авторизации через Postman, Python.

api_key='c82139fac94b31f6d0739eecb2528dd7'
shared_secret='0eb91cf8516ed380beb0cc6ccc2689d4'
main_music_link='http://ws.audioscrobbler.com/2.0/'
name=input('\nWrite the name of a singer to search for the similar ones:') #cher -as example
number=input('How many singers would you like to get?')

req_1=requests.get(f'{main_music_link}?method=artist.getsimilar&artist={name}&'
                   f'api_key={api_key}&autocorrect[1]&limit={number}&format=json')
if req_1.ok:
    art_data=req_1.json()

print(f'The list of {number} similar artists to {name}\n')
for artist in art_data['similarartists']['artist']:
    print(artist['name'])








