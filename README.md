# Movie Store - Full Stack Application

A full-stack movie rental application with Flask REST API backend and Next.js frontend with Clerk authentication.

## Project Structure

```
movie-store/
├── backend/          # Flask REST API
│   ├── app/          # Application code
│   ├── migrations/   # Database migrations
│   └── Dockerfile    # Backend container config
├── frontend/         # Next.js application
│   ├── app/          # Next.js App Router pages
│   ├── middleware.ts # Clerk authentication middleware
│   └── Dockerfile    # Frontend container config
└── docker-compose.yml # Multi-service orchestration
```

## Backend API Features
 - list movies using `GET`: endpoint api/v1/movies
 - search movies using `GET`: endpoint api/v1/movies/search and using the genre parameter to find movies in a specified category.
 - get the details of a movie by id using `GET`: endpoint api/v1/movies/\<int:movie_id>
 - update the details of a movie using `PATCH`: endpoint api/v1/movies/\<int:movie_id> use genre, title, year or director params to update the relative fields.
 - create a movie using `POST`: endpoint api/v1/movies use the above parameters and also title and director are mandatory.
 - delete a movie using `DELETE`: endpoint api/v1/movies/\<int:movie_id>
 
 - list categories using `GET`: endpoint api/v1/categories to view all available categories. If genre param is specified all movies under that category will be also listed. 
   If genre equals 'all', then all movies will be listed under their category.
 - create a new category using `POST`: endpoint api/v1/categories. You must specify the genre param for a successful creation.
 - delete a new category using `DELETE`: endpoint api/v1/categories. You must specify the genre or the id param for a successful deletion.
 
 - rent a movie using using `POST`: endpoint api/v1/rent. You must specify the id of the movie using the movie_id param.
 - list your orders using `GET`: endpoint api/v1/orders
 - pay a movie that was previously rent using `POST`: endpoint api/v1/pay. You must specify the order id and the amount to pay using the order_id and amount params.
   If the amount is less than the order's charge the payment will fail.
  
  - view all available info for the user using `GET`: endpoint api/v1/home/
 
 - login to gain access to the service by using the available users specified in the basic auth configuration.
 - all actions that create, modify or delete are using authorization rules.
 - data related to the user like orders, and info about a specific user require also authorization from the user or the admin.
 - only the admin user can modify movies, categories and orders.
 - click [here](https://github.com/nmakro/movie-store/blob/master/app/api/auth.py#L6) to see the current available users with authorization access.
 - all list actions support pagination using the page/per_page params, defaulting to 1 and 4.
 - a database with some initial setup is provided [here](https://github.com/nmakro/movie-store/blob/master/app/app.db)
  
## Use
  example usage:
  search all movies by category:drama
  http://127.0.0.1:5000/api/v1/movies/search?genre=drama
  
  ```json
  {
  "_meta": {
    "next": "/api/v1/movies/?page=2&genre=drama", 
    "prev": null
  }, 
  "movies": [
    {
      "director": "Lumet", 
      "genre": [
        "drama"
      ], 
      "id": 4, 
      "title": "12 Angry Men", 
      "year": "1957"
    }, 
    {
      "director": "David Fincher", 
      "genre": [
        "drama"
      ], 
      "id": 6, 
      "title": "Fight Club", 
      "year": "1999"
    }, 
    {
      "director": "Robert Zemeckis", 
      "genre": [
        "drama"
      ], 
      "id": 7, 
      "title": "Forrest Gump", 
      "year": "1994"
    }, 
    {
      "director": "Martin Scorsese", 
      "genre": [
        "crime", 
        "drama"
      ], 
      "id": 10, 
      "title": "Goodfellas", 
      "year": "1990"
    }
  ]
}
```


## Quick Start

### Prerequisites
- Docker & Docker Compose
- Clerk account (for authentication) - [Sign up free](https://clerk.com/)

### 1. Clone the repository

```bash
git clone https://github.com/nmakro/movie-store.git
cd movie-store
```

### 2. Set up Clerk Authentication

1. Create a free account at [Clerk.com](https://clerk.com/)
2. Create a new application in the Clerk Dashboard
3. Get your API keys from the [API Keys page](https://dashboard.clerk.com/last-active?path=api-keys)
4. Update the frontend environment variables:

```bash
# Edit frontend/.env.local and replace the placeholder keys
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_actual_key_here
CLERK_SECRET_KEY=sk_test_your_actual_secret_here
NEXT_PUBLIC_API_URL=http://localhost:5000
```

**Note**: Docker Compose automatically loads these from `frontend/.env.local` - no need to export them separately!

### 3. Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Backend API: http://localhost:5000
# Frontend App: http://localhost:3000
```

## Development Mode

### Backend Development

**With uv (recommended - 10-100x faster!):**
```bash
cd backend
uv sync  # Creates .venv and installs dependencies
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
export FLASK_APP=moviestore.py
flask run
```

**Or with pip:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=moviestore.py
flask run
```

### Frontend Development

```bash
cd frontend

# Make sure .env.local has your Clerk keys
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Authentication

The frontend uses [Clerk](https://clerk.com/) for modern, secure authentication:

- **Sign Up/Sign In**: Built-in authentication UI
- **User Management**: Managed through Clerk Dashboard
- **Protected Routes**: Automatic middleware-based protection
- **Session Management**: Secure, automatic session handling

The backend still uses its own authentication system for API endpoints. You can integrate Clerk with the backend in the future for unified authentication.

