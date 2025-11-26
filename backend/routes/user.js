const express = require('express');
const User = require('../models/User');
const auth = require('../middleware/auth');
const router = express.Router();

router.put('/update-username', auth, async (req, res) => {
  try {
    const { username } = req.body;
    const user = await User.findByIdAndUpdate(
      req.user.userId,
      { username },
      { new: true }
    );
    res.json({ user: { id: user._id, username: user.username, email: user.email } });
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

module.exports = router;