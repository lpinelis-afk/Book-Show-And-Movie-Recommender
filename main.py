from random import randint
import re
import time
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    results = None
    searched = False
    if request.method == 'POST':
        creator = normalize_text(request.form.get('author', ''))
        books_with_author = books[contains_normalized(books['authors'], creator)]
        searched = True
        if not books_with_author.empty:
            results = [(row['title'], row['publication_date']) for _, row in books_with_author.iterrows()]
    return render_template('book.html', results=results, searched=searched)

@app.route('/movie', methods=['GET', 'POST'])
def movie():
    results = None
    searched = False
    if request.method == 'POST':
        role = normalize_text(request.form.get('role', ''))
        creator = normalize_text(request.form.get('creator', ''))
        searched = True
        
        if role == "director":
            movies_result = movies[contains_normalized(movies['director'], creator)]
        else:
            movies_result = movies[contains_normalized(movies['cast'], creator)]
        
        if not movies_result.empty:
            results = [(row['title'], row['genres']) for _, row in movies_result.iterrows()]
    return render_template('movie.html', results=results, searched=searched)

@app.route('/show', methods=['GET', 'POST'])
def show():
    results = None
    searched = False
    if request.method == 'POST':
        director = normalize_text(request.form.get('director', ''))
        shows_result = shows[contains_normalized(shows['directors'], director)]
        searched = True
        if not shows_result.empty:
            results = [(row['primaryTitle'], row['genres']) for _, row in shows_result.iterrows()]
    return render_template('show.html', results=results, searched=searched)

@app.route('/music', methods=['GET', 'POST'])
def music_route():
    results = None
    searched = False
    if request.method == 'POST':
        track = normalize_text(request.form.get('track', ''))
        artist = normalize_text(request.form.get('artist', ''))
        music_name_mask = contains_normalized(music['track_name'], track)
        music_artist_mask = contains_normalized(music['track_artist'], artist)
        found_music = music[music_name_mask & music_artist_mask]
        searched = True
        if not found_music.empty:
            results = [(row['track_name'], row['track_album_name']) for _, row in found_music.iterrows()]
    return render_template('music.html', results=results, searched=searched)

@app.route('/games', methods=['GET', 'POST'])
def games_route():
    results = None
    searched = False
    if request.method == 'POST':
        developer = normalize_text(request.form.get('developer', ''))
        games_result = games[contains_normalized(games['developer'], developer)]
        searched = True
        if not games_result.empty:
            results = [(row['name'], row['developer']) for _, row in games_result.iterrows()]
    return render_template('games.html', results=results, searched=searched)

@app.route('/boardgames', methods=['GET', 'POST'])
def boardgames_route():
    results = None
    columns = []
    searched = False
    if request.method == 'POST':
        search_type = normalize_text(request.form.get('search_type', ''))
        search_query = normalize_text(request.form.get('query', ''))
        searched = True
        
        if search_type == "name":
            found_boardgames = boardgames[contains_normalized(boardgames['Name'], search_query)]
            columns = ['Name', 'Year Published', 'Rating Average', 'Complexity Average']
        elif search_type == "mechanics":
            found_boardgames = boardgames[contains_normalized(boardgames['Mechanics'], search_query)]
            columns = ['Name', 'Mechanics', 'Rating Average']
        elif search_type == "domains":
            found_boardgames = boardgames[contains_normalized(boardgames['Domains'], search_query)]
            columns = ['Name', 'Domains', 'Rating Average']
        else:
            found_boardgames = pd.DataFrame()
        
        if not found_boardgames.empty:
            results = [tuple(row[col] for col in columns) for _, row in found_boardgames.iterrows()]
    return render_template('boardgames.html', results=results, columns=columns, searched=searched)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = None
    columns = []
    category_display = ""
    searched = False
    if request.method == 'POST':
        category = normalize_text(request.form.get('category', ''))
        query = normalize_text(request.form.get('query', ''))
        searched = True
        
        if category == "book":
            found = books[contains_normalized(books['title'], query)]
            if not found.empty:
                author_name = found.iloc[0]['authors']
                results_df = books[contains_normalized(books['authors'], author_name)]
                columns = ['title', 'authors']
                category_display = "Book"
            else:
                results_df = pd.DataFrame()
        elif category == "show":
            found = shows[contains_normalized(shows['primaryTitle'], query)]
            if not found.empty:
                director_name = found.iloc[0]['directors']
                results_df = shows[contains_normalized(shows['directors'], director_name)]
                columns = ['primaryTitle', 'directors']
                category_display = "Show"
            else:
                results_df = pd.DataFrame()
        elif category == "movie":
            found = movies[contains_normalized(movies['original_title'], query)]
            if not found.empty:
                director_name = found.iloc[0]['director']
                results_df = movies[contains_normalized(movies['director'], director_name)]
                columns = ['original_title', 'director']
                category_display = "Movie"
            else:
                results_df = pd.DataFrame()
        elif category == "music":
            track = normalize_text(request.form.get('track', ''))
            artist = normalize_text(request.form.get('artist', ''))
            music_name_mask = contains_normalized(music['track_name'], track)
            music_artist_mask = contains_normalized(music['track_artist'], artist)
            found = music[music_name_mask & music_artist_mask]
            if not found.empty:
                results_df = found
                columns = ['track_name', 'track_artist', 'danceability', 'playlist_genre']
                category_display = "Music"
            else:
                results_df = pd.DataFrame()
        elif category == "games":
            found = games[contains_normalized(games['name'], query)]
            if not found.empty:
                developer = found.iloc[0]['developer']
                results_df = games[contains_normalized(games['developer'], developer)]
                columns = ['name', 'developer']
                category_display = "Games"
            else:
                results_df = pd.DataFrame()
        elif category == "boardgames":
            found = boardgames[contains_normalized(boardgames['Name'], query)]
            if not found.empty:
                mechanics = found.iloc[0]['Mechanics']
                results_df = boardgames[contains_normalized(boardgames['Mechanics'], mechanics)]
                columns = ['Name', 'Mechanics', 'Rating Average']
                category_display = "Board Games"
            else:
                results_df = pd.DataFrame()
        else:
            results_df = pd.DataFrame()
        
        if not results_df.empty and columns:
            results = [tuple(row[col] for col in columns) for _, row in results_df.iterrows()]
    return render_template('search.html', results=results, columns=columns, category_display=category_display, searched=searched)

if __name__ == '__main__':
    app.run(debug=True)