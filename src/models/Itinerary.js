const mongoose = require('mongoose');

const activitySchema = new mongoose.Schema({
  time: {
    type: String,
    default: '',
  },
  activity: {
    type: String,
    required: [true, 'Activity name is required'],
    trim: true,
  },
  location: {
    type: String,
    default: '',
  },
  notes: {
    type: String,
    default: '',
  },
  cost: {
    type: Number,
    default: 0,
  },
  currency: {
    type: String,
    default: 'USD',
  },
  photos: [{
    type: String,
  }],
  bookingRef: {
    type: String,
    default: '',
  },
  isCompleted: {
    type: Boolean,
    default: false,
  },
});

const itinerarySchema = new mongoose.Schema(
  {
    trip: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Trip',
      required: true,
      index: true,
    },
    dayNumber: {
      type: Number,
      required: [true, 'Day number is required'],
      min: 1,
    },
    date: {
      type: Date,
    },
    title: {
      type: String,
      default: '',
      trim: true,
    },
    notes: {
      type: String,
      default: '',
    },
    activities: [activitySchema],
  },
  {
    timestamps: true,
  }
);

// Compound index to ensure uniqueness of dayNumber per trip
itinerarySchema.index({ trip: 1, dayNumber: 1 });

module.exports = mongoose.model('Itinerary', itinerarySchema);
