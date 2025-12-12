# 🎯 Product Review Analyzer

Aplikasi web untuk menganalisis review produk menggunakan AI (Hugging Face + Google Gemini).

## ✨ Fitur

- Analisis sentiment review (Positive/Negative/Neutral)
- Ekstraksi key points otomatis
- Simpan hasil ke database PostgreSQL
- Tampilkan history semua review

## 🛠️ Tech Stack

**Backend:** Python Pyramid, SQLAlchemy, PostgreSQL  
**Frontend:** React.js, Pure CSS  
**AI:** Hugging Face API, Google Gemini API

## 📦 Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- [Hugging Face API Key](https://huggingface.co/settings/tokens)
- [Google Gemini API Key](https://makersuite.google.com/app/apikey)

## 🚀 Installation

### 1. Setup Database

```bash
psql -U postgres
CREATE DATABASE review_analyzer;
\q
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac: venv\Scripts\activate untuk Windows

pip install -e ".[testing]"
pip install huggingface_hub google-generativeai psycopg2-binary requests

# Set API Keys
export HUGGINGFACE_API_KEY="your_key_here"
export GEMINI_API_KEY="your_key_here"

# Edit development.ini - ubah sqlalchemy.url dengan kredensial PostgreSQL Anda
# sqlalchemy.url = postgresql://postgres:password@localhost/review_analyzer

# Initialize database
initialize_backend_db development.ini

# Run server
pserve development.ini --reload
```

Backend running di: `http://localhost:6542`

### 3. Setup Frontend

```bash
cd frontend
npm install
npm start
```

Frontend running di: `http://localhost:3000`

## 📡 API Endpoints

**POST** `/api/analyze-review` - Analyze review
```json
{
  "product_name": "iPhone 15 Pro",
  "review_text": "Amazing camera quality..."
}
```

**GET** `/api/reviews` - Get all reviews

## 📁 Struktur Project

```
product-review-analyzer/
├── backend/
│   ├── backend/
│   │   ├── models/
│   │   │   ├── meta.py
│   │   │   └── review.py
│   │   ├── views/
│   │   │   └── review_views.py
│   │   ├── __init__.py
│   │   └── routes.py
│   └── development.ini
│
└── frontend/
    ├── src/
    │   ├── App.js
    │   └── App.css
    └── package.json
```

## 🐛 Troubleshooting

**Database connection error:**
```bash
sudo systemctl start postgresql  # Linux
brew services start postgresql   # Mac
```

**react-scripts not found:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Import error backend:**
- Pastikan file `meta.py` dan `review.py` ada di `backend/backend/models/`

## 📝 License

MIT License

---
