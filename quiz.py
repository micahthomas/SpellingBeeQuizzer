import requests
import csv
import pyglet
import shutil
import subprocess
import os.path


def play_word(word):
    sound_file_name = '{}.mp3'.format(word.replace(' ', '-').lower())
    sound_file_loc = 'sounds/{}'.format(sound_file_name);
    if os.path.isfile(sound_file_loc) is False:
        response = requests.get('https://ssl.gstatic.com/dictionary/static/sounds/de/0/{}'.format(sound_file_name), stream=True)

        if not response.ok:
            print('Sound file: {} doesn\'t exist!'.format(sound_file_name))
            return
        else:
            with open(sound_file_loc, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
    subprocess.call(['mplayer', sound_file_loc], stdout=open(os.devnull, 'wb'));

def show_menu(words):
    print('What would you like to do?');
    print('1. Hear the word again')
    print('2. Show me the word')
    print('3. Next Word');
    choice = input('ENTER Answer or Choice: ').lower().strip()
    if choice == '1':
        play_word(words[0])
        return True
    if choice == '2':
        for word in words:
            print(word)
        return True
    elif choice == '3':
        return False
    else:
        correct = False
        correct_word = ''
        for word in words:
            if word.lower().strip() == choice:
                correct = True
                correct_word = word
        if correct:
            print('You got it!')
            print('Word is: {}'.format(word))
            input('ENTER to continue!')
            return False
        else:
            print('You were wrong!')
            return True
with open('words.csv', 'r') as wordfile:
    wordreader = csv.reader(wordfile);
    for words in wordreader:
        play_word(words[0])
        while show_menu(words):
            print('------------')
