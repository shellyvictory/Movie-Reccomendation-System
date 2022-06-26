# Laporan Proyek Machine Learning - [Shelly Victory](https://www.linkedin.com/in/shellyvictory/)

## *Project Overview*
Sistem rekomendasi merupakan salah satu aplikasi yang sukses dalam menyaring banyaknya informasi tersedia di internet. Tujuan digunakannya sistem rekomendasi adalah untuk menyarankan produk atau item berupa buku, movie, berita, CD, hingga DVD kepada pengguna berdasarkan riwayat preferensi mereka. [Zang et. al.,](https://www.sciencedirect.com/science/article/abs/pii/S1045926X14000901) (2014), membuat sistem rekomendasi movie dengan tipe *hybrid-based dataset* Movielens. Hasil dari sistem yang dibuat yaitu menghasilkan rekomendasi yang lebih terpersonalisasi namun proses pembuatannya cukup rumit dibanding metode lain. Pada proyek ini, akan dibuat sistem rekomendasi movie dengan tipe *content-based filtering*.

## *Business Understanding*
Hampir seluruh situs di internet dan aplikasi menggunakan sistem rekomendasi. Pada zaman dimana perkembangan teknologi dan aliran informasi terjadi sangat cepat, efisiensi penerimaan informasi menjadi salah satu faktor untuk menarik lebih banyak pengguna. Oleh karena itu, sistem rekomendasi harus mampu memberikan saran produk lainnya kepada pengguna yang sesuai dengan selera dan pengalaman mereka untuk meningkatkan penjualan produk.
Perkembangan pesat industri film membuat produksi movie dengan berbagai genre semakin meningkat. Tiap movie memiliki keuinkan dan target pasarnya tersendiri sehingga promosi atau rekomendasi yang tepat sasaran akan membuat suatu movie lebih banyak ditonton. Disisi lain, pengguna akan mendapat rekomendasi beberapa movie yang belum pernah mereka tonton sesuai selera dalam waktu singkat.

### *Problem Statements*
Pada analisis ini, bagaimana cara membuat sistem rekomendasi movie yang dengan teknik *content-based filtering*?

### *Goals*
*Goals* yang ingin dicapai pada proyek ini yaitu mengetahui cara pembuatan sistem rekomendasi yang dipersonalisasi dengan teknik *content-based filtering*.

### *Solution Statments*
Berdasarkan permasalahan yang dijelaskan sebelumnya, proyek ini akan menggunakan pendekatan sistem rekomendasi *content-based filtering*. Tipe sistem rekomendasi ini menggunakan kemiripan antar item yang disukai oleh pengguna sebelumnya untuk menawarkan item lain yang belum pernah diketahui pengguna yang sesuai dengan kesukaan mereka.

## Data Understanding
Pada analisis ini, dataset yang digunakan merupakan [MovieLens (small)](https://www.kaggle.com/sengzhaotoo/movielens-small) yang memuat data rating (0,5 - 5) oleh pengguna pada tiap movie. Selain itu, pengguna yang tercantum setidaknya telah memberikan rating pada 20 movies. *Dataset* memiliki beberapa variabel seperti:

1. links: merupakan dataset yang berisikan tautan menuju sumber atau database untuk mengakses detail movie.
2. movies: merupakan dataset yang berisikan judul dan genre movie.
3. ratings: merupakan penilaian user terhadap movie.
4. tags: merupakan dataset dengan fitur dan isi yang sama dengan ratings.

Pada ke-4 dataset tersebut, fitur userId merujuk pada movieId dan data yang sama. Tidak terdapat data yang hilang pada seluruh dataset. Dataset ini memuat penilaian movie dimulai tanggal 09 Januari 1995 - 16 Oktober 2016.

### Links Variable
Pada dataset links, terdapat beberapa fitur yaitu:

- movieId: ID movie yang bersifat unik pada tiap judul.
- Internet Movie Database ID (imdbId): Situs Web yang menyediakan informasi mengenai movie.
- The Movie Database ID (tmdbId): Database yang menyediakan informasi mengenai movie.

### Movies Variable
Pada *dataset* movies, terdapat beberapa fitur:

- movieId: ID movie yang bersifat unik pada tiap judul.
- title: judul movie.
- genres: Kategori yang menjadi salah satu dasar pengelompokkan movie.

### Ratings Variable
Rating movie memiliki skala 1-5 dengan rating minimum adalah 0,5 dan maksimum 5. Terdapat 671 jumlah pengguna (unik) yang memberikan penilaian terhadap movie. Pada dataset ratings, fitur-fitur yang dimiliki adalah:

- userId : ID pengguna yang bersifat unik tiap orang.
- movieId: ID movie yang bersifat unik pada tiap judul.
- rating: penilaian yang diberikan pengguna terhadap movie.
- timestamp: stempel waktu.

### Tags Variable
Fitur-fitur yang dimiliki adalah:
- userId : ID pengguna yang bersifat unik tiap orang.
- movieId: ID movie yang bersifat unik pada tiap judul.
- tag: label pada movie.
- timestamp: stempel waktu.



## Data Preparation
Merupakan bagian yang terdiri dari beberapa tahapan untuk melakukan pengecekan data.


### Data Preprocessing
Bagian ini dilakukan dengan beberapa tahapan, meliputi:

1. Menggabungkan seluruh movieId pada dataset links dan movies lalu mengurutkan dan menghapus data yang sama.
2. Menggabungkan seluruh userId pada dataset ratings dan tags lalu mengurutkan dan menghapus data yang sama.
3. Menggabungkan rating pada dataset ratings dengan judul movie yang berasal dari dataset movies.
4. Menggabungkan data sebelumnya dengan genre movie yang berasal dari dataset movies.

### Data Cleaning
Persiapan data dilakukan dengan beberapa teknik yaitu:
1. Memeriksa kembali missing values. Data dengan nilai yang hilang akan menurunkan performa sistem rekomendasi. Pada dataframe tidak ditemukan missing values sehinga dilanjutkan ke tahap selanjutnya.
2. Menyamakan jenis genre movie dengan menghapus data movieId yang duplikat, lalu melihat rincian genre pada movie. Movie dengan judul yang sama memiliki kemungkinan untuk memiliki genre yang berbeda sehingga perlu diatasi menyamakan jenis genrenya. Pengecekan dilakukan dengan melihat jenis-jenis genre dan tidak ditemukan genre dengan movie yang tidak sesuai.

### Data Transformation
1. Melakukan konversi data series 'movieID', 'title', dan 'genres' menjadi dalam bentuk list dengan fungsi tolist() dari library numpy. Sebelumnya, urutkan data berdasarkan fitur movieId lalu hilangkan data dengan movieId duplikat.
2. Setelah mengonversi data genre dalam bentuk list, dibuat dictionary untuk menentukan pasangan key value pada data 'movies_id', 'movies_name', dan 'movies_genre'. Dataframe siap untuk dilakukan pemodelan.

## Modeling
1. TF-IDF Vectorizer berfungsi untuk menemukan representasi fitur penting dari setiap kategori genre. Tahapan yang dilakukan meliputi inisialisasi TfidfVectorizer, melakukan perhitungan idf pada data genre dan mapping array dari fitur index integer ke fitur nama. Selanjutnya, dilakukan fit lalu transformasi dalam bentuk matrix. Ukuran matrix yang diperoleh adalah ( , ). Setelah itu, buat df dengan kolom berisikan genre dan baris berisi nama movie.
2. Menggunakan fungsi cosine_similarity dari library sklearn untuk menghitung derajat kesamaan antar nama movie. Selanjutnya melihat matriks kesamaan setiap movie dengan menampilkan judul movie. 
3. Tahap berikutnya yaitu mendapatkan rekomendasi dengan memasang parameter sebagai berikut:
- Nama_movie: judul movie (indeks kemiripan df)
- Similarity_data: Dataframe mengenai similarity yang telah didefinisikan sebelumnya.
- Items: Nama dan fitur yang digunakan untuk mendifinisikan kemiripan, yaitu 'movies_name' dan movies_genre'.
- k: Banyak rekomendasi yang ingin didapatkan

Kode yang telah dibuat selanjutnya diterapkan untuk menemukan rekomendasi judul movie yang sesuai dengan Billy Liar (1963).
 Movies_id | Movies_name | Movies_genre|
------------ | ------------- | -----------|
4687 |	Billy Liar (1963) | Comedy

Billy Liar merupakan movie dengan genre komedi. Berdasarkan sistem rekomendasi yang telah dirancang, output yang dihasilkan harusnya memiliki genre yang sama.

Movies_name |Movies_genre|	
------------ | ------------- | 
Bring It On (2000) |Comedy|
Private School (1983) |Comedy|
Punk's Dead: SLC Punk! 2 (2014) |Comedy|
Porky's Revenge (1985) |Comedy|
Death at a Funeral (2007)	|Comedy|

Pada tabel di atas hasil rekomendasi movie berdasarkan Billy Liar seluruhnya memiliki genre yang sama sehingga sistem rekomendasi bekerja dengan baik.

## Evaluasi
Evaluasi dilakukan dengan metrik presisi dengan rumus di bawah. Pada proyek ini, tingkat presisi dihitung dengan menghitung perbandingan antara rekomendasi genre yang sama dengan total rekomendasi yang diberikan kepada pengguna.

![Precision Matrix](https://miro.medium.com/max/552/1*5PvyyMvH5n42XICQrlXOzw.png)

Pada tabel output modeling, dapat diketahui bahwa seluruh rekomendasi memiliki genre yang sama dengan judul movie yang dimasukkan.Berdasarkan rumus di atas, hasil rekomendasi yang diperoleh bernilai sempurna atau 100%. 

**---Ini adalah bagian akhir laporan---**
