# SmartNotes - MERN Notes Application

A full-stack notes management application built with React.js, Node.js, Express.js, MongoDB, and JWT authentication.

## Features

- Secure user authentication with JWT
- CRUD operations for notes
- Keyword-based search functionality
- MongoDB schema indexing for optimized queries
- REST API with Express.js

## Setup

1. Install dependencies:
```bash
npm run install-deps
```

2. Start MongoDB locally or update MONGODB_URI in backend/.env

3. Update JWT_SECRET in backend/.env

4. Run the application:
```bash
npm run dev
```

## API Endpoints

- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- GET /api/notes - Get all notes (with optional search)
- POST /api/notes - Create new note
- PUT /api/notes/:id - Update note
- DELETE /api/notes/:id - Delete note

## Tech Stack

- **Frontend**: React.js, Axios
- **Backend**: Node.js, Express.js
- **Database**: MongoDB with Mongoose
- **Authentication**: JWT with bcryptjs
- **Search**: MongoDB text indexing