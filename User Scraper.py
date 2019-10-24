import requests

person = input('Enter a user: ')
while True:
    yes = input('Specific language (y/n): ')
    if yes == 'y':
        language = input('Langauge: ')
        break
    elif yes == 'n':
        language = None
        break
    else:
        print('Enter y or n')
        continue
print()
response = requests.get(
    'https://api.github.com/search/users',
    params={'q': person},
)
if not response.ok:
    print('An error occurred')

json_response = response.json()
if len(json_response) == 0:
    yay = True
    print('No users were found')
else:
    while True:
        here = False
        yay  = False
        for user in json_response['items']:
            if len(json_response['items']) == 1:
                check = 'y'
                here = True
            else:
                check = input(f'Is the user {user["login"]} (y/n)? ')
            if check == 'y':
                yay = True
                norm = requests.get('https://api.github.com/users/'+user['login'])
                norm = norm.json()
                if not here:
                    if norm['public_repos'] != 0:
                        print(f'\n{user["login"]} has {norm["public_repos"]} repostories')
                else:
                    print(f'{user["login"]} has {norm["public_repos"]} repostories')
                response = requests.get('https://api.github.com/users/'+user['login']+'/repos')
                if not response.ok:
                    print('An error occurred')
                    break
                json = response.json()
                count = None
                for repo in json:
                    if language:
                        if repo['language'] not in (language.title(),language):
                            continue
                    count = True
                    print(f'{repo["name"]}', end='')
                    if repo["description"]:
                        print(f': {repo["description"]}')
                    else:
                        print()
                    if repo["language"]:
                        if yes == 'n':
                            print(f'Language: {repo["language"]}')
                        code = True
                    else:
                        code = None
                    print(f'Forks: {repo["forks_count"]}')
                    print(f'Stars: {repo["stargazers_count"]}')
                    print(f'Watchers: {repo["watchers_count"]}')
                    if not code:
                        if repo["fork"] == 'true':
                            print()
                        print('No code yet')
                    if repo["fork"] == 'true':
                        print('Forked')
                    print()
                if not count:
                    print('No repostories were found.')
                    break
            elif check == 'n':
                continue
            else:
                print('Enter y or n\n')
        break
if not yay:
    print('There are no more users left')
