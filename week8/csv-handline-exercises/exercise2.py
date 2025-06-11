
#Exercise 1

import csv


def get_num_of_games():
    num_games = input('how many videogames do you want to enter?: ')
    while True:
        try:
            num_games = int(num_games)
            break
        except:
            print('invalid input, please enter a number')
            num_games = input('how many videogames do you want to enter?: ')
    return num_games

def get_game_info(num_games):
    games = []
    counter = 0
    while counter < num_games:
        temporal_dic = {}
        print('---------------------')
        temporal_dic['name'] = input('Enter the name of the game: ')
        temporal_dic['gender'] = input('Enter the gender of the game: ')
        temporal_dic['developer'] = input('Enter the developer of the game: ')
        temporal_dic['ESRB rating'] = input('Enter the ESRB rating of the game: ')
        games.append(temporal_dic)
        counter += 1
    print(games)
    return games


def create_csv_file(file_path, data, headers):
    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, headers, delimiter='\t')
        writer.writeheader()
        writer.writerows(data)


def main():
    num_games = get_num_of_games()
    games = get_game_info(num_games)
    create_csv_file('games-second-version.csv', games, games[0].keys())

if __name__ == '__main__':
    main()