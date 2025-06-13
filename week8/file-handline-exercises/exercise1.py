# Exercise 1

def read_and_write_file(path):
    songs = []
    with open(path) as file:
        for line in file.readlines():
            songs.append(line.strip())
        songs.sort(key=str.lower)
        print(f'second list: {songs}')

    with open('./new-songs.txt', 'a') as file:
        for song in songs:
            file.write(song + '\n')


read_and_write_file('./songs.txt')