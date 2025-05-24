# Visit Tracker Application

This is a full-stack web application for tracking website visits built with:
- Backend: Python Flask
- Frontend: React with Tailwind CSS
- Database: PostgreSQL

## Project Structure

```
projekt-react/
├── backend/               # Flask backend
│   ├── models/            # Database models
│   ├── routes/            # API routes
│   ├── services/          # Business logic
│   ├── static/            # Static assets
│   ├── templates/         # HTML templates
│   ├── utils/             # Utility functions
│   ├── app.py             # Main Flask application
│   ├── config.py          # Configuration settings
│   └── requirements.txt   # Python dependencies
│
└── frontend/              # React frontend
    ├── public/            # Public assets
    ├── src/               # Source code
    │   ├── api/           # API client
    │   ├── components/    # UI components
    │   ├── pages/         # Page components
    │   └── App.js         # Main app component
    └── package.json       # NPM dependencies
```

## Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL database

## Setup Instructions

### Configure Database

1. Create a PostgreSQL database
2. Update the database connection settings in `backend/.env`

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the Flask server:
   ```
   python app.py
   ```
   
   The backend server will run on http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install NPM dependencies:
   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```

   The frontend application will run on http://localhost:3000

### Quick Start

For Windows users, you can use the provided scripts to start both servers:

```
# Using batch file
start.bat

# OR using PowerShell
./start.ps1
```

## Features

- Track website visits with URL and optional tag
- View visit statistics with visual charts
- Create and manage tags for organizing visits
- Export visit data as CSV

## API Endpoints

### Visit Tracking
- `POST /track` - Track a new visit

### Statistics
- `GET /api/stats` - Get visit statistics
- `GET /api/exportStats` - Export visit statistics as CSV

### Tags
- `POST /api/tags` - Create a new tag
- `GET /api/tags` - Get all tags
- `GET /api/tags/:id` - Get tag by ID
- `DELETE /api/tags/:id` - Delete tag by ID
