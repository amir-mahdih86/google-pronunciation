import os
import requests
import sys


def open_file(filename):
    if sys.platform == 'win32':
        os.startfile(filename.replace('/', '\\'))
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        os.system(f'{opener} "{filename}" > ./.log 2>&1 &')


def clear_screen():
    os.system('cls' if sys.platform == 'win32' else 'clear')


def download_audio(word):
    urls = [
        f'https://ssl.gstatic.com/dictionary/static/pronunciation/2022-03-02/audio/{word[:2]}/{word}_en_us_1.mp3',
        f'https://ssl.gstatic.com/dictionary/static/pronunciation/2021-03-01/audio/{word[:2]}/{word}_en_us_1.mp3',
        f'https://ssl.gstatic.com/dictionary/static/sounds/20160317/{word}--_us_1.mp3',
        f'https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word}--_us_1.mp3',
    ]
    for count, url in enumerate(urls, start=1):
        print(f'Downloading from url {count} ..... ', end='')
        try:
            audio = requests.get(url)
            if 'audio/mpeg' in audio.headers.get('content-type', ''):
                print('Ok')
                return audio.content
            print(f'File does not exist in url {count}')
        except requests.RequestException:
            print('Error while downloading audio. Check your internet connection.')
    return None


def main():
    os.chdir(sys.path[0])
    os.makedirs('./files', exist_ok=True)
    while True:
        clear_screen()

        word = input('Please enter a word: ')
        if not word.isalpha():
            print('Invalid input. Please enter a valid word.')
        else:
            file_name = f'./files/{word}.mp3'

            if os.path.exists(file_name):
                print('The file already exists.')
                open_file(file_name)
            else:
                audio_content = download_audio(word)
                if audio_content:
                    with open(file_name, mode='wb') as file:
                        file.write(audio_content)
                    open_file(file_name)
                else:
                    print(
                        'Word not found. If you are sure that the spelling is correct,' +
                        'word doesn\'t exist in the database.'
                    )

        if input('Would you like to check for another word? (Y/n) ').lower() not in ['y', 'yes', '']:
            break


if __name__ == '__main__':
    main()
