const express = require('express');
const router = express.Router();
const {
  getDestinations,
  getDestinationById,
  createDestination,
  getDestinationWeather,
} = require('../controllers/destinationController');
const { protect } = require('../middleware/authMiddleware');

router.route('/')
  .get(getDestinations)
  .post(protect, createDestination);

router.route('/:id')
  .get(getDestinationById);

router.route('/:id/weather')
  .get(getDestinationWeather);

module.exports = router;
