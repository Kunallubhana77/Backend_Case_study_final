const Trip = require('../models/Trip');

/**
 * @desc    Get trip budget and expenses breakdown
 * @route   GET /api/trips/:id/expenses
 * @access  Private
 */
const getExpenses = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id).populate('budget.expenses.paidBy', 'name email');

    if (!trip) {
      return res.status(404).json({ success: false, message: 'Trip not found' });
    }

    const totalBudget = trip.budget.totalBudget || 0;
    const expenses = trip.budget.expenses || [];
    const totalSpent = expenses.reduce((sum, item) => sum + (item.amount || 0), 0);
    const remaining = totalBudget - totalSpent;

    // Breakdown by category
    const categoryBreakdown = expenses.reduce((acc, curr) => {
      acc[curr.category] = (acc[curr.category] || 0) + curr.amount;
      return acc;
    }, {});

    res.status(200).json({
      success: true,
      data: {
        totalBudget,
        totalSpent,
        remaining,
        currency: trip.budget.currency || 'USD',
        categoryBreakdown,
        expenses,
      },
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Add expense to trip
 * @route   POST /api/trips/:id/expenses
 * @access  Private
 */
const addExpense = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id);

    if (!trip) {
      return res.status(404).json({ success: false, message: 'Trip not found' });
    }

    const { title, category, amount, currency, notes, date } = req.body;

    const newExpense = {
      title,
      category: category || 'other',
      amount: Number(amount),
      currency: currency || trip.budget.currency || 'USD',
      notes: notes || '',
      date: date || new Date(),
      paidBy: req.user._id,
    };

    trip.budget.expenses.push(newExpense);
    await trip.save();

    res.status(201).json({
      success: true,
      message: 'Expense added successfully',
      data: trip.budget,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Delete an expense from trip
 * @route   DELETE /api/trips/:id/expenses/:expenseId
 * @access  Private
 */
const deleteExpense = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id);

    if (!trip) {
      return res.status(404).json({ success: false, message: 'Trip not found' });
    }

    const expenseIndex = trip.budget.expenses.findIndex(
      (e) => e._id.toString() === req.params.expenseId
    );

    if (expenseIndex === -1) {
      return res.status(404).json({ success: false, message: 'Expense not found' });
    }

    trip.budget.expenses.splice(expenseIndex, 1);
    await trip.save();

    res.status(200).json({
      success: true,
      message: 'Expense deleted successfully',
      data: trip.budget,
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getExpenses,
  addExpense,
  deleteExpense,
};
