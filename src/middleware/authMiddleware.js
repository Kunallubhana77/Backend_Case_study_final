const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { admin, isFirebaseConfigured } = require('../config/firebase');

/**
 * Protect routes: verifies JWT or Firebase Auth token
 */
const protect = async (req, res, next) => {
  let token;

  if (
    req.headers.authorization &&
    req.headers.authorization.startsWith('Bearer')
  ) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (!token) {
    return res.status(401).json({
      success: false,
      message: 'Not authorized to access this route. No token provided.',
    });
  }

  try {
    // 1. Try standard JWT verification
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'tripcraft_jwt_secret_key_secure_2026_token');
      const user = await User.findById(decoded.id).select('-password');
      if (user) {
        req.user = user;
        return next();
      }
    } catch (jwtErr) {
      // If JWT verification fails and Firebase is configured, try Firebase Auth Token
      if (isFirebaseConfigured()) {
        try {
          const decodedFirebaseToken = await admin.auth().verifyIdToken(token);
          let user = await User.findOne({
            $or: [{ firebaseUid: decodedFirebaseToken.uid }, { email: decodedFirebaseToken.email }],
          });

          // If user doesn't exist yet, auto-provision
          if (!user) {
            user = await User.create({
              name: decodedFirebaseToken.name || decodedFirebaseToken.email.split('@')[0],
              email: decodedFirebaseToken.email,
              firebaseUid: decodedFirebaseToken.uid,
              avatar: decodedFirebaseToken.picture || '',
            });
          }

          req.user = user;
          return next();
        } catch (firebaseErr) {
          // Fall through to 401
        }
      }
      throw jwtErr;
    }

    return res.status(401).json({
      success: false,
      message: 'User belonging to this token no longer exists.',
    });
  } catch (error) {
    return res.status(401).json({
      success: false,
      message: 'Not authorized. Invalid or expired token.',
      error: error.message,
    });
  }
};

/**
 * Restrict by user role
 */
const authorize = (...roles) => {
  return (req, res, next) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        message: `User role '${req.user ? req.user.role : 'guest'}' is not authorized to access this route`,
      });
    }
    next();
  };
};

module.exports = {
  protect,
  authorize,
};
