import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def create_vectorized_genre_df(df,dfgenre):
    df_new = pd.merge(df, dfgenre, on='movieId', how='outer').drop(columns=['timestamp']).dropna()
    df_new['genres']=df_new['genres'].apply(lambda x: x.replace('|',',').replace('-','').replace(' ',''))
    count_vect = CountVectorizer()
    arr = count_vect.fit_transform(df_new['genres']).todense()
    cols=count_vect.get_feature_names().copy()
    df_genre_vectorized=pd.DataFrame(arr,columns=cols)
    df_new=df_new.join(df_genre_vectorized,lsuffix='i')
    return df_new.drop(columns='genres')

def avg_genre_rating(df_new):
    avg_list=[]
    genres_list=df_new.iloc[:,4:].columns.tolist()
    for genre in genres_list:
        avg=df_new[df_new[genre]==1].groupby('movieId')['rating'].mean().mean()
        avg_list.append(avg)
    for i, word in enumerate(genres_list):
        if word == 'nogenreslisted':
            genres_list[i] = 'not listed'
        if word == 'filmnoir':
            genres_list[i] = 'film noir'
    return genres_list,avg_list
    
def avg_genre_count(df_new):
    avg_list=[]
    genres_list=df_new.iloc[:,4:].columns.tolist()
    for genre in genres_list:
        avg=df_new[df_new[genre]==1].groupby('movieId')['rating'].count().count()
        avg_list.append(avg)
    for i, word in enumerate(genres_list):
        if word == 'nogenreslisted':
            genres_list[i] = 'not listed'
        if word == 'filmnoir':
            genres_list[i] = 'film noir'
    return genres_list,avg_list