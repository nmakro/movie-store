# Docker Compose Environment Setup

This guide explains how to properly configure environment variables for Docker Compose builds.

## The Problem

When building Docker images, Next.js needs environment variables at **build time** to properly render pages. If `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` is not available during the build, it defaults to a placeholder value, causing Clerk authentication errors.

## The Solution

Docker Compose automatically reads `.env.local` files from the **project root directory** (where `docker-compose.yml` is located) and passes variables to build processes.

## Setup Steps

### 1. Get Your Clerk Keys

- Go to https://dashboard.clerk.com/last-active?path=api-keys
- Create a new application if needed
- Copy your **Publishable Key** (starts with `pk_`)
- Copy your **Secret Key** (starts with `sk_`)

### 2. Create `.env.local` in Project Root

Create a file named `.env.local` in the **project root** (same directory as `docker-compose.yml`):

```bash
cat > .env.local << 'EOF2'
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_actual_key_here
CLERK_SECRET_KEY=sk_test_your_actual_secret_here
EOF2
```

⚠️ **Important**: 
- This file should be in the **project root**, NOT in `frontend/`
- This file is in `.gitignore` - it won't be committed
- Replace the placeholder values with your actual keys

### 3. Run Docker Compose

```bash
cd /Users/nmakro/Projects/movie-store
docker-compose up --build
```

Docker Compose will:
1. Read `.env.local` from the project root
2. Pass `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` as a build argument to the frontend Dockerfile
3. Pass both keys to the running containers as environment variables

## File Locations

```
/Users/nmakro/Projects/movie-store/
├── docker-compose.yml          # Main Docker Compose config
├── .env.local                  # ⭐ Create here (root level) - GITIGNORED
├── .env.example                # Template reference
├── frontend/
│   ├── Dockerfile              # Updated with ARG support
│   └── .env.local              # For local npm run dev (optional)
└── backend/
    └── ...
```

## Two Environments

### Local Development (npm run dev)
Use `.env.local` in `frontend/` directory:
```bash
frontend/.env.local
```

### Docker Compose
Use `.env.local` in project root:
```bash
.env.local  (same level as docker-compose.yml)
```

## Troubleshooting

### Error: "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY is invalid"

**Solution**: Make sure you:
1. Created `.env.local` in the **project root** (not in `frontend/`)
2. Ran `docker-compose up --build` from the project root
3. Replaced placeholder values with actual Clerk keys

### Error: "Could not find .env.local"

**Solution**: 
- The file must exist before running `docker-compose up`
- Create it with: `cat > .env.local << 'EOF' ... EOF`
- Verify location with: `ls -la .env.local`

## Related Files

- `.env.example` - Template for environment variables
- `CLERK_INTEGRATION.md` - Clerk setup guide
- `SETUP.md` - Full project setup instructions

