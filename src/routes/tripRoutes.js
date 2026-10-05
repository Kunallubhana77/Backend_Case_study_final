const express = require('express');
const router = express.Router();
const {
  getTrips,
  getTripById,
  createTrip,
  updateTrip,
  deleteTrip,
  shareTrip,
  searchTrips,
  uploadTripPhoto,
} = require('../controllers/tripController');
const {
  getItineraries,
  addItineraryDay,
  updateItineraryDay,
  deleteItineraryDay,
} = require('../controllers/itineraryController');
const {
  getExpenses,
  addExpense,
  deleteExpense,
} = require('../controllers/expenseController');
const { getTripWeather } = require('../controllers/weatherController');

const { protect } = require('../middleware/authMiddleware');
const upload = require('../middleware/uploadMiddleware');
const {
  createTripValidation,
  updateTripValidation,
  addItineraryValidation,
  shareTripValidation,
  expenseValidation,
} = require('../middleware/validationMiddleware');

// All trip routes require authentication
router.use(protect);

// Search endpoint MUST be defined before /:id to avoid router treating "search" as an ID
router.get('/search', searchTrips);

// Trips CRUD
router.route('/')
  .get(getTrips)
  .post(createTripValidation, createTrip);

router.route('/:id')
  .get(getTripById)
  .put(updateTripValidation, updateTrip)
  .delete(deleteTrip);

// Collaborators
router.post('/:id/share', shareTripValidation, shareTrip);

// Day-by-Day Itineraries
router.route('/:id/itinerary')
  .get(getItineraries)
  .post(addItineraryValidation, addItineraryDay);

router.route('/:id/itinerary/:itineraryId')
  .put(updateItineraryDay)
  .delete(deleteItineraryDay);

// Photo Upload (Firebase Storage / Local Fallback)
router.post('/:id/photos', upload.single('photo'), uploadTripPhoto);

// Budget & Expenses (Optional Advanced Feature)
router.route('/:id/expenses')
  .get(getExpenses)
  .post(expenseValidation, addExpense);

router.delete('/:id/expenses/:expenseId', deleteExpense);

// Trip Weather (Optional Advanced Feature)
router.get('/:id/weather', getTripWeather);

module.exports = router;
