<p align="center"><img src="/logo.svg" alt="Logo"></p>

---

Nuri CMS is a lightweight API-based content management system.
It is designed to be minimalistic and easy to set up.

## 🚀 Installation

You can install Nuri CMS via pip:

```bash
pip install nuri-cms
```

## 📌 Getting Started

To start using Nuri CMS, create a simple `run.py` file:

```python
from nuri import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
```

Run the application:

```bash
python run.py
```

The application will be available at `http://localhost:8000`.

⚠️ There will be an admin user with username admin@example.com" and password admin123.
Make sure you create your own admin user and delete the demouser!

## 🛠 Configuration (Optional)

You can customize the configuration by creating a `config.py` file:

```python
# config.py
SQLALCHEMY_DATABASE_URI = "sqlite:///my_nuri.db"
SECRET_KEY = "my_secret_key"
```

Then load it in `run.py`:

```python
app.config.from_pyfile("config.py")
```

## 📦 Running in Production

Nuri uses flask so take a look at (this)[https://flask.palletsprojects.com/en/stable/tutorial/deploy/]. 
