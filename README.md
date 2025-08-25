https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white

# 🧑‍🤝‍🧑 Social Media App

A **Django-based Social Media Web Application** that allows users to share posts, like & comment, and interact via **real-time chat**.  
This project demonstrates the integration of Django with WebSockets for live messaging, along with essential social media features.

---

## 🚀 Features

- 🔐 **User Authentication** (Signup, Login, Logout, Profile Management)  
- 📰 **Feed System** (Users can post text/images and view others' posts)  
- ❤️ **Like & Comment** (Engage with posts in real time)  
- 💬 **Real-Time Chat** (One-to-one and group chat using Django Channels/WebSockets)  
- 🔔 **Notifications** (For likes, comments, and chat messages)  
- 📱 **Responsive UI** (Mobile & desktop-friendly using Bootstrap/HTML/CSS)

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Database:** SQLite (development) / PostgreSQL (production)  
- **Real-time Chat:** Django Channels, WebSockets, Redis  
- **Authentication:** Django AllAuth / JWT  
- **Deployment:** Heroku / AWS / Railway  

---

## 📂 Project Structure

instaclone/
│
├── instagram_clone/      # Main project settings
├── media/                # Uploaded user images & media files
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── accounts/             # User authentication & profiles
├── posts/                # Post, likes, and comments logic
├── chat/                 # Real-time chat app
└── manage.py             # Django management script


---

## ⚙️ Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/KatariyaVyomesh/instaclone.git
   cd instaclone


2. ## Run Migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate

3. ## Run Server
   ```bash
   python manage.py runserver
