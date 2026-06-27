const express = require('express');
const router = express.Router();

// Assume a mock database interaction
const database = {
  saveUserInfo: async function(userInfo) {
    // Simulate a database insert operation
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve('User info saved successfully');
      }, 1000);
    });
  }
};

// POST route for user info form submission
router.post('/submit', async (req, res) => {
  try {
    const userInfo = req.body;

    if (!userInfo.name || !userInfo.email) {
      return res.status(400).json({ message: 'Name and email are required.' });
    }

    const result = await database.saveUserInfo(userInfo);
    res.status(200).json({ message: result });
  } catch (error) {
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router;