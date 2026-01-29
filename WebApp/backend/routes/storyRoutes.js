const express = require("express");
const Story = require("../models/Story");
const translateEmojiStory = require("../translation");

const router = express.Router();

// Live translation preview
router.post("/translate", (req, res) => {
  const { emojiSequence } = req.body;
  if (!emojiSequence || emojiSequence.length === 0)
    return res.status(400).json({ error: "No emojis provided" });

  const translation = translateEmojiStory(emojiSequence);
  res.json({ translation });
});

module.exports = router;
