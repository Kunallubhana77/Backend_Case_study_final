const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { bucket, isFirebaseConfigured } = require('../config/firebase');

/**
 * Uploads a file buffer to Firebase Storage or local uploads directory fallback.
 * @param {Object} file - Multer file object
 * @param {String} folder - Destination folder (e.g. 'trips', 'itineraries')
 * @returns {Promise<{ url: String, storageType: String, filename: String }>}
 */
const uploadFile = async (file, folder = 'trips') => {
  if (!file) {
    throw new Error('No file provided for upload');
  }

  const ext = path.extname(file.originalname).toLowerCase() || '.jpg';
  const uniqueName = `${folder}/${Date.now()}-${crypto.randomBytes(6).toString('hex')}${ext}`;

  // If Firebase is configured, upload to Firebase Storage Bucket
  if (isFirebaseConfigured() && bucket) {
    try {
      const fileUpload = bucket.file(uniqueName);
      
      const stream = fileUpload.createWriteStream({
        metadata: {
          contentType: file.mimetype,
          metadata: {
            firebaseStorageDownloadTokens: crypto.randomUUID(),
          },
        },
      });

      await new Promise((resolve, reject) => {
        stream.on('error', (error) => reject(error));
        stream.on('finish', () => resolve());
        stream.end(file.buffer);
      });

      // Make public or get public URL
      await fileUpload.makePublic().catch(() => {});
      const publicUrl = `https://storage.googleapis.com/${bucket.name}/${fileUpload.name}`;

      return {
        url: publicUrl,
        storageType: 'firebase',
        filename: uniqueName,
      };
    } catch (err) {
      console.warn('[Firebase Storage] Upload failed, falling back to local storage:', err.message);
    }
  }

  // Local storage fallback
  const uploadsDir = path.join(__dirname, '../../uploads', folder);
  if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir, { recursive: true });
  }

  const localFilename = `${Date.now()}-${crypto.randomBytes(6).toString('hex')}${ext}`;
  const filePath = path.join(uploadsDir, localFilename);
  fs.writeFileSync(filePath, file.buffer);

  const localUrl = `/uploads/${folder}/${localFilename}`;

  return {
    url: localUrl,
    storageType: 'local',
    filename: localFilename,
  };
};

module.exports = {
  uploadFile,
};
