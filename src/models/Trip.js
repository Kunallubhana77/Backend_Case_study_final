const mongoose = require('mongoose');

const bookingSchema = new mongoose.Schema({
  type: {
    type: String,
    enum: ['flight', 'hotel', 'car', 'activity', 'train', 'other'],
    default: 'hotel',
  },
  title: { type: String, required: true },
  confirmationNumber: { type: String, default: '' },
  bookingDate: { type: Date },
  cost: { type: Number, default: 0 },
  currency: { type: String, default: 'USD' },
  notes: { type: String, default: '' },
});

const expenseSchema = new mongoose.Schema({
  title: { type: String, required: true },
  category: {
    type: String,
    enum: ['food', 'transportation', 'lodging', 'activities', 'shopping', 'other'],
    default: 'other',
  },
  amount: { type: Number, required: true },
  currency: { type: String, default: 'USD' },
  date: { type: Date, default: Date.now },
  paidBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  notes: { type: String, default: '' },
});

const collaboratorSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  role: {
    type: String,
    enum: ['viewer', 'editor'],
    default: 'viewer',
  },
  addedAt: {
    type: Date,
    default: Date.now,
  },
});

const tripPhotoSchema = new mongoose.Schema({
  url: { type: String, required: true },
  caption: { type: String, default: '' },
  storageType: { type: String, enum: ['firebase', 'local'], default: 'firebase' },
  uploadedAt: { type: Date, default: Date.now },
});

const tripSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: [true, 'Trip title is required'],
      trim: true,
      maxlength: [100, 'Title cannot exceed 100 characters'],
    },
    description: {
      type: String,
      default: '',
    },
    destination: {
      name: { type: String, required: [true, 'Destination name is required'] },
      country: { type: String, default: '' },
      destinationRef: { type: mongoose.Schema.Types.ObjectId, ref: 'Destination' },
    },
    startDate: {
      type: Date,
      required: [true, 'Start date is required'],
    },
    endDate: {
      type: Date,
      required: [true, 'End date is required'],
    },
    coverPhoto: {
      type: String,
      default: '',
    },
    photos: [tripPhotoSchema],
    owner: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    collaborators: [collaboratorSchema],
    bookings: [bookingSchema],
    budget: {
      totalBudget: { type: Number, default: 0 },
      currency: { type: String, default: 'USD' },
      expenses: [expenseSchema],
    },
    status: {
      type: String,
      enum: ['planning', 'ongoing', 'completed', 'cancelled'],
      default: 'planning',
    },
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

// Virtual field to calculate total spent
tripSchema.virtual('totalSpent').get(function () {
  if (!this.budget || !this.budget.expenses) return 0;
  return this.budget.expenses.reduce((sum, item) => sum + (item.amount || 0), 0);
});

// Text index for search
tripSchema.index({
  title: 'text',
  description: 'text',
  'destination.name': 'text',
  'destination.country': 'text',
});

module.exports = mongoose.model('Trip', tripSchema);
