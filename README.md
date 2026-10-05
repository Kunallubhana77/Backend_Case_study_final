# 🌍 TripCraft - Travel Itinerary Planner Backend API

[![Node.js](https://img.shields.io/badge/Node.js-v20+-green.svg)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/Express.js-5.x-black.svg)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Mongoose-brightgreen.svg)](https://mongoosejs.com/)
[![Firebase](https://img.shields.io/badge/Firebase-Admin%20%26%20Storage-orange.svg)](https://firebase.google.com/)
[![Swagger](https://img.shields.io/badge/Swagger-OpenAPI%203.0-blue.svg)](http://localhost:5000/api-docs)

> **Case Study 96: Backend Development - Travel Itinerary Planner ("TripCraft")**  
> B.Tech Computer Science Engineering — Backend Development (Node.js, Express.js, MongoDB & Firebase)

TripCraft is a modular, secure, production-ready REST API that empowers travelers to organize day-by-day trips, schedule activities, upload photos to Firebase Storage, collaborate with fellow travelers, track budgets and expenses, and check destination weather forecasts.

---

## 📋 Features

- 🔐 **Dual Authentication**: Secure JWT-based authentication + Firebase Auth token verification.
- 🗺️ **Trip Management**: Full CRUD operations for trips with destinations, dates, bookings, and covers.
- 📅 **Day-by-Day Itinerary**: Create and manage detailed daily plans, locations, times, and activities.
- 👥 **Trip Collaboration**: Share trips with friends and teammates with granular roles (`viewer` / `editor`).
- 🔎 **Smart Keyword Search**: Search trips and activities by keyword (e.g. `europe`, `museum`, `paris`).
- 📸 **Firebase Storage**: Upload trip cover photos and gallery snapshots to Firebase Storage (with local disk fallback).
- 💰 **Budget & Expense Tracking** *(Advanced Feature)*: Track expenses, log spend by category, and calculate remaining trip budget.
- 🌤️ **Live Weather Forecast** *(Advanced Feature)*: Real-time and 7-day weather forecasts for destinations via free Open-Meteo integration.
- 📖 **Interactive API Documentation**: Swagger UI at `/api-docs` and a ready-to-import Postman Collection.

---

## 🏗️ Project Architecture

```
backend/
├── src/
│   ├── config/
│   │   ├── db.js                     # MongoDB connection via Mongoose
│   │   └── firebase.js               # Firebase Admin & Storage initialization
│   ├── models/
│   │   ├── User.js                   # User schema with bcrypt password hashing
│   │   ├── Trip.js                   # Trip schema (collaborators, budget, bookings)
│   │   ├── Itinerary.js              # Day-by-day itinerary & activities schema
│   │   └── Destination.js            # Destination catalog schema
│   ├── middleware/
│   │   ├── authMiddleware.js         # JWT & Firebase token verification
│   │   ├── uploadMiddleware.js       # Multer image upload memory handler
│   │   ├── validationMiddleware.js   # express-validator request validation
│   │   └── errorHandler.js           # Centralized HTTP error handler
│   ├── services/
│   │   ├── firebaseStorageService.js # Firebase Storage uploader & local fallback
│   │   └── weatherService.js         # Geocoding & live weather forecast service
│   ├── controllers/
│   │   ├── authController.js         # Register, Login, Me
│   │   ├── tripController.js         # Trip CRUD, search, photo uploads, sharing
│   │   ├── itineraryController.js    # Day-by-day itinerary & activity actions
│   │   ├── expenseController.js      # Trip budget & expense tracking
│   │   ├── destinationController.js  # Destinations catalog & destination weather
│   │   └── weatherController.js      # Weather forecast endpoints
│   ├── routes/
│   │   ├── authRoutes.js             # /api/auth
│   │   ├── tripRoutes.js             # /api/trips (CRUD, itinerary, share, search)
│   │   ├── destinationRoutes.js      # /api/destinations
│   │   ├── weatherRoutes.js          # /api/weather
│   │   └── index.js                  # Master route aggregator
│   ├── docs/
│   │   └── swagger.json              # OpenAPI 3.0 specification
│   ├── app.js                        # Express app setup & middleware
│   └── server.js                     # Entry point & HTTP server
├── postman/
│   └── TripCraft_API.postman_collection.json # Exported Postman Collection
├── uploads/                          # Local image uploads directory (fallback)
├── Dockerfile                        # Production Docker container
├── render.yaml                       # Render.com deployment blueprint
├── Procfile                          # Heroku deployment configuration
├── .env.example                      # Sample environment variables
└── README.md                         # Documentation & setup guide
```

---

## 🚀 Getting Started

### 1. Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher)
- [MongoDB](https://www.mongodb.com/) (Local instance or MongoDB Atlas URI)

### 2. Installation

Clone or open the repository folder and install dependencies:
```bash
npm install
```

### 3. Environment Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Configure your environment variables in `.env`:
```env
PORT=5000
NODE_ENV=development
MONGO_URI=mongodb://127.0.0.1:27017/tripcraft
JWT_SECRET=your_super_secret_jwt_key_here
JWT_EXPIRES_IN=7d

# Optional: Firebase Storage (local uploads fallback automatically if left empty)
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_STORAGE_BUCKET=your-app.appspot.com
```

### 4. Running the Server

- **Development Mode (with auto-reload)**:
  ```bash
  npm run dev
  ```

- **Production Mode**:
  ```bash
  npm start
  ```

Server will start on: `http://localhost:5000`  
Interactive Swagger Docs: `http://localhost:5000/api-docs`

---

## 📡 API Endpoints Reference

### 1. Authentication (`/api/auth`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/auth/register` | Register a new user (`name`, `email`, `password`) | Public |
| `POST` | `/api/auth/login` | Login user & receive JWT token | Public |
| `GET` | `/api/auth/me` | Get profile of logged-in user | Private |

### 2. Trips (`/api/trips`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/trips` | Get all trips for logged in user (owned & collaborated) | Private |
| `GET` | `/api/trips/:id` | Get trip by ID with populated itineraries & collaborators | Private |
| `POST` | `/api/trips` | Create a new trip | Private |
| `PUT` | `/api/trips/:id` | Update trip details | Private (Owner/Editor) |
| `DELETE` | `/api/trips/:id` | Delete trip and cascade delete its itineraries | Private (Owner) |
| `POST` | `/api/trips/:id/photos` | Upload trip photos via Multer & Firebase Storage | Private |

### 3. Search (`/api/trips/search`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/trips/search?keyword=europe` | Search trips by keyword in title, destination, activities | Private |

### 4. Day-by-Day Itineraries (`/api/trips/:id/itinerary`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/trips/:id/itinerary` | Get all day-by-day itineraries for the trip | Private |
| `POST` | `/api/trips/:id/itinerary` | Add or update day itinerary with activities | Private (Owner/Editor) |
| `PUT` | `/api/trips/:id/itinerary/:itineraryId` | Update a specific itinerary day | Private (Owner/Editor) |
| `DELETE` | `/api/trips/:id/itinerary/:itineraryId` | Delete a specific itinerary day | Private (Owner/Editor) |

### 5. Collaborators (`/api/trips/:id/share`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/trips/:id/share` | Share trip with friend (`email`, `role: viewer/editor`) | Private (Owner/Editor) |

### 6. Budget & Expense Tracking *(Advanced Feature)*
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/trips/:id/expenses` | Get budget, category breakdown, total spent & remaining | Private |
| `POST` | `/api/trips/:id/expenses` | Log a new expense (`title`, `amount`, `category`, `currency`) | Private |
| `DELETE` | `/api/trips/:id/expenses/:expenseId` | Delete an expense entry | Private |

### 7. Weather Forecast *(Advanced Feature)*
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/weather?city=Paris` | Live weather & 7-day forecast for any city | Public |
| `GET` | `/api/trips/:id/weather` | Live weather forecast for the trip's destination | Private |

---

## 🔄 Example User Flow (From Case Study)

Follow this 3-step walkthrough to test the core flow:

### Step 1: Register and Log In
```bash
# 1. Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Explorer",
    "email": "jane@tripcraft.dev",
    "password": "Password123!"
  }'

# Save the "token" from the response.
export TOKEN="your_jwt_token_here"
```

### Step 2: Create a New Trip (`POST /api/trips`)
```bash
curl -X POST http://localhost:5000/api/trips \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Summer in Europe",
    "description": "Exploring Paris, Rome, and Zurich",
    "destination": {
      "name": "Paris",
      "country": "France"
    },
    "startDate": "2026-07-01T00:00:00.000Z",
    "endDate": "2026-07-15T00:00:00.000Z",
    "budget": {
      "totalBudget": 3000,
      "currency": "EUR"
    }
  }'

# Save the trip "_id" from the response.
export TRIP_ID="your_trip_id_here"
```

### Step 3: Add Day-by-Day Activities (`POST /api/trips/:id/itinerary`)
```bash
curl -X POST http://localhost:5000/api/trips/$TRIP_ID/itinerary \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "dayNumber": 1,
    "title": "Arrival & City Lights",
    "date": "2026-07-01T00:00:00.000Z",
    "activities": [
      {
        "time": "10:00 AM",
        "activity": "Hotel Check-in",
        "location": "Le Petit Hotel, Paris",
        "cost": 120
      },
      {
        "time": "03:00 PM",
        "activity": "Visit Eiffel Tower",
        "location": "Champ de Mars",
        "cost": 28
      }
    ]
  }'
```

### Step 4: Share Trip with a Friend (`POST /api/trips/:id/share`)
```bash
curl -X POST http://localhost:5000/api/trips/$TRIP_ID/share \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "email": "friend@tripcraft.dev",
    "role": "editor"
  }'
```

### Step 5: Search Trips (`GET /api/trips/search?keyword=europe`)
```bash
curl -X GET "http://localhost:5000/api/trips/search?keyword=europe" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📮 Postman Collection

Import `postman/TripCraft_API.postman_collection.json` into [Postman](https://www.postman.com/):
1. Click **Import** in Postman.
2. Select the file: `postman/TripCraft_API.postman_collection.json`.
3. Set your collection variable `baseUrl` to `http://localhost:5000`.
4. Run `Register User` or `Login User` — the test scripts automatically set the `{{token}}` variable for subsequent requests!

---

## ☁️ Deployment Guide

### Deployment on Render
1. Push this repository to GitHub.
2. Go to [Render Dashboard](https://dashboard.render.com/) and create a **New Web Service**.
3. Connect your GitHub repository.
4. Set the following:
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
5. Under **Environment Variables**, add:
   - `MONGO_URI`: Your MongoDB Atlas connection string.
   - `JWT_SECRET`: A long random string.
   - `NODE_ENV`: `production`

*(Alternatively, connect via `render.yaml` blueprint included in the root directory)*.

### Deployment on Heroku
```bash
heroku create tripcraft-backend
heroku config:set MONGO_URI="mongodb+srv://..." JWT_SECRET="your_secret" NODE_ENV="production"
git push heroku main
```

---

## 📄 License
This project was developed for educational and evaluation purposes under the B.Tech Computer Science Engineering Backend Development Curriculum.
