const patterns = [
  {
    pattern: ["🏃", "🌧️"],
    templates: ["Someone ran from the rain", "Quick dash through the storm"],
  },
  {
    pattern: ["🐱", "🐟"],
    templates: [
      "The cat spotted its favorite meal",
      "Feline fishing adventures",
    ],
  },
];

function translateEmojiStory(emojis) {
  for (const rule of patterns) {
    if (JSON.stringify(rule.pattern) === JSON.stringify(emojis)) {
      return rule.templates[Math.floor(Math.random() * rule.templates.length)];
    }
  }
  return "A mysterious emoji adventure happened 🤔";
}

module.exports = translateEmojiStory;
