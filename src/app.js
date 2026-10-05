const path = require('path');
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const swaggerUi = require('swagger-ui-express');

const routes = require('./routes');
const errorHandler = require('./middleware/errorHandler');
const swaggerDoc = require('./docs/swagger.json');

const app = express();

// Security HTTP headers (configured to allow Swagger UI resources)
app.use(
  helmet({
    contentSecurityPolicy: false,
    crossOriginResourcePolicy: false,
  })
);

// Enable CORS
app.use(cors());

// HTTP request logger
if (process.env.NODE_ENV !== 'test') {
  app.use(morgan('dev'));
}

// Body parsers
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static uploaded files (for local file upload fallback)
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

// Swagger API Documentation UI
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDoc, {
  customSiteTitle: 'TripCraft API Documentation',
}));

// API Root Information & Health Check
app.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'Welcome to TripCraft API - Travel Itinerary Planner',
    documentation: '/api-docs',
    endpoints: {
      auth: {
        register: 'POST /api/auth/register',
        login: 'POST /api/auth/login',
        me: 'GET /api/auth/me',
      },
      trips: {
        list: 'GET /api/trips',
        getById: 'GET /api/trips/:id',
        create: 'POST /api/trips',
        update: 'PUT /api/trips/:id',
        delete: 'DELETE /api/trips/:id',
        search: 'GET /api/trips/search?keyword=europe',
        uploadPhoto: 'POST /api/trips/:id/photos',
      },
      itinerary: {
        get: 'GET /api/trips/:id/itinerary',
        addOrUpdate: 'POST /api/trips/:id/itinerary',
      },
      collaborators: {
        share: 'POST /api/trips/:id/share',
      },
      budget: {
        getExpenses: 'GET /api/trips/:id/expenses',
        addExpense: 'POST /api/trips/:id/expenses',
      },
      weather: {
        city: 'GET /api/weather?city=Paris',
        tripDestination: 'GET /api/trips/:id/weather',
      },
    },
  });
});

// Mount modular API routes
app.use('/api', routes);

// 404 Route Handler
app.use((req, res, next) => {
  res.status(404).json({
    success: false,
    message: `Resource not found at ${req.originalUrl}`,
  });
});

// Centralized Error Handling Middleware
app.use(errorHandler);

module.exports = app;
