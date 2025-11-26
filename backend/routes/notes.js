const express = require('express');
const Note = require('../models/Note');
const auth = require('../middleware/auth');
const router = express.Router();

router.get('/', auth, async (req, res) => {
  try {
    const { search, tag, favorite } = req.query;
    const query = { user: req.user.userId };
    
    if (search) {
      query.$text = { $search: search };
    }
    if (tag) {
      query.tags = tag;
    }
    if (favorite === 'true') {
      query.isFavorite = true;
    }
    
    const notes = await Note.find(query).sort({ isPinned: -1, updatedAt: -1 });
    res.json(notes);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.post('/', auth, async (req, res) => {
  try {
    const note = new Note({
      ...req.body,
      user: req.user.userId
    });
    await note.save();
    res.status(201).json(note);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.put('/:id', auth, async (req, res) => {
  try {
    const note = await Note.findOneAndUpdate(
      { _id: req.params.id, user: req.user.userId },
      req.body,
      { new: true }
    );
    if (!note) return res.status(404).json({ message: 'Note not found' });
    res.json(note);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.put('/:id/pin', auth, async (req, res) => {
  try {
    const note = await Note.findOneAndUpdate(
      { _id: req.params.id, user: req.user.userId },
      { isPinned: req.body.isPinned },
      { new: true }
    );
    if (!note) return res.status(404).json({ message: 'Note not found' });
    res.json(note);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.put('/:id/favorite', auth, async (req, res) => {
  try {
    const note = await Note.findOneAndUpdate(
      { _id: req.params.id, user: req.user.userId },
      { isFavorite: req.body.isFavorite },
      { new: true }
    );
    if (!note) return res.status(404).json({ message: 'Note not found' });
    res.json(note);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.get('/stats', auth, async (req, res) => {
  try {
    const totalNotes = await Note.countDocuments({ user: req.user.userId });
    const pinnedNotes = await Note.countDocuments({ user: req.user.userId, isPinned: true });
    const favoriteNotes = await Note.countDocuments({ user: req.user.userId, isFavorite: true });
    const tags = await Note.distinct('tags', { user: req.user.userId });
    
    res.json({ totalNotes, pinnedNotes, favoriteNotes, totalTags: tags.length });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.put('/:id/share', auth, async (req, res) => {
  try {
    const shareId = Math.random().toString(36).substring(2, 15);
    const note = await Note.findOneAndUpdate(
      { _id: req.params.id, user: req.user.userId },
      { isPublic: req.body.isPublic, shareId: req.body.isPublic ? shareId : null },
      { new: true }
    );
    if (!note) return res.status(404).json({ message: 'Note not found' });
    res.json(note);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.get('/shared/:shareId', async (req, res) => {
  try {
    const note = await Note.findOne({ shareId: req.params.shareId, isPublic: true });
    if (!note) return res.status(404).json({ message: 'Note not found' });
    res.json(note);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get('/analytics', auth, async (req, res) => {
  try {
    const notes = await Note.find({ user: req.user.userId });
    const totalWords = notes.reduce((sum, note) => sum + note.content.split(' ').length, 0);
    const avgWordsPerNote = notes.length ? Math.round(totalWords / notes.length) : 0;
    const mostUsedTags = {};
    
    notes.forEach(note => {
      note.tags.forEach(tag => {
        mostUsedTags[tag] = (mostUsedTags[tag] || 0) + 1;
      });
    });
    
    const topTags = Object.entries(mostUsedTags)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
      .map(([tag, count]) => ({ tag, count }));
    
    res.json({ totalWords, avgWordsPerNote, topTags, notesThisWeek: notes.filter(n => 
      new Date(n.createdAt) > new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    ).length });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.delete('/:id', auth, async (req, res) => {
  try {
    const note = await Note.findOneAndDelete({ _id: req.params.id, user: req.user.userId });
    if (!note) return res.status(404).json({ message: 'Note not found' });
    res.json({ message: 'Note deleted' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;