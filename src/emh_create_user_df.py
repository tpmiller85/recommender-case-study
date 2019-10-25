import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.float_format = '{:,.2f}'.format

df_movies = pd.read_csv('../data/movies/movies.csv')
df_links =  pd.read_csv('../data/movies/links.csv')
df_ratings =  pd.read_csv('../data/movies/ratings.csv')
df_tags =  pd.read_csv('../data/movies/tags.csv')

#Merge ratings with movies
df_ratings = pd.merge(df_ratings, df_movies, how='left', on='movieId')

#count how many times did a user watch a movie within a genre
df_ratings['genres'] = df_ratings['genres'].str.lower()
df_ratings['Drama'] = 0
df_ratings['Comedy'] = 0
df_ratings['Romance'] = 0
df_ratings['Action'] = 0

df_ratings['Drama'][df_ratings['genres'].str.contains('drama')]=1
df_ratings['Comedy'][df_ratings['genres'].str.contains('comedy')]=1
df_ratings['Romance'][df_ratings['genres'].str.contains('romance')]=1
df_ratings['Action'][df_ratings['genres'].str.contains('action')]=1

#convert to datetime
df_ratings['rating_year'] = pd.to_datetime(df_ratings['timestamp'], unit='s').dt.year
df_ratings['date'] = pd.to_datetime(df_ratings['timestamp'], unit='s')

#group by user and get aggregate info
df_ratings_users = df_ratings.groupby('userId')

df_user_info = pd.concat([pd.DataFrame(df_ratings_users.count()['rating'].rename('rating_count')), 
                         pd.DataFrame(df_ratings_users.mean()['rating'].rename('rating_average')), 
                         pd.DataFrame(df_ratings_users.min()['date'].rename('start_date')), 
                         pd.DataFrame(df_ratings_users.max()['date'].rename('most_recent_date')),
                         pd.DataFrame(df_ratings_users.sum()['Drama'].rename('Drama_Count')),
                         pd.DataFrame(df_ratings_users.sum()['Comedy'].rename('Comedy_Count')),
                         pd.DataFrame(df_ratings_users.sum()['Romance'].rename('Romance_Count')),
                         pd.DataFrame(df_ratings_users.sum()['Action'].rename('Action_Count'))], 
                         axis=1)

#get average rating for genre for each user
def genre_average_rating(df, df_to_join, genre):
    df_group = df[df['genres'].str.contains(genre)].groupby(['userId'])
    df_group.mean()['rating']
    df_new = pd.DataFrame(df_group.mean()['rating'].rename('rating_average_%s' % genre))
    return df_to_join.merge(df_new, on='userId')

df_user_info = genre_average_rating(df_ratings, df_user_info, 'drama')
df_user_info = genre_average_rating(df_ratings, df_user_info, 'comedy')
df_user_info = genre_average_rating(df_ratings, df_user_info, 'romance')
df_user_info = genre_average_rating(df_ratings, df_user_info, 'action')
df_user_info.head()