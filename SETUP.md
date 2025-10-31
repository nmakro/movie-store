# Movie Store - Complete Setup Guide

This guide will help you set up and run the Movie Store application with Clerk authentication.

## 🏗️ Architecture

This is a **monorepo** containing:
- **Backend**: Flask REST API (Python) in `backend/`
- **Frontend**: Next.js App Router (TypeScript + React) in `frontend/`
- **Docker**: Multi-container setup with docker-compose

## ✅ Verification Steps

### 1. Check Project Structure

Your project should look like this:

```
movie-store/
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── Dockerfile
│   ├── moviestore.py
│   ├── requirements.txt
│   └── start.sh
├── frontend/
│   ├── app/
│   │   ├── layout.tsx    (Clerk configured)
│   │   └── page.tsx
│   ├── lib/
│   │   └── api.ts        (Backend API client)
│   ├── middleware.ts     (Clerk middleware)
│   ├── next.config.ts    (Standalone + rewrites)
│   ├── Dockerfile
│   ├── .env.local        (Your Clerk keys go here)
│   └── package.json
├── docker-compose.yml
└── README.md
```

### 2. Verify Clerk Integration

#### ✓ Middleware Check

File: `frontend/middleware.ts`

```typescript
import { clerkMiddleware } from "@clerk/nextjs/server";

export default clerkMiddleware();
```

**Status**: ✅ Using `clerkMiddleware()` (correct, modern approach)

#### ✓ Layout Check

File: `frontend/app/layout.tsx`

Should have:
- `<ClerkProvider>` wrapping the entire app
- Imports from `@clerk/nextjs` (not deprecated paths)
- `<SignInButton>`, `<SignUpButton>`, `<UserButton>` components

**Status**: ✅ Properly configured

#### ✓ Environment Variables

**For Local Development:**
File: `frontend/.env.local` (gitignored)
```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=YOUR_PUBLISHABLE_KEY
CLERK_SECRET_KEY=YOUR_SECRET_KEY
NEXT_PUBLIC_API_URL=http://localhost:5000
```

**For Docker Compose:**
File: `.env.local` in **project root** (gitignored)
```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=YOUR_PUBLISHABLE_KEY
CLERK_SECRET_KEY=YOUR_SECRET_KEY
```

**Action Required**: Replace placeholder keys with real keys from [Clerk Dashboard](https://dashboard.clerk.com/last-active?path=api-keys)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Get your Clerk keys**:
   - Go to https://dashboard.clerk.com
   - Create a new application
   - Copy your Publishable Key and Secret Key

2. **Set environment variables** (create `.env.local` in project root):
   ```bash
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_actual_key
   CLERK_SECRET_KEY=sk_test_your_actual_secret
   ```
   
   ⚠️ **Important**: Create this file in the **project root** (same level as `docker-compose.yml`), NOT in `frontend/`
   
   Docker Compose automatically reads `.env.local` and:
   - Passes `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` as a build argument to the frontend
   - Sets environment variables for the running container

3. **Run the application**:
   ```bash
   docker-compose up --build
   ```

4. **Access the apps**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Option 2: Development Mode (Local)

#### Backend:

**With uv (recommended - much faster!):**
```bash
cd backend

# Install uv if you haven't already
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Sync dependencies (creates .venv and installs from pyproject.toml)
uv sync

# Activate virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Run Flask
export FLASK_APP=moviestore.py
flask run
```

**Or with traditional pip:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=moviestore.py
flask run
```

Backend will run on http://localhost:5000

#### Frontend:
```bash
cd frontend

# Make sure .env.local has your Clerk keys
npm install
npm run dev
```

Frontend will run on http://localhost:3000

## 🔐 Clerk Authentication Features

The frontend now includes:

1. **Public Routes**: Homepage accessible to everyone
2. **Conditional UI**: Different content for signed-in vs signed-out users
3. **Sign In/Up**: Modal-based authentication (no separate pages needed)
4. **User Profile**: `<UserButton>` in the header with account management
5. **Protected Routes**: Can be added using Clerk's middleware matcher
6. **Session Management**: Automatic, handled by Clerk

### Example: Protecting Routes

To protect specific routes, update `frontend/middleware.ts`:

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/movies(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) await auth.protect();
});

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
```

## 🧪 Testing the Integration

### Test Backend API:

```bash
# List movies
curl http://localhost:5000/api/v1/movies

# Search movies by genre
curl http://localhost:5000/api/v1/movies/search?genre=drama

# List categories
curl http://localhost:5000/api/v1/categories
```

### Test Frontend:

1. Visit http://localhost:3000
2. Click "Sign Up" to create an account
3. Sign in with your new account
4. Verify the `<UserButton>` appears in the header

### Test Integration:

The frontend can call the backend API using the helper in `frontend/lib/api.ts`:

```typescript
import { fetchMovies } from '@/lib/api';

const movies = await fetchMovies(1, 10);
```

## 📁 Backend & Frontend Separation

### Why This Works Well:

1. **Independent Deployment**: Each service can be deployed separately
2. **Clear Boundaries**: Backend = data/logic, Frontend = UI/UX
3. **Different Tech Stacks**: Python (backend) and TypeScript (frontend) work independently
4. **Shared Network**: Docker Compose creates a network for internal communication
5. **Environment Isolation**: Each has its own dependencies and environment

### API Communication:

- **Development**: Frontend → `http://localhost:5000` → Backend
- **Docker**: Frontend → `http://backend:5000` → Backend (internal Docker network)
- **Next.js Rewrites**: Configured in `next.config.ts` to proxy `/api/*` requests

## 🐛 Troubleshooting

### Clerk Issues:

**Problem**: "Clerk: Missing publishable key"

**Solution**: 
1. Verify `.env.local` exists in `frontend/` directory
2. Check that keys don't have quotes around them
3. Restart the dev server after changing env variables

### Docker Issues:

**Problem**: "Cannot find module '@clerk/nextjs'"

**Solution**: Rebuild containers:
```bash
docker-compose down
docker-compose up --build
```

### Backend Issues:

**Problem**: Backend API returns 404

**Solution**: 
1. Check backend is running on port 5000
2. Verify endpoints start with `/api/v1/`
3. Check `docker-compose.yml` port mappings

## 🎯 Next Steps

Now that you have a working monorepo with Clerk authentication, you can:

1. **Create Movie Listing Page**: Use the API client in `lib/api.ts`
2. **Add Protected Routes**: Protect `/movies` or `/rent` pages
3. **Integrate Clerk with Backend**: Use Clerk JWT validation in Flask
4. **Add User Preferences**: Store user data in backend associated with Clerk user ID
5. **Build Rental Flow**: Create UI for renting movies and viewing orders

## 📚 Resources

- [Clerk Next.js Docs](https://clerk.com/docs/quickstarts/nextjs)
- [Next.js App Router](https://nextjs.org/docs/app)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

**Need Help?** Check that:
- ✅ All TODOs are completed
- ✅ Clerk keys are set in `.env.local`
- ✅ Both services are running
- ✅ No linter errors in frontend code

