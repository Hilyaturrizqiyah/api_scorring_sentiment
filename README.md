## Installation
Untuk installsai jalankan perintah berikut pada terminal atau cmd

```bash
pip install -r requirements.txt
```

## Running 
Untuk running pastikan file main.py model.pkl dan vectorizer.pkl ada di dalam satu folder kemudian running dengan command berikut

```bash
python main.py
```

## Cara menggunakan
Setelah aplikasi jalan maka dapat diakses melalui rest api pada 
endpoint /predict
dengan body request

```json
{
  "tweet": "Semua selesai dirusak sama kamu"
}
```
dan akan mengembalikan response dengan format
```json
{
  "tweet": "Semua selesai dirusak sama kamu",
  "sentiment": "Sadness"
}
```

untuk lebih detail akses di endpoint 
http://127.0.0.1:8000/docs