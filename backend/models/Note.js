const mongoose = require('mongoose');

const noteSchema = new mongoose.Schema({
  title: { type: String, required: true },
  content: { type: String, required: true },
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  isPinned: { type: Boolean, default: false },
  isFavorite: { type: Boolean, default: false },
  tags: [{ type: String }],
  color: { type: String, default: '#ffffff' },
  isPublic: { type: Boolean, default: false },
  shareId: { type: String, unique: true, sparse: true }
}, { timestamps: true });

noteSchema.index({ title: 'text', content: 'text' });

module.exports = mongoose.model('Note', noteSchema);