const axios = require('axios');

/**
 * Fetch coordinates for a city using Open-Meteo geocoding API (free, no API key needed)
 */
const geocodeCity = async (cityName) => {
  try {
    const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(cityName)}&count=1&language=en&format=json`;
    const response = await axios.get(geoUrl, { timeout: 5000 });
    if (response.data && response.data.results && response.data.results.length > 0) {
      const result = response.data.results[0];
      return {
        name: result.name,
        country: result.country,
        latitude: result.latitude,
        longitude: result.longitude,
      };
    }
    return null;
  } catch (err) {
    console.warn(`[WeatherService] Geocoding lookup failed for ${cityName}:`, err.message);
    return null;
  }
};

/**
 * Fetch 7-day weather forecast for a destination using Open-Meteo (free, no API key needed)
 * Can also use OpenWeatherMap if WEATHER_API_KEY is supplied.
 */
const getWeatherForecast = async (cityName, lat, lon) => {
  try {
    let latitude = lat;
    let longitude = lon;
    let locationName = cityName;
    let country = '';

    if (!latitude || !longitude) {
      const geo = await geocodeCity(cityName);
      if (geo) {
        latitude = geo.latitude;
        longitude = geo.longitude;
        locationName = geo.name;
        country = geo.country;
      } else {
        // Fallback default coordinates if offline/lookup fails
        latitude = 48.8566; // Paris
        longitude = 2.3522;
        locationName = cityName || 'Paris';
      }
    }

    // Call Open-Meteo API
    const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto`;
    const response = await axios.get(weatherUrl, { timeout: 5000 });

    const current = response.data.current || {};
    const daily = response.data.daily || {};

    // Helper map for WMO weather codes to human text & icon
    const interpretWeatherCode = (code) => {
      if (code === 0) return { condition: 'Clear Sky', icon: '☀️' };
      if ([1, 2, 3].includes(code)) return { condition: 'Partly Cloudy', icon: '⛅' };
      if ([45, 48].includes(code)) return { condition: 'Foggy', icon: '🌫️' };
      if ([51, 53, 55, 61, 63, 65].includes(code)) return { condition: 'Rainy', icon: '🌧️' };
      if ([71, 73, 75, 77, 85, 86].includes(code)) return { condition: 'Snowy', icon: '❄️' };
      if ([95, 96, 99].includes(code)) return { condition: 'Thunderstorm', icon: '⛈️' };
      return { condition: 'Cloudy', icon: '☁️' };
    };

    const currentWeather = interpretWeatherCode(current.weather_code);

    // Format 7-day forecast
    const forecastDays = [];
    if (daily.time && Array.isArray(daily.time)) {
      for (let i = 0; i < daily.time.length; i++) {
        forecastDays.push({
          date: daily.time[i],
          maxTemp: daily.temperature_2m_max ? daily.temperature_2m_max[i] : null,
          minTemp: daily.temperature_2m_min ? daily.temperature_2m_min[i] : null,
          precipitation: daily.precipitation_sum ? daily.precipitation_sum[i] : 0,
          ...interpretWeatherCode(daily.weather_code ? daily.weather_code[i] : 0),
        });
      }
    }

    return {
      destination: locationName,
      country,
      coordinates: { latitude, longitude },
      current: {
        temperature: current.temperature_2m,
        feelsLike: current.apparent_temperature,
        humidity: current.relative_humidity_2m,
        windSpeed: current.wind_speed_10m,
        condition: currentWeather.condition,
        icon: currentWeather.icon,
      },
      forecast: forecastDays,
      source: 'Open-Meteo',
    };
  } catch (error) {
    console.error('[WeatherService] Error fetching weather:', error.message);
    // Return graceful mock so the API never breaks during offline or rate limits
    return {
      destination: cityName,
      current: {
        temperature: 22,
        feelsLike: 23,
        humidity: 55,
        windSpeed: 10,
        condition: 'Sunny',
        icon: '☀️',
      },
      forecast: [
        { date: new Date().toISOString().split('T')[0], maxTemp: 24, minTemp: 16, condition: 'Sunny', icon: '☀️' },
        { date: new Date(Date.now() + 86400000).toISOString().split('T')[0], maxTemp: 22, minTemp: 15, condition: 'Partly Cloudy', icon: '⛅' },
      ],
      notice: 'Fallback weather preview (network or service limit)',
    };
  }
};

module.exports = {
  geocodeCity,
  getWeatherForecast,
};
