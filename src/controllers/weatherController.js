const Trip = require('../models/Trip');
const { getWeatherForecast } = require('../services/weatherService');

/**
 * @desc    Get weather for a city or coordinates
 * @route   GET /api/weather
 * @access  Public
 */
const getWeather = async (req, res, next) => {
  try {
    const { city, lat, lon } = req.query;

    if (!city && (!lat || !lon)) {
      return res.status(400).json({
        success: false,
        message: 'Please provide a city name (e.g. ?city=Paris) or lat/lon coordinates',
      });
    }

    const weatherData = await getWeatherForecast(
      city,
      lat ? parseFloat(lat) : null,
      lon ? parseFloat(lon) : null
    );

    res.status(200).json({
      success: true,
      data: weatherData,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Get weather for a specific trip destination
 * @route   GET /api/trips/:id/weather
 * @access  Private
 */
const getTripWeather = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id).populate('destination.destinationRef');

    if (!trip) {
      return res.status(404).json({ success: false, message: 'Trip not found' });
    }

    let lat = null;
    let lon = null;
    if (trip.destination && trip.destination.destinationRef && trip.destination.destinationRef.coordinates) {
      lat = trip.destination.destinationRef.coordinates.latitude;
      lon = trip.destination.destinationRef.coordinates.longitude;
    }

    const destinationName = trip.destination ? trip.destination.name : 'Unknown';
    const weatherData = await getWeatherForecast(destinationName, lat, lon);

    res.status(200).json({
      success: true,
      tripId: trip._id,
      tripTitle: trip.title,
      destination: destinationName,
      data: weatherData,
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getWeather,
  getTripWeather,
};
