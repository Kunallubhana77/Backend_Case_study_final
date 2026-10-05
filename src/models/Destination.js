const mongoose = require('mongoose');

const destinationSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Destination name is required'],
      trim: true,
    },
    country: {
      type: String,
      required: [true, 'Country name is required'],
      trim: true,
    },
    description: {
      type: String,
      default: '',
    },
    coordinates: {
      latitude: { type: Number },
      longitude: { type: Number },
    },
    imageUrl: {
      type: String,
      default: '',
    },
    popularAttractions: [{
      type: String,
    }],
    averageDailyCost: {
      type: Number,
      default: 0,
    },
    currency: {
      type: String,
      default: 'USD',
    },
    bestTimeToVisit: {
      type: String,
      default: '',
    },
  },
  {
    timestamps: true,
  }
);

// Index for search
destinationSchema.index({ name: 'text', country: 'text', description: 'text' });

module.exports = mongoose.model('Destination', destinationSchema);
