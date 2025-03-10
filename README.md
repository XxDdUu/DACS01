# DACS01[KHMT_De_Cuong_Do_An.docx](https://github.com/user-attachments/files/19154100/KHMT_De_Cuong_Do_An.docx) //Read to know how to run
QuanLyDoanhThu/
│── 📂 backend/                  # Backend (Flask API)
│   ├── 📂 models/               # Database models (SQLAlchemy, etc.)
│   │   ├── branch.py
│   │   ├── revenue.py
│   │   └── __init__.py
│   ├── 📂 routes/               # API routes
│   │   ├── branch_routes.py
│   │   ├── revenue_routes.py
│   │   └── __init__.py
│   ├── app.py                   # Main Flask app
│   ├── config.py                # Database and environment configurations
│   ├── database.py              # MySQL connection setup
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Backend documentation
│
│── 📂 frontend/                  # Frontend (Streamlit Dashboard)
│   ├── 📂 pages/                 # Streamlit pages
│   │   ├── home.py
│   │   ├── branches.py
│   │   ├── revenue.py
│   │   └── dashboard.py
│   ├── app.py                    # Main Streamlit app
│   ├── config.py                  # Frontend settings
│   ├── requirements.txt           # Streamlit dependencies
│   └── README.md                  # Frontend documentation
│
│── 📂 scripts/                   # Scripts for database setup and testing
│   ├── init_db.py                 # Script to create MySQL tables
│   ├── seed_data.py               # Script to insert sample data
│   ├── test_api.py                # Script for API testing
│   ├── export_data.py             # Script to export reports (CSV, Excel)
│   └── README.md                  # Instructions for scripts
│
│── 📂 tests/                      # Unit and integration tests
│   ├── test_branches.py
│   ├── test_revenue.py
│   └── __init__.py
│
│── .gitignore                     # Ignore unnecessary files
│── README.md                       # Main documentation
│── docker-compose.yml              # Docker setup (if needed)
│── .env                            # Environment variables (API keys, DB credentials)
│── main.py                         # Entry point (if needed)
