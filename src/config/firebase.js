const admin = require('firebase-admin');

let firebaseApp = null;
let bucket = null;
let isConfigured = false;

try {
  if (
    process.env.FIREBASE_PROJECT_ID &&
    process.env.FIREBASE_CLIENT_EMAIL &&
    process.env.FIREBASE_PRIVATE_KEY
  ) {
    const privateKey = process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n');
    
    firebaseApp = admin.initializeApp({
      credential: admin.credential.cert({
        projectId: process.env.FIREBASE_PROJECT_ID,
        clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
        privateKey: privateKey,
      }),
      storageBucket: process.env.FIREBASE_STORAGE_BUCKET || `${process.env.FIREBASE_PROJECT_ID}.appspot.com`,
    });

    bucket = admin.storage().bucket();
    isConfigured = true;
    console.log('[Firebase] Admin SDK initialized successfully');
  } else {
    console.log('[Firebase] Credentials not provided in .env - File uploads will use local fallback storage');
  }
} catch (err) {
  console.warn('[Firebase] Initialization warning:', err.message);
  console.log('[Firebase] Continuing with local storage fallback');
}

module.exports = {
  admin,
  firebaseApp,
  bucket,
  isFirebaseConfigured: () => isConfigured,
};
