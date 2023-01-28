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
  "tweet": "Aku menangis karena sedih"
}
```
dan akan mengembalikan response dengan format
```json
{
  "tweet": "Aku menangis karena sedih"
  "sentiment": "Sadness"
}
```

![Screenshot 2023-01-28 225122](https://user-images.githubusercontent.com/61138185/215276252-5d82b315-4633-4d9e-b06b-9d51058061a3.jpg)

untuk lebih detail akses di endpoint 
http://127.0.0.1:3000/docs
