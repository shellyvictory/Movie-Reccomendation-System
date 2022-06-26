# -*- coding: utf-8 -*-
"""Shelly Victory_Sistem Rekomendasi .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17MQsLvzGdO1xILerEDQYIl4JY0BX17dO

# *Recommender System* : Sistem Rekomendasi Movie Berdasarkan Tipe *Content Based Filter*

Analisis oleh [Shelly Victory](https://www.dicoding.com/users/victorysl)

*Dataset*: [MovieLens (small)](https://www.kaggle.com/sengzhaotoo/movielens-small)

## 1. Pendahuluan
Pada proyek ini dibuat sistem rekomendasi movie dengan tipe *content based filter* pada situs MovieLens sebagai tugas *submission* ahir pada kelas *Machine Learning* Terapan.

## 2. Data *Understanding*

### 2.1. Mengimpor Pustaka *Python* yang  Diperlukan
"""

import numpy as np
import os
import pandas as pd
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google.colab import drive
from sklearn.metrics import precision_score

"""### 2.2 Data *Loading*
Mengunduh dan mendeksripsikan *dataset*.
"""

drive.mount('/content/drive')

links = pd.read_csv('/content/drive/MyDrive/dataset/movie/links.csv')
movies = pd.read_csv('/content/drive/MyDrive/dataset/movie/movies.csv')
tags = pd.read_csv('/content/drive/MyDrive/dataset/movie/tags.csv')
ratings = pd.read_csv('/content/drive/MyDrive/dataset/movie/ratings.csv')

print('Jumlah data link movies: ', len(links.tmdbId.unique()))
print('Jumlah data judul movies: ', len(movies.title.unique()))
print('Jumlah data movie yang diberikan tag: ', len(tags.movieId.unique()))
print('Jumlah data pengguna yang setidaknya memberikan 1 kali penilaian: ', len(ratings.userId.unique()))

"""## 3. *Univariate Exploratory Data Analysis*
Secara keseluruhan, variabel-variabel yang terdapat dalam *dataset* meliputi: <br>
a. links: merupakan *dataset* yang berisikan tautan menuju sumber atau *database* untuk mengakses detail movie. <br>
b. movies: merupakan *dataset* yang berisikan judul dan genre movie. <br>
c. ratings: merupakan penilaian *user* terhadap movie. <br>
d. tags: merupakan penanda sistem online pada movie. <br>

Pada ke-4 *dataset* tersebut, fitur userId merujuk pada movieId dan data yang sama.

### 3.1.  *Links Variable*
"""

links

"""Pada *dataset* links, terdapat beberapa fitur yaitu: <br>
- movieId: ID movie yang bersifat unik pada tiap judul. <br>
- Internet Movie Database ID (imdbId): Situs Web yang menyediakan informasi mengenai movie.<br>
- The Movie Database ID (tmdbId): Database yang menyediakan informasi mengenai movie.

"""

print('Banyak data: ', len(links.movieId.unique()))
print('Banyak imdbID yang tersedia: ', len(links.imdbId.unique()))

"""### 3.2. *Movies Variable*"""

movies

"""Pada *dataset* movies, terdapat beberapa fitur: <br>
- movieId: ID movie yang bersifat unik pada tiap judul. <br>
- title: judul movie. <br>
- genres: Kategori yang menjadi salah satu dasar pengelompokkan movie.
"""

print('Banyak data judul movie: ', len(movies.title.unique()))
print('Jumlah genre: ', len(movies.genres.unique()))

"""### 3.3. *Ratings Variable*"""

ratings

"""Pada *dataset* ratings, fitur-fitur yang dimiliki adalah: <br>
- userId : ID pengguna yang bersifat unik tiap orang. <br>
- movieId: ID movie yang bersifat unik pada tiap judul. <br>
- rating: penilaian yang diberikan pengguna terhadap movie. <br>
- timestamp: stempel waktu. <br>
"""

print('Jumlah user yang memberikan penilaian: ', len(ratings.userId.unique()))
print('Jumlah movie yang diberikan penilaian: ', len(ratings.movieId.unique()))

ratings.describe()

"""### 3.4. *Tags Variable*"""

tags

"""Sama seperti *dataset* ratings, fitur-fitur yang dimiliki oleh *dataset* tags adalah: <br>
- userId : ID pengguna yang bersifat unik tiap orang. <br>
- movieId: ID movie yang bersifat unik pada tiap judul. <br>
- tag: penanda sistem online pada movie. <br>
- timestamp: stempel waktu. <br>
"""

print('Banyak data tag movie: ', len(tags.tag.unique()))
print('Jumlah movie yang diberi label: ', len(tags.movieId.unique()))

"""## 4. *Data Preparation*

### 4.1. *Data Preprocessing*

#### 4.1.1. Menggabungkan Movie
"""

# Menggabungkan Movie
# Menggabungkan seluruh movieID pada kategori movie
movie_all = np.concatenate((
    links.movieId.unique(),
    movies.movieId.unique()
))

# Mengurutkan data dan menghapus data yang sama
movie_all = np.sort(np.unique(movie_all))
print('Jumlah seluruh data movie berdasarkan movieID: ', len(movie_all))

"""#### 4.1.2. Menggabungkan Pengguna"""

# Menggabungkan seluruh userID berdasarkan kategori user
user_all = np.concatenate((
    ratings.userId.unique(),
    tags.userId.unique()
))

# mengurutkan data dan menghapus data yang sama
user_all = np.sort(np.unique(user_all))
print('Jumlah seluruh data pengguna berdasarkan userID: ', len(user_all))

