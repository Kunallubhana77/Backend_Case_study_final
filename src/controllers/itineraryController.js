const Itinerary = require('../models/Itinerary');
const Trip = require('../models/Trip');

/**
 * @desc    Get all day-by-day itineraries for a trip
 * @route   GET /api/trips/:id/itinerary
 * @access  Private
 */
const getItineraries = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id);

    if (!trip) {
      return res.status(404).json({
        success: false,
        message: 'Trip not found',
      });
    }

    // Permission check
    const isOwner = trip.owner.toString() === req.user._id.toString();
    const isCollaborator = trip.collaborators.some(
      (c) => c.user.toString() === req.user._id.toString()
    );

    if (!isOwner && !isCollaborator && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'You do not have permission to view this itinerary',
      });
    }

    const itineraries = await Itinerary.find({ trip: req.params.id }).sort({ dayNumber: 1 });

    res.status(200).json({
      success: true,
      count: itineraries.length,
      data: itineraries,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Add or update day-by-day itinerary with activities to a trip
 * @route   POST /api/trips/:id/itinerary
 * @access  Private
 */
const addItineraryDay = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id);

    if (!trip) {
      return res.status(404).json({
        success: false,
        message: 'Trip not found',
      });
    }

    // Permission check: owner or editor
    const isOwner = trip.owner.toString() === req.user._id.toString();
    const isEditor = trip.collaborators.some(
      (c) => c.user.toString() === req.user._id.toString() && c.role === 'editor'
    );

    if (!isOwner && !isEditor && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'You do not have permission to modify this trip itinerary',
      });
    }

    const { dayNumber, date, title, notes, activities } = req.body;

    // Check if itinerary day already exists for this trip
    let itinerary = await Itinerary.findOne({
      trip: trip._id,
      dayNumber: Number(dayNumber),
    });

    if (itinerary) {
      // Append or replace activities if provided
      if (title !== undefined) itinerary.title = title;
      if (date !== undefined) itinerary.date = date;
      if (notes !== undefined) itinerary.notes = notes;
      if (activities && Array.isArray(activities)) {
        itinerary.activities.push(...activities);
      }
      await itinerary.save();

      return res.status(200).json({
        success: true,
        message: `Itinerary for Day ${dayNumber} updated successfully`,
        data: itinerary,
      });
    }

    // Create new day itinerary
    itinerary = await Itinerary.create({
      trip: trip._id,
      dayNumber: Number(dayNumber),
      date: date || null,
      title: title || `Day ${dayNumber}`,
      notes: notes || '',
      activities: activities || [],
    });

    res.status(201).json({
      success: true,
      message: `Itinerary for Day ${dayNumber} created successfully`,
      data: itinerary,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Update a specific itinerary day
 * @route   PUT /api/trips/:id/itinerary/:itineraryId
 * @access  Private
 */
const updateItineraryDay = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id);
    if (!trip) {
      return res.status(404).json({ success: false, message: 'Trip not found' });
    }

    const isOwner = trip.owner.toString() === req.user._id.toString();
    const isEditor = trip.collaborators.some(
      (c) => c.user.toString() === req.user._id.toString() && c.role === 'editor'
    );

    if (!isOwner && !isEditor && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'You do not have permission to edit this itinerary',
      });
    }

    const updated = await Itinerary.findOneAndUpdate(
      { _id: req.params.itineraryId, trip: req.params.id },
      req.body,
      { new: true, runValidators: true }
    );

    if (!updated) {
      return res.status(404).json({ success: false, message: 'Itinerary day not found' });
    }

    res.status(200).json({
      success: true,
      message: 'Itinerary day updated successfully',
      data: updated,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Delete an itinerary day
 * @route   DELETE /api/trips/:id/itinerary/:itineraryId
 * @access  Private
 */
const deleteItineraryDay = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id);
    if (!trip) {
      return res.status(404).json({ success: false, message: 'Trip not found' });
    }

    const isOwner = trip.owner.toString() === req.user._id.toString();
    const isEditor = trip.collaborators.some(
      (c) => c.user.toString() === req.user._id.toString() && c.role === 'editor'
    );

    if (!isOwner && !isEditor && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'You do not have permission to delete this itinerary',
      });
    }

    const deleted = await Itinerary.findOneAndDelete({
      _id: req.params.itineraryId,
      trip: req.params.id,
    });

    if (!deleted) {
      return res.status(404).json({ success: false, message: 'Itinerary day not found' });
    }

    res.status(200).json({
      success: true,
      message: 'Itinerary day deleted successfully',
      data: {},
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getItineraries,
  addItineraryDay,
  updateItineraryDay,
  deleteItineraryDay,
};
