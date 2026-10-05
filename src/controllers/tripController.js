const Trip = require('../models/Trip');
const User = require('../models/User');
const Itinerary = require('../models/Itinerary');
const Destination = require('../models/Destination');
const { uploadFile } = require('../services/firebaseStorageService');

/**
 * @desc    Get all trips for logged in user (owned or collaborated)
 * @route   GET /api/trips
 * @access  Private
 */
const getTrips = async (req, res, next) => {
  try {
    const { status, sort } = req.query;
    const query = {
      $or: [
        { owner: req.user._id },
        { 'collaborators.user': req.user._id },
      ],
    };

    if (status) {
      query.status = status;
    }

    let tripQuery = Trip.find(query)
      .populate('owner', 'name email avatar')
      .populate('collaborators.user', 'name email avatar');

    if (sort) {
      tripQuery = tripQuery.sort(sort);
    } else {
      tripQuery = tripQuery.sort({ startDate: 1 });
    }

    const trips = await tripQuery;

    res.status(200).json({
      success: true,
      count: trips.length,
      data: trips,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Get single trip by ID (with full itineraries and collaborators)
 * @route   GET /api/trips/:id
 * @access  Private
 */
const getTripById = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id)
      .populate('owner', 'name email avatar')
      .populate('collaborators.user', 'name email avatar')
      .populate('destination.destinationRef');

    if (!trip) {
      return res.status(404).json({
        success: false,
        message: 'Trip not found',
      });
    }

    // Check if user is owner or collaborator
    const isOwner = trip.owner._id.toString() === req.user._id.toString();
    const isCollaborator = trip.collaborators.some(
      (c) => c.user && c.user._id.toString() === req.user._id.toString()
    );

    if (!isOwner && !isCollaborator && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'You do not have permission to view this trip',
      });
    }

    // Fetch day-by-day itineraries for this trip
    const itineraries = await Itinerary.find({ trip: trip._id }).sort({ dayNumber: 1 });

    res.status(200).json({
      success: true,
      data: {
        ...trip.toObject(),
        itineraries,
      },
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Create a new trip
 * @route   POST /api/trips
 * @access  Private
 */
const createTrip = async (req, res, next) => {
  try {
    const {
      title,
      description,
      destination,
      startDate,
      endDate,
      budget,
      bookings,
      coverPhoto,
    } = req.body;

    // Handle destination if passed as string or object
    let destinationObj = { name: '', country: '' };
    if (typeof destination === 'string') {
      destinationObj.name = destination;
    } else if (typeof destination === 'object' && destination !== null) {
      destinationObj = destination;
    }

    // Check or auto-link with Destination model
    if (destinationObj.name) {
      const existingDest = await Destination.findOne({
        name: { $regex: new RegExp(`^${destinationObj.name}$`, 'i') },
      });
      if (existingDest) {
        destinationObj.destinationRef = existingDest._id;
        if (!destinationObj.country) destinationObj.country = existingDest.country;
      }
    }

    const trip = await Trip.create({
      title,
      description: description || '',
      destination: destinationObj,
      startDate,
      endDate,
      coverPhoto: coverPhoto || '',
      budget: budget || { totalBudget: 0, currency: 'USD', expenses: [] },
      bookings: bookings || [],
      owner: req.user._id,
      collaborators: [],
    });

    res.status(201).json({
      success: true,
      message: 'Trip created successfully',
      data: trip,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Update a trip
 * @route   PUT /api/trips/:id
 * @access  Private
 */
const updateTrip = async (req, res, next) => {
  try {
    let trip = await Trip.findById(req.params.id);

    if (!trip) {
      return res.status(404).json({
        success: false,
        message: 'Trip not found',
      });
    }

    // Check permission (owner or collaborator with editor role)
    const isOwner = trip.owner.toString() === req.user._id.toString();
    const isEditor = trip.collaborators.some(
      (c) => c.user.toString() === req.user._id.toString() && c.role === 'editor'
    );

    if (!isOwner && !isEditor && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'You do not have permission to update this trip',
      });
    }

    // Do not allow transferring ownership through regular update
    delete req.body.owner;

    trip = await Trip.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true,
    }).populate('owner', 'name email avatar');

    res.status(200).json({
      success: true,
      message: 'Trip updated successfully',
      data: trip,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Delete a trip
 * @route   DELETE /api/trips/:id
 * @access  Private
 */
const deleteTrip = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id);

    if (!trip) {
      return res.status(404).json({
        success: false,
        message: 'Trip not found',
      });
    }

    // Only owner can delete the trip
    if (trip.owner.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'Only the trip owner can delete this trip',
      });
    }

    // Cascade delete all day itineraries
    await Itinerary.deleteMany({ trip: trip._id });
    await trip.deleteOne();

    res.status(200).json({
      success: true,
      message: 'Trip and associated itineraries deleted successfully',
      data: {},
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Share trip with a collaborator
 * @route   POST /api/trips/:id/share
 * @access  Private
 */
const shareTrip = async (req, res, next) => {
  try {
    const { email, role } = req.body;
    const trip = await Trip.findById(req.params.id);

    if (!trip) {
      return res.status(404).json({
        success: false,
        message: 'Trip not found',
      });
    }

    // Only owner or editor can share
    const isOwner = trip.owner.toString() === req.user._id.toString();
    const isEditor = trip.collaborators.some(
      (c) => c.user.toString() === req.user._id.toString() && c.role === 'editor'
    );

    if (!isOwner && !isEditor && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'You do not have permission to invite collaborators to this trip',
      });
    }

    // Find the user to invite
    const collaboratorUser = await User.findOne({ email });
    if (!collaboratorUser) {
      return res.status(404).json({
        success: false,
        message: `No user found with email '${email}'. They must register on TripCraft first.`,
      });
    }

    // Prevent sharing with oneself
    if (collaboratorUser._id.toString() === trip.owner.toString()) {
      return res.status(400).json({
        success: false,
        message: 'Trip owner is already the creator of this trip',
      });
    }

    // Check if already a collaborator
    const existingIndex = trip.collaborators.findIndex(
      (c) => c.user.toString() === collaboratorUser._id.toString()
    );

    if (existingIndex !== -1) {
      // Update role
      trip.collaborators[existingIndex].role = role || 'viewer';
    } else {
      // Add collaborator
      trip.collaborators.push({
        user: collaboratorUser._id,
        role: role || 'viewer',
        addedAt: new Date(),
      });
    }

    await trip.save();
    await trip.populate('collaborators.user', 'name email avatar');

    res.status(200).json({
      success: true,
      message: `Trip successfully shared with ${collaboratorUser.name} (${collaboratorUser.email})`,
      data: trip,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Search trips by keyword (title, destination, description, activities)
 * @route   GET /api/trips/search?keyword=europe
 * @access  Private
 */
const searchTrips = async (req, res, next) => {
  try {
    const { keyword } = req.query;

    if (!keyword || keyword.trim() === '') {
      return res.status(400).json({
        success: false,
        message: 'Please provide a search keyword (e.g. /api/trips/search?keyword=europe)',
      });
    }

    const regex = new RegExp(keyword.trim(), 'i');

    // Find itineraries matching keyword in activity title, notes, or location
    const matchingItineraries = await Itinerary.find({
      $or: [
        { title: regex },
        { notes: regex },
        { 'activities.activity': regex },
        { 'activities.location': regex },
        { 'activities.notes': regex },
      ],
    }).select('trip');

    const itineraryTripIds = matchingItineraries.map((it) => it.trip);

    // Search query
    const searchQuery = {
      $and: [
        {
          $or: [
            { owner: req.user._id },
            { 'collaborators.user': req.user._id },
          ],
        },
        {
          $or: [
            { title: regex },
            { description: regex },
            { 'destination.name': regex },
            { 'destination.country': regex },
            { _id: { $in: itineraryTripIds } },
          ],
        },
      ],
    };

    const trips = await Trip.find(searchQuery)
      .populate('owner', 'name email avatar')
      .populate('collaborators.user', 'name email avatar')
      .sort({ createdAt: -1 });

    res.status(200).json({
      success: true,
      keyword,
      count: trips.length,
      data: trips,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Upload trip photo (cover photo or gallery photo) using Firebase Storage
 * @route   POST /api/trips/:id/photos
 * @access  Private
 */
const uploadTripPhoto = async (req, res, next) => {
  try {
    const trip = await Trip.findById(req.params.id);

    if (!trip) {
      return res.status(404).json({
        success: false,
        message: 'Trip not found',
      });
    }

    // Check permission
    const isOwner = trip.owner.toString() === req.user._id.toString();
    const isEditor = trip.collaborators.some(
      (c) => c.user.toString() === req.user._id.toString() && c.role === 'editor'
    );

    if (!isOwner && !isEditor && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'You do not have permission to upload photos for this trip',
      });
    }

    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: 'Please provide an image file to upload',
      });
    }

    const { isCover, caption } = req.body;
    const uploaded = await uploadFile(req.file, 'trips');

    if (isCover === 'true' || isCover === true) {
      trip.coverPhoto = uploaded.url;
    }

    trip.photos.push({
      url: uploaded.url,
      caption: caption || '',
      storageType: uploaded.storageType,
      uploadedAt: new Date(),
    });

    await trip.save();

    res.status(200).json({
      success: true,
      message: 'Photo uploaded successfully',
      data: {
        photoUrl: uploaded.url,
        storageType: uploaded.storageType,
        isCover: isCover === 'true' || isCover === true,
        trip,
      },
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getTrips,
  getTripById,
  createTrip,
  updateTrip,
  deleteTrip,
  shareTrip,
  searchTrips,
  uploadTripPhoto,
};
