import pandas as pd
import sys
movies = pd.read_csv('./CSV/movies.csv')
books = pd.read_csv('./CSV/books.csv')
shows = pd.read_csv('./CSV/shows.csv')

category=input("Book/Movie/Show/Search> ")



# Filter the dataframe where the 'cast' column contains the actor's name

# Print the titles of those movies
if category.lower() == "book":
    creator=input("Author's name> ")
    books_with_author = books[books['authors'].str.contains(creator, case=False, na=False)]

    print(books_with_author['title'] + " " + str(books_with_author['publication_date']))
elif category.lower() == "movie":
    creator=input("Choose Director or Actor> ")
    if creator.lower() == "director":
        creator = input("Director's Name> ")
        movies_with_director = movies[movies['director'].str.contains(creator, case=False, na=False)]
        print(movies_with_director['title'] + " " + movies_with_director['genres'])
    else:
        creator = input("Actor's Name> ")
        movies_with_actor = movies[movies['cast'].str.contains(creator, case=False, na=False)]
        print(movies_with_actor['title'] + " " + movies_with_actor['genres'])
elif category.lower() == "show":
    creator=input("Director's Name> ")
    shows_with_director = shows[shows['directors'].str.contains(creator, case=False, na=False)]
    print(shows_with_director['primaryTitle'] + " " + shows_with_director['genres'])
elif category.lower() == "search":
    bookorshow = input("Book/Show/Movie> ")
    if bookorshow.lower() == "book":
        search = input("> ")
        book = books[books['title'].str.contains(search, case=False, na=False)]
        if not book.empty:
            author_name = book.iloc[0]['authors']
            author =  books[books['authors'].str.contains(author_name, case=False, na=False)]
            print(author['title'] + ", " + author['authors'])
        else:
            print("No book found.")

    if bookorshow.lower() == "show":
        search = input("> ")
        show = shows[shows['primaryTitle'].str.contains(search, case=False, na=False)]
        if not show.empty:
            director_name = show.iloc[0]['directors']
            director = shows[shows['directors'].str.contains(director_name, case=False, na=False)]
            print(director['primaryTitle'] + ", " + director['directors'])
        else:
            print("No show found.")
    if bookorshow.lower() == "movie":
        search = input("> ")
        movie = movies[movies['original_title'].str.contains(search, case=False, na=False)]
        if not movie.empty:
            director_name = movie.iloc[0]['director']
            director = movies[movies['director'].str.contains(director_name, case=False, na=False)]
            print(director['original_title'] + ", " + director['director'])
        else:
            print("No movie found.")
else:
    print("No Input Found, Please Try Again.")
