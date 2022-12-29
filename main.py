import os
import json
import requests

# comparison function used for incrementing game scores.
# works essentially as a signum function:
# Returns:
#   0 if equal
#  -1 if negative (a < b)
#   1 if positive (a > b)
# https://en.wikipedia.org/wiki/Sign_function
cmp = lambda a, b: (a > b) - (a < b)

# The API is split up as [base_url] / '[year_of_game]' / '[game_date]'
# The reason I declare the API URL as its own variable is so I can
# concatenate the base url with other values for specific game information.
url_base = "http://football-frenzy.s3-website.eu-north-1.amazonaws.com/api"
req_base = requests.get(url_base)
data = json.loads(req_base.text)

seasons = data["seasons"]

while True:
    os.system("cls") if os.name == "nt" else os.system("clear")
    print("List | List available seasons.")
    print("View | View table for season.")
    print("Quit | Exits the program.")

    user_input = input("selection > ")

    if user_input == "list":
        print(*seasons, sep = '\n')

    elif user_input == "view":
        year = input("Enter year [1980..2018]: ")

        if year not in seasons:
            print("Invalid year provided")
            continue
            
        if year in seasons:
            url_season  = f"{url_base}/{year}"
            req_season  = requests.get(url_season)
            data_season = json.loads(req_season.text)

            teams = {team:0 for team in data_season["teams"]}

            for game_day in data_season["gamedays"]:
                url_game_day  = f"{url_base}/{year}/{game_day}"
                req_game_day  = requests.get(url_game_day)
                data_game_day = json.loads(req_game_day.text)

                for game in data_game_day["games"]:
                    data_team_home = game["score"]["home"]
                    data_team_away = game["score"]["away"]

                    name_team_home = data_team_home["team"]
                    name_team_away = data_team_away["team"]

                    teams[name_team_home] += [0,1,3][cmp(data_team_home["goals"], data_team_away["goals"]) + 1]
                    teams[name_team_away] += [0,1,3][cmp(data_team_away["goals"], data_team_home["goals"]) + 1]

            for key, value in sorted(teams.items()):
                print(key, value)

    elif user_input == "quit":
        break

    else:
        print("Invalid option provided.")

    input("Press enter to continue")
