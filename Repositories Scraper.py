import requests

repository = input('Enter a repository: ')
while True:
    extra = input('Specific language (y/n): ')
    if extra == 'y':
        language = input('Langauge: ')
        break
    elif extra == 'n':
        language = None
        break
    else:
        print('Enter y or n')
        continue
print()
if language:
    response = requests.get('https://api.github.com/search/repositories',params={'q':repository,'type':'Repositories','l':language,'s':'stars'})
else:
    response = requests.get('https://api.github.com/search/repositories',params={'q':repository,'type':'Repositories','s':'stars'})
here = False
if not response.ok:
    print('An error occurred')
json = response.json()
if len(json) == 0:
    print('No repositories were found')
elif len(json) == 1:
    here = True
else:
    done = False
    con = False
    for repo in json['items']:
        if language:
            if repo['language'] not in (language,language.title()):
                continue
        done = False
        con  = False
        while True:
            check = input(f'Is it {repo["name"]} (y/n)? ')
            if check == 'y':
                done = True
                break
            elif check == 'n':
                con = True
                break
            else:
                print('Please enter y or n.')
        if con:
            continue
        if done:
            break
    stop = False
    if done:
        while True:
            no_code = False
            response = requests.get(f'https://api.github.com/repos/{repo["full_name"]}')
            if not response.ok:
                print('An error occurred')
                break
            json = response.json()
            print()
            print(f'Name: {json["name"]}')
            print(f'Owner: {json["owner"]["login"]}')
            print(f'Stars: {json["stargazers_count"]}')
            print(f'Watchers: {json["watchers_count"]}')
            if json['fork']:
                print('Forked')
#            while True:
#                more = input('\n-------------------- More? --------------------\n')
#                if more == 'n':
#                    stop = True
#                    break
#                elif more == '':
#                    break
#                else:
#                    print('Click enter or enter the letter n.')
#                    continue
#            if stop:
#                break
            if not language:
                if json["language"] not in ('null',None):
                    print(f'Language: {json["language"]}')
            if json['language'] == None:
                no_code = True
            print(f'Forks: {json["forks_count"]}')
            if no_code:
                print('No code yet')
            break
    else:
        print('No repositories were found')