"""#### 4.1.3. Menggabungkan Rating dengan Judul Movie"""

all_movie = ratings

# Menggabungkan all_movie dengan dataframe movies berdasarkan movieID
all_movie_name = pd.merge(all_movie, movies[['movieId', 'title']], on='movieId', how='left')

# print dataframe all_movie_name
all_movie_name

"""#### 4.1.4 Menggabungkan Data dengan Genre Movie"""

# Menggabungkan all_movie dengan dataframe movies berdasarkan movieID
all_movie_genre = pd.merge(all_movie_name, movies[['movieId', 'genres']], on='movieId', how='left')

# print dataframe all_movie_name
all_movie_genre

"""### 4.2. *Data Cleaning*"""

# Memeriksa missing values
all_movie_genre.isnull().sum()

# Menyamakan jenis genre movie
all_movie_genre=all_movie_genre.sort_values('movieId', ascending=True)
all_movie_genre

len(all_movie_genre.movieId.unique())

all_movie_genre.genres.unique()

all_movie_genre = all_movie_genre.drop_duplicates('movieId')
all_movie_genre

"""### 4.3. Data *Transformation*"""

preparation = all_movie_genre

# mengonversi data series 'movieID' menjadi dalam bentuk list
movies_id = preparation['movieId'].tolist()

# mengonversi data series 'title' menjadi dalam bentuk list
movies_name = preparation['title'].tolist()

# mengonversi data series 'genres' menjadi dalam bentuk list
movies_genre = preparation['genres'].tolist()

print(len(movies_id))
print(len(movies_name))
print(len(movies_genre))

# membuat dictionary untuk data 'movies_id', 'movies_name', dan 'movies_genre'
movies_new = pd.DataFrame({
    'movies_id' : movies_id,
    'movies_name' : movies_name,
    'movies_genre' : movies_genre
})
movies_new

"""## 5. *Model Development* dengan *Content Based Filtering*"""

data = movies_new
data.head(2)

"""### 5.1. TF-IDF Vectorizer"""

# inisialisasi TfidfVectorizer
tf = TfidfVectorizer()

# melakukan perhitungan idf pada datacuisine
tf.fit(data['movies_genre'])

# Mapping array dari fitur index integer ke fitur utama
tf.get_feature_names()

# melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(data['movies_genre'])

# melihat ukuran matrix tfidf
tfidf_matrix.shape

# megubah vektor tf-idf dalam bentuk matrix dengan fungsi todense()
tfidf_matrix.todense()

# membuat dataframe untuk melihat tf-idf matrix
# kolom diisi dengan jenis genre
# baris diisi dengan judul movie

pd.DataFrame(
    tfidf_matrix.todense(),
    columns=tf.get_feature_names(),
    index=data.movies_name
).sample(22, axis=1).sample(10, axis=0)

"""### 5.2. Cosine Similarity"""

# menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

# membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa nama movie
cosine_sim_df = pd.DataFrame(cosine_sim, index=data['movies_name'], columns=data['movies_name'])
print('Shape: ', cosine_sim_df.shape)

# melhat similarity matrix pada setiap movies
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""### 5.3. Mendapatkan Rekomendasi"""

def movies_recommendations(nama_movie, similarity_data=cosine_sim_df, items=data[['movies_name', 'movies_genre']], k=5):
    """
    Rekomendasi Movies berdasarkan kemiripan dataframe
 
    Parameter:
    ---
    nama_movie : tipe data string (str)
                Nama Restoran (index kemiripan dataframe)
    similarity_data : tipe data pd.DataFrame (object)
                      Kesamaan dataframe, simetrik, dengan movies sebagai 
                      indeks dan kolom
    items : tipe data pd.DataFrame (object)
            Mengandung kedua nama dan fitur lainnya yang digunakan untuk mendefinisikan kemiripan
    k : tipe data integer (int)
        Banyaknya jumlah rekomendasi yang diberikan
    ---
 
 
    Pada index ini, kita mengambil k dengan nilai similarity terbesar 
    pada index matrix yang diberikan (i).
    """
 
 
    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan    
    # Dataframe diubah menjadi numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,nama_movie].to_numpy().argpartition(
        range(-1, -k, -1))
    
    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    
    # Drop nama_movie agar nama movie yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(nama_movie, errors='ignore')
 
    return pd.DataFrame(closest).merge(items).head(k)

data[data.movies_name.eq('Billy Liar (1963)')]

movies_recommendations('Billy Liar (1963)')

rekomendasi_relevan = 5
total_rekomendasi = 5

presisi = (rekomendasi_relevan / total_rekomendasi)
presisi

"""Berdasarkan hasil rekomendasi yang muncul, seluruh movie yang disarankan memiliki genre yang sama dengan Billy Liar yaitu komedi sehingga presisi sistem bernilai 5/5 atau 100%.

## 6. Penutup
Pada proyek ini dilakukan pembuatan sistem rekomendasi dengan tipe *content based filtering* menggunakan dataset MovieLens. Pada sistem rekomendasi, fungsi tfidfvectorizer mengidentifikasi representasi penting dari fitur genre movie. Sementara itu, cosine similarity mengidentifikasi derajat kesamaan antar judul movie. Berdasarkan hasil pengembangan model, didapat model sistem rekomendasi yang memberikan saran judul movie dengan genre dan kesukaan pengguna sebelumnya. Metrik evaluasi yang digunakan adalah metrik presisi dengan nilai 1.0 atau 100%.

## 7. Referensi
*Dataset*: [MovieLens (small)](https://www.kaggle.com/sengzhaotoo/movielens-small)
"""