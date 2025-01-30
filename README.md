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

You should customize the configuration by creating a `config.py` file:

```python
# config.py
import os

import os

UPLOAD_FOLDER = "uploads"
SQLALCHEMY_DATABASE_URI = "sqlite:///nuri.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)
```

Then load it in `run.py`:

```python
project_root = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(project_root, "config.py")

app = create_app(config_path)
```

## 📦 Running in Production

Nuri uses flask so take a look at [this](https://flask.palletsprojects.com/en/stable/tutorial/deploy/). 


## API Documentation

### Authentication
All endpoints require an API key for authentication. The API key must be included in the headers:
```python
x-api-key
```

### Pagination
All endpoints use pagination. The following query parameters are available:

| Parameter | Type  | Required | Description |
|-----------|-------|----------|-------------|
| page      | int   | No       | Page number (default: 1) |
| per_page  | int   | No       | Number of items per page (default: 50) |

Example request:
```
GET /content?page=2&per_page=20
```

Response structure:
```json
{
  "data": [...],
  "pagination": {
    "current_page": 2,
    "per_page": 20,
    "total_items": 100
  }
}
```

---

### Endpoints

#### 1. Content
Retrieve content data.

**GET /content**
```
GET /content
```

##### Query Parameters
| Parameter          | Type   | Required | Description |
|-------------------|--------|----------|-------------|
| collection.alias  | string | No       | Alias of the collection |
| id               | string | No       | ID of the content |

##### Example Request
```
GET /content?collection.alias=my_collection&id=123
```

##### Example Response
```json
{
  "data": [
    {
      "id": "123",
      "title": "Sample Content",
      "collection": "my_collection"
    }
  ],
  "pagination": {
    "total_items": 1,
    "current_page": 1,
    "per_page": 10
  }
}
```

---

#### 2. Collection
Retrieve collections.

**GET /collection**
```
GET /collection
```

##### Query Parameters
| Parameter | Type   | Required | Description |
|----------|--------|----------|-------------|
| alias    | string | No       | Alias of the collection |
| id       | string | No       | ID of the collection |

##### Example Request
```
GET /collection?alias=my_collection
```

##### Example Response
```json
{
  "data": [
    {
      "id": "1",
      "alias": "my_collection",
      "name": "My Collection"
    }
  ],
  "pagination": {
    "total_items": 1,
    "current_page": 1,
    "per_page": 10
  }
}
```

---

### 3. Field
Retrieve fields.

**GET /field**
```
GET /field
```

##### Query Parameters
| Parameter | Type   | Required | Description |
|----------|--------|----------|-------------|
| alias    | string | No       | Alias of the field |
| id       | string | No       | ID of the field |

##### Example Request
```
GET /field?alias=my_field
```

##### Example Response
```json
{
  "data": [
    {
      "id": "10",
      "alias": "my_field",
      "type": "text"
    }
  ],
  "pagination": {
    "total_items": 1,
    "current_page": 1,
    "per_page": 10
  }
}
```

---

#### 4. Asset
Retrieve assets.

**GET /asset**
```
GET /asset
```

##### Query Parameters
| Parameter | Type   | Required | Description |
|----------|--------|----------|-------------|
| name     | string | No       | Name of the asset |
| id       | string | No       | ID of the asset |

##### Example Request
```
GET /asset?name=logo.png
```

##### Example Response
```json
{
  "data": [
    {
      "id": "20",
      "name": "logo.png",
      "url": "/uploads/logo.png"
    }
  ],
  "pagination": {
    "total_items": 1,
    "current_page": 1,
    "per_page": 10
  }
}
```

---

### Error Responses

| Status Code | Description |
|------------|-------------|
| 400        | Invalid request parameters |
| 401        | Invalid or missing API key |
| 404        | Resource not found |
| 500        | Internal server error |

##### Example Error Response
```json
{
  "error": "Invalid API key"
}
```

