const mongoose = require("mongoose");

const connectDB = async () => {
  await mongoose.connect("mongodb://localhost:27017/emoji_story");
  console.log("MongoDB Connected");
};

module.exports = connectDB;
