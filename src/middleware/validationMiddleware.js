const { body, query, param, validationResult } = require('express-validator');

// Helper to handle validation errors
const validate = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      message: 'Validation failed',
      errors: errors.array().map((err) => ({
        field: err.path,
        message: err.msg,
      })),
    });
  }
  next();
};

// Auth validations
const registerValidation = [
  body('name').trim().notEmpty().withMessage('Name is required'),
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('password')
    .isLength({ min: 6 })
    .withMessage('Password must be at least 6 characters long'),
  validate,
];

const loginValidation = [
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('password').notEmpty().withMessage('Password is required'),
  validate,
];

// Trip validations
const createTripValidation = [
  body('title').trim().notEmpty().withMessage('Trip title is required'),
  body('destination')
    .notEmpty()
    .withMessage('Destination is required (provide object or string name)'),
  body('startDate').isISO8601().toDate().withMessage('Valid start date is required'),
  body('endDate').isISO8601().toDate().withMessage('Valid end date is required'),
  validate,
];

const updateTripValidation = [
  param('id').isMongoId().withMessage('Invalid Trip ID format'),
  body('startDate')
    .optional()
    .isISO8601()
    .toDate()
    .withMessage('Valid start date is required if provided'),
  body('endDate')
    .optional()
    .isISO8601()
    .toDate()
    .withMessage('Valid end date is required if provided'),
  validate,
];

// Itinerary validations
const addItineraryValidation = [
  param('id').isMongoId().withMessage('Invalid Trip ID'),
  body('dayNumber')
    .isInt({ min: 1 })
    .withMessage('dayNumber must be a positive integer starting from 1'),
  validate,
];

// Share trip validation
const shareTripValidation = [
  param('id').isMongoId().withMessage('Invalid Trip ID'),
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Valid email of collaborator is required'),
  body('role')
    .optional()
    .isIn(['viewer', 'editor'])
    .withMessage("Role must be either 'viewer' or 'editor'"),
  validate,
];

// Expense validation (Budget tracking)
const expenseValidation = [
  param('id').isMongoId().withMessage('Invalid Trip ID'),
  body('title').trim().notEmpty().withMessage('Expense title is required'),
  body('amount').isFloat({ min: 0.01 }).withMessage('Amount must be greater than 0'),
  body('category')
    .optional()
    .isIn(['food', 'transportation', 'lodging', 'activities', 'shopping', 'other'])
    .withMessage('Invalid expense category'),
  validate,
];

module.exports = {
  validate,
  registerValidation,
  loginValidation,
  createTripValidation,
  updateTripValidation,
  addItineraryValidation,
  shareTripValidation,
  expenseValidation,
};
