# xrwvm-fullstack_developer_capstone

## Best Cars Dealership — Full-Stack Web Application

This is the capstone project for the IBM Full Stack Software Developer Professional Certificate on Coursera. It demonstrates a complete full-stack web application for a national car dealership network.

## Project Overview

**Best Cars Dealership** is a responsive web application that allows users to:
- Browse dealership locations across the United States
- View and filter dealerships by state
- Read customer reviews for each dealership
- Post reviews for visited dealerships (authenticated users)
- Sentiment analysis of reviews using NLP

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React.js, Bootstrap 4 |
| Backend | Django 4.2, Python 3.11 |
| Database | SQLite (Django), MongoDB (dealers/reviews) |
| Dealer Microservice | Node.js, Express.js |
| Sentiment Analysis | Flask, TextBlob |
| Containerization | Docker |
| Orchestration | Kubernetes |
| Deployment | IBM Cloud Code Engine |
| CI/CD | GitHub Actions |
| Version Control | Git, GitHub |

## Architecture

```
                    ┌─────────────┐
                    │   Browser   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Django    │
                    │  (Port 8000)│
                    └──┬──────┬──┘
                       │      │
          ┌────────────▼──┐ ┌─▼──────────────┐
          │ Node.js/Mongo │ │ Flask Sentiment │
          │  (Port 3000)  │ │  (Port 5000)   │
          └───────────────┘ └────────────────┘
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB
- Docker (optional)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sarthak-amrute/xrwvm-fullstack_developer_capstone.git
   cd xrwvm-fullstack_developer_capstone
   ```

2. **Install Django dependencies:**
   ```bash
   cd server
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

3. **Install Node.js microservice:**
   ```bash
   cd server/database/app
   npm install
   node app.js
   ```

4. **Install Flask sentiment service:**
   ```bash
   cd server/sentiment
   pip install -r requirements.txt
   python app.py
   ```

## Pages

- `/` — Home: Dealership listing
- `/static/About.html` — About Us page
- `/static/Contact.html` — Contact Us page
- `/register` — User registration
- `/login` — User login
- `/dealer/<id>` — Dealer detail page with reviews
- `/postreview/<id>` — Post a review (authenticated)
- `/admin/` — Django admin panel

## Author

**Sarthak Amrute**
- GitHub: [@sarthak-amrute](https://github.com/sarthak-amrute)
- Course: IBM Full Stack Software Developer — Coursera Capstone

## License

MIT License — see [LICENSE](LICENSE) for details.
