# Social Media App

A small social network built with Django: users can post photos, comment and like, send and accept friend requests, set a status, and chat with friends in real time over WebSockets.

## Features

- **Accounts.** Register, log in and log out. Each user has a profile with a picture, date of birth and status message.
- **Posts.** Create image posts, comment and like. The home feed also suggests people to add.
- **Friends.** Search for users, then send, accept, decline, cancel or remove friend requests.
- **Real-time chat.** Named chat rooms powered by Django Channels and Redis, with message history and online presence.
- **REST API.** Django REST Framework endpoints for profiles, posts, comments, likes, friends and chat. They're listed at `/rest-apis`.

## Tech stack

- **Backend:** Django 4.2, Django REST Framework, Django Channels + Daphne (ASGI), channels-redis
- **Frontend:** Django templates, Tailwind CSS (via `django-tailwind`), vanilla JS
- **Database:** SQLite
- **Testing / data:** Django test framework, factory_boy, Faker

## Project structure

```
authentication/   login, logout, registration
userprofile/      profiles and status updates
post/             posts, comments, likes
friends/          friend requests and search
chat/             chat rooms, WebSocket consumer, message history
socialmedia/      project settings, ASGI routing, populate_db command
theme/            Tailwind theme app
templates/        HTML templates
static/js/        page scripts (posts, friends, chat, profile)
data_files/       CSV seed data used by populate_db
```

## Getting started

### Prerequisites

- Python 3.11
- Redis running on `localhost:6379` (needed for chat). The quickest way to get it is with Docker:

  ```bash
  docker run -d -p 6379:6379 redis
  ```

### Install and run

```bash
git clone https://github.com/gshudhanshu/socialmedia.git
cd socialmedia

python -m venv venv
# Windows: venv\Scripts\activate
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000. Daphne is installed as the first app, so `runserver` serves both HTTP and the chat WebSockets.

### Sample data

The repo ships with a pre-populated `db.sqlite3`. To reset it from the CSV files in `data_files/`, run:

```bash
python manage.py populate_db
```

> **Note:** `populate_db` deletes all existing users, posts, friends and chat data before loading the CSVs.

### Tests

```bash
python manage.py test
```

## API endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/profiles` | GET | All user profiles |
| `/api/profiles/<user_id>` | GET | A single profile |
| `/api/user-posts/<user_id>` | GET, POST | Posts by a user |
| `/api/posts/<post_id>` | GET | A single post |
| `/api/posts/<post_id>/comments` | GET, POST | Comments on a post |
| `/api/posts/<post_id>/like` | GET, POST | Likes on a post |
| `/api/friend-list/<user_id>` | GET, POST | A user's friends |
| `/api/friend-requests-received/<user_id>` | GET | Pending requests received |
| `/api/friend-requests-sent/<user_id>` | GET | Pending requests sent |
| `/api/chat` | GET, POST | Chat rooms |
| `/api/chat/<room_name>` | GET, POST | Messages in a room |
