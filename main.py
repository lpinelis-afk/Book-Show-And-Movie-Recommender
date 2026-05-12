from random import randint
import time
import pandas as pd
import pyautogui as pag
movies = pd.read_csv('./CSV/movies.csv')
books = pd.read_csv('./CSV/books.csv')
shows = pd.read_csv('./CSV/shows.csv')
music = pd.read_csv('./CSV/music.csv')
games = pd.read_csv('./CSV/games.csv')
print("Ignore this")
# * Get category input from user and print results based on that input
category=input("Book/Movie/Show/Music/Games/Search> ")

# * Runs through the different categories and prints results based on user input. If search is selected, it will ask for a search term and print results based on that search term.
if category.lower() == "book":
    creator=input("Author's name> ")
    books_with_author = books[books['authors'].str.contains(creator, case=False, na=False)]

    print(books_with_author['title'] + " " + str(books_with_author['publication_date']))
#! ignore this
if category == "CONTROLMYMAUSPLEASE20": 
    for i in range(25):
        pag.moveTo(randint(10, 1000), randint(10, 1000), duration=0.25)
        time.sleep(0.5)
    pag.click(700,700)
    pag.keyDown('ctrl')
    pag.press('n')
    pag.keyUp('ctrl')
    pag.write("This is entirely harmless, I promise. This is just the easter egg. I won't do anything else. I swear.")
    time.sleep(2)
    pag.keyDown('ctrl')
    pag.press("f4")
    pag.keyUp('ctrl')
    pag.press('right')
    pag.press('enter')
    pag.press('win')
    pag.write("edge")
    pag.press('enter')
    time.sleep(2)
    pag.keyDown('ctrl')
    pag.press('t')
    pag.keyUp('ctrl')
    pag.keyDown('ctrl')
    pag.press('l')
    pag.keyUp('ctrl')
    pag.write("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1")
    pag.press('enter')
if category.lower() == "domath":
    print("1+1=3" + " " + "2+2=5" + " " + "3+3=7")
    true_or_false = input("Are these equations correct? (True/False)> ")
    if true_or_false.lower() == "true":
        print("Correct! You are a genius!")
    else:
        print("Incorrect!")
    question=input("Easy question for you: what is a+b? ")
    if question == "9820547":
        print("Correct! You are a genius!")
    else:
        print("Incorrect!")

elif category.lower() == "movie":
    creator=input("Choose Director or Actor> ")
    if creator.lower() == "director":
        creator = input("Director's Name> ")
        movies_with_director = movies[movies['director'].str.contains(creator, case=False, na=False)]
        print(movies_with_director['title'] + ", " + movies_with_director['genres'])
    else:
        creator = input("Actor's Name> ")
        movies_with_actor = movies[movies['cast'].str.contains(creator, case=False, na=False)]
        print(movies_with_actor['title'] + ", " + movies_with_actor['genres'])
elif category.lower() == "show":
    creator=input("Director's Name> ")
    shows_with_director = shows[shows['directors'].str.contains(creator, case=False, na=False)]
    print(shows_with_director['primaryTitle'] + " " + shows_with_director['genres'])
elif category.lower() == "music":
    creator = input("Artist's Name> ")
    music_with_artist = music[music['track_artist'].str.contains(creator, case=False, na=False)]
    print(music_with_artist['track_name'] + ", " + music_with_artist['track_album_name'])
elif category.lower() == "games":
    creator = input("Game's Developer> ")
    
    games_with_price = games[games['developer'].str.contains(creator, case=False, na=False)]
    print(games_with_price['name'] + ", " + games_with_price['developer'])
# * If the category is search it will ask for another category then a name, then it will print movies/shows/books with the same director/author as the one searched for. If no results are found it will print "No book/show/movie found."
elif category.lower() == "search":
    bookorshow = input("Book/Show/Movie/Music> ")
    if bookorshow.lower() == "book":
        search = input("> ")
        # * Finds the book with the right title. If there are multiple books with the same title, it will take the first one. Then it will find all books with the same author as that book and print them.
        book = books[books['title'].str.contains(search, case=False, na=False)]
        if not book.empty:
            # * Gets book author and finds all books with the same author. If there are multiple authors, it will take the first one.
            author_name = book.iloc[0]['authors']
            author =  books[books['authors'].str.contains(author_name, case=False, na=False)]
            print(author['title'] + ", " + author['authors'])
        else:
            print("No book found.")

    if bookorshow.lower() == "show":
        search = input("> ")
        # * Finds the show with the right title. If there are multiple shows with the same title, it will take the first one. Then it will find all shows with the same director as that show and print them.
        show = shows[shows['primaryTitle'].str.contains(search, case=False, na=False)]
        if not show.empty:
            # * Gets show directors and finds all shows with the same director. If there are multiple directors, it will take the first one.
            director_name = show.iloc[0]['directors'][0]
            director = shows[shows['directors'].str.contains(director_name, case=False, na=False)]
            print(director['primaryTitle'] + ", " + director['directors'])
        else:
            print("No show found.")
    if bookorshow.lower() == "movie":
        search = input("> ")
        # * Finds the movie with the right title. If there 
        # are multiple movies with the same title, it will take the first one. Then it will find all movies with the same director as that movie and print them.
        movie = movies[movies['original_title'].str.contains(search, case=False, na=False)]
        if not movie.empty:
            # * Gets movie director and finds all movies with the same director. If there are multiple directors, it will take the first one.
            director_name = movie.iloc[0]['director']
            director = movies[movies['director'].str.contains(director_name, case=False, na=False)]
            print(director['original_title'] + ", " + director['director'])
        else:
            print("No movie foundhh.")
    if bookorshow.lower() == "music":
        search = input("> ")
        # * Finds the show with the right title. If there are multiple shows with the same title, it will take the first one. Then it will find all shows with the same director as that show and print them.
        music = music[music['track_name'].str.contains(search, case=False, na=False)]
        if not music.empty:
            # * Gets music artists and finds all music with the same artist. If there are multiple artists, it will take the first one.
            danceability_rating = music.iloc[0]['danceability']
            print(music['track_name'] + ", " + music["track_artist"] + ", Danceability Rating: " + str(danceability_rating) + " out of 1" + ", " + music['playlist_genre'])
        else:
            print("No song found.")
    if bookorshow.lower() == "games":
        search = input("> ")
        # * Finds the show with the right title. If there are multiple shows with the same title, it will take the first one. Then it will find all shows with the same director as that show and print them.
        games = games[games['name'].str.contains(search, case=False, na=False)]
        if not games.empty:
            # * Gets game developers and finds all games with the same developer. If there are multiple developers, it will take the first one.
            developer = games.iloc[0]['developer']
            print(developer)
            games_with_developer = games[games['developer'].str.contains(developer, case=False, na=False)]
            print(games_with_developer)
            print(games_with_developer['name'] + ", " + games_with_developer['developer'])
        else:
            print("No game found.")
else:
    print("No Input Found, Please Try Again.")