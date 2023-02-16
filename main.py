import os
import json
import requests

# comparison function used for finding game outcomes.
# works essentially as a signum function:
# Returns:
#   0 if equal
#  -1 if negative (a < b)
#   1 if positive (a > b)
# https://en.wikipedia.org/wiki/Sign_function
cmp = lambda a, b: (a > b) - (a < b)

# Function used to compile a team's point total
# Works on the basis that a win is worth 3 points and a draw 1 point.
# Return value is the point total as a number.
get_points = lambda team: team["W"] * 3 + team["D"]

# The API is split up as [base_url] / '[year_of_game]' / '[game_date]'
# The reason I declare the API URL as its own variable is so I can
# concatenate the base url with other values for specific information retrieval.
URL_BASE = "http://football-frenzy.s3-website.eu-north-1.amazonaws.com/api"
REQ_BASE = requests.get(URL_BASE)
data = json.loads(REQ_BASE.text)

seasons = data["seasons"]

while True:
    os.system("cls") if os.name == "nt" else os.system("clear")
    print("List │ List available seasons.")
    print("View │ View table for season.")
    print("Quit │ Exits the program.")

    user_input = input("selection > ").lower()

    if user_input == "list":
        print(*seasons, sep="\n")

    elif user_input == "view":
        year = input("Enter year [1980..2018]: ")

        if year not in seasons:
            print("Invalid year provided")
            input("Press enter to continue")
            continue

        if year in seasons:
            URL_SEASON = f"{URL_BASE}/{year}"
            REQ_SEASON = requests.get(URL_SEASON)
            DATA_SEASON = json.loads(REQ_SEASON.text)

            teams = {team: {"W": 0, "D": 0, "L": 0} for team in DATA_SEASON["teams"]}

            for game_day in DATA_SEASON["gamedays"]:
                URL_GAMEDAY = f"{URL_BASE}/{year}/{game_day}"
                REQ_GAMEDAY = requests.get(URL_GAMEDAY)
                DATA_GAMEDAY = json.loads(REQ_GAMEDAY.text)

                for game in DATA_GAMEDAY["games"]:
                    DATA_HOME = game["score"]["home"]
                    DATA_AWAY = game["score"]["away"]

                    TEAM_HOME = DATA_HOME["team"]
                    TEAM_AWAY = DATA_AWAY["team"]

                    # cmp returns -1, 0, or 1
                    # +1 makes the results into 0, 1, 2 which I can use as indeces.
                    result = cmp(DATA_HOME["goals"], DATA_AWAY["goals"]) + 1

                    teams[TEAM_HOME][["L", "D", "W"][result]] += 1
                    teams[TEAM_AWAY][["L", "D", "W"][2 - result]] += 1

            name_fill = max([len(team) for team in DATA_SEASON["teams"]])

            print(
                "Team".ljust(name_fill)
                + f'  {"W": >3}  {"D": >3}  {"L": >3}  {"P": >3}'
            )

            print("  ".join(["─" * name_fill, "─" * 3, "─" * 3, "─" * 3, "─" * 3]))

            for key, value in sorted(
                teams.items(), key=lambda item: get_points(item[1]), reverse=True
            ):
                print(
                    "  ".join(
                        [
                            key.ljust(name_fill),
                            str(value["W"]).rjust(3),
                            str(value["D"]).rjust(3),
                            str(value["L"]).rjust(3),
                            str(get_points(value)).rjust(3),
                        ]
                    )
                )

    elif user_input == "quit":
        break

    else:
        print("Invalid option provided.")

    input("Press enter to continue")
