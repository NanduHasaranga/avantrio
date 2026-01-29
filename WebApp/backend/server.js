const express = require("express");
const cors = require("cors");
const connectDB = require("./db");
const storyRoutes = require("./routes/storyRoutes");

const app = express();
app.use(cors());
app.use(express.json());

connectDB();

app.use("/api", storyRoutes);

app.listen(5000, () => console.log("Server running on http://localhost:5000"));
