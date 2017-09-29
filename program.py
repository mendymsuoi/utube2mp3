#!/usr/bin/env python

# import all the library used
import re, urllib, os, sys
from bs4 import BeautifulSoup

# determine python version
version = sys.version_info[0]

# set user_input and import modules for correct encodeversion of python
if version == 2:  # python 2.x
    user_input = raw_input
    import urllib2
    urlopen = urllib2.urlopen  # open a url
    encode = urllib.urlencode  # encode a search line
    retrieve = urllib.urlretrieve  # retrieve url info
    cleanup = urllib.urlcleanup()  # cleanup url cache

else:  # python 3.x
    user_input = input
    import urllib.request
    import urllib.parse
    urlopen = urllib.request.urlopen
    encode = urllib.parse.urlencode
    retrieve = urllib.request.urlretrieve
    cleanup = urllib.request.urlcleanup()



# clear the terminal screen
def screen_clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# function to retrieve video title from provided link
def video_title(url):
    try:
        webpage = urlopen(url).read()
        title = str(webpage).split('<title>')[1].split('</title>')[0]
    except:
        title = 'Youtube Song'

    return title


# find out what the user wants to do
def prompt():
    # userr prompt to ask mode
    print ('''\t\t\t Select A mode
    [1] Download from a list
    [2] Download from direct entry
    [3] Search and select
    Press any other key from keyboard to exit''')

    choice = user_input('>>> ')
    return str(choice)


# download from a list of songs or links
def list_download():
    fileName = user_input('fileName(with extension): ')  # get the file name to be opened

    # find the file and set fhand as handler
    try:
        fhand = open(fileName, 'r')
    except IOError:
        print('File does not exist')
        exit(1)

    # Iterating over the lines in file
    for song in fhand:
        single_download(song)

    fhand.close()


# download directly with a song name or link
def single_download(song=None):
    if not(song):
        song = user_input('Enter the song name or youtube link: ')  # get the song name from user

    if "youtube.com/" not in song:
        # try to get the search result and exit upon error
        try:
            query_string = encode({"search_query" : song})
            html_content = urlopen("http://www.youtube.com/results?" + query_string)

            if version == 3:  # if using python 3.x
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            else:  # if using python 2.x
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read())
        except:
            print('Network Error')
            return None
        
        # make command that will be later executed
        command = 'youtube-dl --embed-thumbnail --no-warnings --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" ' + search_results[0]
        
    else:      # For a link
        # make command that will be later executed
        command = 'youtube-dl --embed-thumbnail --no-warnings --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" ' + song[song.find("=")+1:]
        song=video_title(song)

    try:       # Try downloading song
        print('Downloading %s' % song)
        os.system(command)
    except:
        print('Error downloading %s' % song)
        return None
        

# program exit
def exit(code):
    print('\nExiting....')
    print('\nHave a good day.')
    sys.exit(code)


# main guts of the program
def main():
    try:
        screen_clear()
        print('Created by Mendy Mishulovin')
        choice = prompt()

        try:
            if choice == '1':
                list_download()
            elif choice == '2':
                single_download()
            elif choice=='3':
                choose(links("http://youtube.com/results?"+encode({"search_query" : input()})))
        except NameError:
            exit(1)
    except KeyboardInterrupt:
        exit(1)
    exit(1)
class m:
    def __init__(self, name, link, number, channel):
        self.name=name
        self.link=link
        self.number=number
        self.channel=channel
def links(url):
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, "html5lib", from_encoding=resp.info().get_param('charset'))
    links=[]
    number=0
    for link in soup.select("#results div a.yt-uix-tile-link"):
        #.find_all('*', href=True):
        links.append(m(link.string,link['href'], number, None))
        number+=1
    return links
def choose(results):
    for link in results:
        print(link.number)
        print(link.name)
    single_download(results[int(input())].link)
if __name__ == '__main__':
    main()  # run the main program
    exit(0)  # exit the program
