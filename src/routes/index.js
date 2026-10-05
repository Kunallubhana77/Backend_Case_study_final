const express = require('express');
const router = express.Router();

const authRoutes = require('./authRoutes');
const tripRoutes = require('./tripRoutes');
const destinationRoutes = require('./destinationRoutes');
const weatherRoutes = require('./weatherRoutes');

router.use('/auth', authRoutes);
router.use('/trips', tripRoutes);
router.use('/destinations', destinationRoutes);
router.use('/weather', weatherRoutes);

module.exports = router;
