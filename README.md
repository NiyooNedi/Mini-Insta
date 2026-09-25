# Mini-Insta

An Instagram-style social media app built with Django. Users can create profiles, share photo posts, follow other users, like posts, search content, and browse a personalized feed. A token-authenticated REST API is also available for registering, logging in, and interacting with profiles and posts from external clients.

**Live demo:** [cs-webapps.bu.edu/nnedi/mini_insta/](https://cs-webapps.bu.edu/nnedi/mini_insta/)

## Features

- User registration, login, and logout with Django authentication
- Profile pages with display name, bio, and profile image
- Create, update, and delete posts with image uploads (file or URL)
- Follow / unfollow other profiles
- Like / unlike posts
- Personalized feed of posts from followed profiles
- Search profiles and posts by keyword
- REST API with token authentication for profiles, posts, feeds, and media creation

## Tech Stack

- **Backend:** Django, Python
- **API:** Django REST Framework (token auth)
- **Database:** SQLite
- **Media:** Pillow / Django `ImageField`
- **Frontend:** Django templates + CSS

## Getting Started

This app lives inside the `cs412` Django project. From the repository root:

### 1. Install dependencies

```bash
pipenv install
pipenv shell
```

If you are not using Pipenv:

```bash
pip install django pillow djangorestframework
```

### 2. Apply migrations

```bash
python manage.py migrate
```

### 3. Run the development server

```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000/mini_insta/](http://127.0.0.1:8000/mini_insta/).

## Project Structure

```
mini_insta/
├── models.py          # Profile, Post, Photo, Follow, Comment, Like
├── views.py           # Class-based views + API views
├── urls.py            # Web and API routes
├── forms.py           # Create/update forms for profiles and posts
├── serializers.py     # DRF serializers for JSON API
├── admin.py           # Django admin registration
└── templates/mini_insta/
    └── ...            # HTML templates
```

## Main Web Routes

| Path | Description |
|------|-------------|
| `/mini_insta/` | List all profiles |
| `/mini_insta/profile/<pk>` | View a profile |
| `/mini_insta/profile/` | Logged-in user's profile |
| `/mini_insta/create_profile` | Register a new account + profile |
| `/mini_insta/login/` / `logout/` | Authentication |
| `/mini_insta/profile/create_post` | Create a post |
| `/mini_insta/profile/feed` | Personalized feed |
| `/mini_insta/profile/search` | Search profiles and posts |
| `/mini_insta/post/<pk>` | View a post |
| `/mini_insta/profile/<pk>/follow` | Follow a profile |
| `/mini_insta/post/<pk>/like` | Like a post |

## API Endpoints

All authenticated API requests require an `Authorization: Token <key>` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/mini_insta/api/register/` | Register a new user |
| `POST` | `/mini_insta/api/login/` | Log in and receive a token + `profile_id` |
| `GET` | `/mini_insta/api/profiles/` | List all profiles |
| `GET` | `/mini_insta/api/profile/<pk>/` | Get one profile |
| `GET` | `/mini_insta/api/profile/<pk>/posts/` | List a profile's posts |
| `GET` | `/mini_insta/api/profile/<pk>/feed/` | Get a profile's feed |
| `POST` | `/mini_insta/api/profile/<pk>/posts/create/` | Create a post (caption + optional image) |

### Example: register and log in

```bash
# Register
curl -X POST http://127.0.0.1:8000/mini_insta/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123", "email": "alice@example.com"}'

# Log in
curl -X POST http://127.0.0.1:8000/mini_insta/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'
```

## Models

- **Profile** — linked to a Django `User`; stores username, display name, bio, and profile image
- **Post** — caption + timestamp, owned by a profile
- **Photo** — image URL and/or uploaded file attached to a post
- **Follow** — follower → followed profile relationship
- **Like** — profile liking a post
- **Comment** — text comment on a post

## Author

Niyoo Nedi (`nnedi@bu.edu`)
