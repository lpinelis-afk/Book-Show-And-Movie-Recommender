from random import randint
import re
import time
import pandas as pd
import pyautogui as pag
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
movies = pd.read_csv('./CSV/movies.csv')
books = pd.read_csv('./CSV/books.csv')
shows = pd.read_csv('./CSV/shows.csv')
music = pd.read_csv('./CSV/music.csv')
games = pd.read_csv('./CSV/games.csv')
boardgames = pd.read_csv('./CSV/bgg_dataset.csv', sep=';', decimal=',')
# normalize text so punctuation and capitalization are ignored
def normalize_text(text):
    if not isinstance(text, str):
        return ""
    cleaned = re.sub(r'[^a-z0-9\s]', '', text.lower())
    return ' '.join(cleaned.split())

# normalize user input directly
def normalize_input(prompt):
    return normalize_text(input(prompt))

# print DataFrame rows without index alignment spaces
def print_rows(df, columns):
    for _, row in df[columns].iterrows():
        print(", ".join(str(row[col]) for col in columns))

# use a normalized contains check for dataframe string columns
def contains_normalized(series, query):
    query = normalize_text(query)
    if query == "":
        return pd.Series([False] * len(series))
    normalized_series = (
        series.astype(str)
        .str.lower()
        .str.replace(r'[^a-z0-9\s]', '', regex=True)
    )
    return normalized_series.str.contains(re.escape(query), na=False)

raw_category = input("Book/Movie/Show/Music/Games/Boardgames/Search> ")
category = normalize_text(raw_category)

if raw_category == "CONTROLMYMAUSPLEASE20":
    for i in range(25):
        pag.moveTo(randint(10, 1000), randint(10, 1000), duration=0.25)
        time.sleep(0.5)
    pag.click(700, 700)
    pag.keyDown('ctrl')
    pag.press('n')
    pag.keyUp('ctrl')
    pag.write("This is entirely harmless, I promise. This is just the easter egg. I won't do anything else. I swear.")
    time.sleep(2)
    pag.keyDown('ctrl')
    pag.press('f4')
    pag.keyUp('ctrl')
    pag.press('right')
    pag.press('enter')
    pag.press('win')
    pag.write('edge')
    pag.press('enter')
    time.sleep(2)
    pag.keyDown('ctrl')
    pag.press('t')
    pag.keyUp('ctrl')
    pag.keyDown('ctrl')
    pag.press('l')
    pag.keyUp('ctrl')
    pag.write('https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1')
    pag.press('enter')

elif category == "domath":
    print("1+1=3 2+2=5 3+3=7")
    true_or_false = normalize_input("Are these equations correct? (True/False)> ")
    if true_or_false == "true":
        print("Correct! You are a genius!")
    else:
        print("Incorrect!")
    question = input("Easy question for you: what is a+b? ")
    if question == "9820547":
        print("Correct! You are a genius!")
    else:
        print("Incorrect!")

elif category == "book":
    creator = normalize_input("Author's name> ")
    books_with_author = books[contains_normalized(books['authors'], creator)]
    print_rows(books_with_author, ['title', 'publication_date'])

elif category == "movie": 
    creator_role = normalize_input("Choose Director or Actor> ")
    if creator_role == "director":
        creator = normalize_input("Director's Name> ")
        movies_with_director = movies[contains_normalized(movies['director'], creator)]
        print_rows(movies_with_director, ['title', 'genres'])
    else:
        creator = normalize_input("Actor's Name> ")
        movies_with_actor = movies[contains_normalized(movies['cast'], creator)]
        print_rows(movies_with_actor, ['title', 'genres'])

elif category == "show": 
    creator = normalize_input("Director's Name> ")
    shows_with_director = shows[contains_normalized(shows['directors'], creator)]
    print_rows(shows_with_director, ['primaryTitle', 'genres'])

elif category == "music": 
    creator = normalize_input("Artist's Name> ")
    music_with_artist = music[contains_normalized(music['track_artist'], creator)]
    print_rows(music_with_artist, ['track_name', 'track_album_name'])

