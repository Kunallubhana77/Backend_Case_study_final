const Destination = require('../models/Destination');
const { getWeatherForecast } = require('../services/weatherService');

/**
 * @desc    Get all destinations with optional search
 * @route   GET /api/destinations
 * @access  Public
 */
const getDestinations = async (req, res, next) => {
  try {
    const { keyword } = req.query;
    let query = {};

    if (keyword) {
      const regex = new RegExp(keyword, 'i');
      query = {
        $or: [{ name: regex }, { country: regex }, { description: regex }],
      };
    }

    const destinations = await Destination.find(query).sort({ name: 1 });

    res.status(200).json({
      success: true,
      count: destinations.length,
      data: destinations,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Get single destination by ID
 * @route   GET /api/destinations/:id
 * @access  Public
 */
const getDestinationById = async (req, res, next) => {
  try {
    const destination = await Destination.findById(req.params.id);

    if (!destination) {
      return res.status(404).json({ success: false, message: 'Destination not found' });
    }

    res.status(200).json({
      success: true,
      data: destination,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Create a destination
 * @route   POST /api/destinations
 * @access  Private (Admin or Authenticated User)
 */
const createDestination = async (req, res, next) => {
  try {
    const destination = await Destination.create(req.body);

    res.status(201).json({
      success: true,
      message: 'Destination created successfully',
      data: destination,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Get destination weather forecast
 * @route   GET /api/destinations/:id/weather
 * @access  Public
 */
const getDestinationWeather = async (req, res, next) => {
  try {
    const destination = await Destination.findById(req.params.id);

    if (!destination) {
      return res.status(404).json({ success: false, message: 'Destination not found' });
    }

    const lat = destination.coordinates ? destination.coordinates.latitude : null;
    const lon = destination.coordinates ? destination.coordinates.longitude : null;

    const weather = await getWeatherForecast(destination.name, lat, lon);

    res.status(200).json({
      success: true,
      data: weather,
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getDestinations,
  getDestinationById,
  createDestination,
  getDestinationWeather,
};
