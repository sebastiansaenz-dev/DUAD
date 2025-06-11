# Exercise 1

import json

def read_pokemon_file():
    with open("./pokemon.json") as file:
        data = json.load(file)
        print(data)
        return data


def get_num_of_pokemons():
    num_pokemons = input('how many pokemons do you want to enter?: ')
    while True:
        try:
            num_pokemons = int(num_pokemons)
            break
        except:
            print('invalid input, please enter a number')
            num_pokemons = input('how many pokemons do you want to enter?: ')
    return num_pokemons

def get_pokemon_info(num_pokemons):
    pokemons = []
    counter = 0
    while counter < num_pokemons:
        temporal_dic = {}
        temporal_dic['name'] = {}
        temporal_dic['type'] = []
        temporal_dic['base'] = {}
        print('---------------------')
        temporal_dic['name']['english'] = input('Enter the name of the pokemon: ')
        temporal_dic['type'] = [input('enter the type of the pokemon: ')]
        temporal_dic['base']['HP'] = check_valid_number('enter the HP of the pokemon: ')
        temporal_dic['base']['Attack'] = check_valid_number('enter the Attack of the pokemon: ')
        temporal_dic['base']['Defense'] = check_valid_number('enter the Defense of the pokemon: ')
        temporal_dic['base']['Sp. Attack'] = check_valid_number('enter the Sp. Attack of the pokemon: ')
        temporal_dic['base']['Sp. Defense'] = check_valid_number('enter the Sp. Defense of the pokemon: ')
        temporal_dic['base']['Speed'] = check_valid_number('enter the Speed of the pokemon: ')
        pokemons.append(temporal_dic)
        counter += 1
    return pokemons


def check_valid_number(message):
    while True:
        number = input(message)
        try:
            number = int(number)
            return number
        except:
            print('invalid input, please enter a number')

def write_pokemon_json_file(data, new_pokemons):
    final_pokemons_list = []

    for pokemon in data:
        final_pokemons_list.append(pokemon)

    for pokemon in new_pokemons:
        final_pokemons_list.append(pokemon)

    print(final_pokemons_list)
    converted_list = json.dumps(final_pokemons_list, indent=4)


    with open("./pokemon.json", 'w') as file:
        file.write(converted_list)

def main():
    try:
        data = read_pokemon_file()
        num_pokemons = get_num_of_pokemons()
        pokemon_info = get_pokemon_info(num_pokemons)
        write_pokemon_json_file(data, pokemon_info)
        print(pokemon_info)
    except Exception as error:
        print('An error occurred: ')
        print(error)

if __name__ == "__main__":
    main()