elif category == "games": 
    creator = normalize_input("Game's Developer> ")
    games_with_price = games[contains_normalized(games['developer'], creator)]
    print_rows(games_with_price, ['name', 'developer'])

elif category == "boardgames":
    search_type = normalize_input("Search by Name/Mechanics/Domains> ")
    search_query = normalize_input("> ")
    
    if search_type == "name":
        found_boardgames = boardgames[contains_normalized(boardgames['Name'], search_query)]
        if not found_boardgames.empty:
            print_rows(found_boardgames, ['Name', 'Year Published', 'Rating Average', 'Complexity Average'])
        else:
            print("No board game found.")
    elif search_type == "mechanics":
        found_boardgames = boardgames[contains_normalized(boardgames['Mechanics'], search_query)]
        if not found_boardgames.empty:
            print_rows(found_boardgames, ['Name', 'Mechanics', 'Rating Average'])
        else:
            print("No board game found with that mechanic.")
    elif search_type == "domains":
        found_boardgames = boardgames[contains_normalized(boardgames['Domains'], search_query)]
        if not found_boardgames.empty:
            print_rows(found_boardgames, ['Name', 'Domains', 'Rating Average'])
        else:
            print("No board game found in that domain.")
    else:
        print("Invalid search type.")

elif category == "search": 
    bookorshow = normalize_input("Book/Show/Movie/Music/Games/Boardgames> ")

    if bookorshow == "book":
        search = normalize_input("> ")
        found_book = books[contains_normalized(books['title'], search)]
        if not found_book.empty:
            author_name = found_book.iloc[0]['authors']
            author_books = books[contains_normalized(books['authors'], author_name)]
            print_rows(author_books, ['title', 'authors'])
        else:
            print("No book found.")

    elif bookorshow == "show":
        search = normalize_input("> ")
        found_show = shows[contains_normalized(shows['primaryTitle'], search)]
        if not found_show.empty:
            director_name = found_show.iloc[0]['directors']
            director_shows = shows[contains_normalized(shows['directors'], director_name)]
            print_rows(director_shows, ['primaryTitle', 'directors'])
        else:
            print("No show found.")

    elif bookorshow == "movie":
        search = normalize_input("> ")
        found_movie = movies[contains_normalized(movies['original_title'], search)]
        if not found_movie.empty:
            director_name = found_movie.iloc[0]['director']
            director_movies = movies[contains_normalized(movies['director'], director_name)]
            print_rows(director_movies, ['original_title', 'director'])
        else:
            print("No movie found.")

    elif bookorshow == "music":
        search = normalize_input("Song Name> ")
        author = normalize_input("Artist's Name> ")
        music_name_mask = contains_normalized(music['track_name'], search)
        music_artist_mask = contains_normalized(music['track_artist'], author)
        found_music = music[music_name_mask & music_artist_mask]
        if not found_music.empty:
            print_rows(found_music, ['track_name', 'track_artist', 'danceability', 'playlist_genre'])
        else:
            print("No song found.")

    elif bookorshow == "games":
        search = normalize_input("> ")
        found_games = games[contains_normalized(games['name'], search)]
        if not found_games.empty:
            developer = found_games.iloc[0]['developer']
            games_with_developer = games[contains_normalized(games['developer'], developer)]
            print_rows(games_with_developer, ['name', 'developer'])
        else:
            print("No game found.")

    elif bookorshow == "boardgames":
        search = normalize_input("> ")
        found_boardgame = boardgames[contains_normalized(boardgames['Name'], search)]
        if not found_boardgame.empty:
            mechanics = found_boardgame.iloc[0]['Mechanics']
            boardgames_with_mechanics = boardgames[contains_normalized(boardgames['Mechanics'], mechanics)]
            print_rows(boardgames_with_mechanics, ['Name', 'Mechanics', 'Rating Average'])
        else:
            print("No board game found.")

    else:
        print("No valid search category found.")

else:
    print("No Input Found, Please Try Again.")