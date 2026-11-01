const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// MongoDB connection
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/dealershipdb';

mongoose.connect(MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.log('MongoDB connection error:', err));

// Dealer Schema
const dealerSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  city: String,
  state: String,
  st: String,
  address: String,
  zip: String,
  lat: Number,
  long: Number,
  short_name: String,
  full_name: String,
});

// Review Schema
const reviewSchema = new mongoose.Schema({
  id: { type: Number, required: true },
  name: String,
  dealership: Number,
  review: String,
  purchase: Boolean,
  purchase_date: String,
  car_make: String,
  car_model: String,
  car_year: Number,
  sentiment: String,
});

const Dealer = mongoose.model('Dealer', dealerSchema);
const Review = mongoose.model('Review', reviewSchema);

// Seed data if empty
const seedDealers = async () => {
  const count = await Dealer.countDocuments();
  if (count === 0) {
    await Dealer.insertMany([
      { id: 1, city: 'Chicago', state: 'Illinois', st: 'IL', address: '123 Main St', zip: '60601', lat: 41.8781, long: -87.6298, short_name: 'chicago_best', full_name: 'Best Cars Chicago' },
      { id: 2, city: 'New York', state: 'New York', st: 'NY', address: '456 Broadway', zip: '10001', lat: 40.7128, long: -74.0060, short_name: 'nyc_best', full_name: 'Best Cars New York' },
      { id: 3, city: 'Los Angeles', state: 'California', st: 'CA', address: '789 Sunset Blvd', zip: '90028', lat: 34.0522, long: -118.2437, short_name: 'la_best', full_name: 'Best Cars Los Angeles' },
      { id: 4, city: 'Wichita', state: 'Kansas', st: 'KS', address: '321 West St', zip: '67201', lat: 37.6872, long: -97.3301, short_name: 'wichita_best', full_name: 'Best Cars Wichita' },
      { id: 5, city: 'Topeka', state: 'Kansas', st: 'KS', address: '654 Capital Ave', zip: '66603', lat: 39.0558, long: -95.6890, short_name: 'topeka_best', full_name: 'Best Cars Topeka' },
      { id: 6, city: 'Houston', state: 'Texas', st: 'TX', address: '987 Houston Rd', zip: '77001', lat: 29.7604, long: -95.3698, short_name: 'houston_best', full_name: 'Best Cars Houston' },
      { id: 7, city: 'Phoenix', state: 'Arizona', st: 'AZ', address: '147 Desert Way', zip: '85001', lat: 33.4484, long: -112.0740, short_name: 'phoenix_best', full_name: 'Best Cars Phoenix' },
    ]);
    console.log('Dealers seeded');
  }
};

const seedReviews = async () => {
  const count = await Review.countDocuments();
  if (count === 0) {
    await Review.insertMany([
      { id: 1, name: 'Alice Johnson', dealership: 1, review: 'Excellent service! The staff was very helpful and friendly.', purchase: true, purchase_date: '2023-05-15', car_make: 'Toyota', car_model: 'Camry', car_year: 2023, sentiment: 'positive' },
      { id: 2, name: 'Bob Smith', dealership: 1, review: 'Great experience overall. Would definitely recommend!', purchase: true, purchase_date: '2023-06-20', car_make: 'Ford', car_model: 'Explorer', car_year: 2022, sentiment: 'positive' },
      { id: 3, name: 'Carol Davis', dealership: 2, review: 'Average service. Nothing special but got what I needed.', purchase: false, purchase_date: '2023-07-10', car_make: 'Honda', car_model: 'Civic', car_year: 2023, sentiment: 'neutral' },
      { id: 4, name: 'David Wilson', dealership: 3, review: 'Fantastic services! Very professional team.', purchase: true, purchase_date: '2023-08-05', car_make: 'BMW', car_model: '3 Series', car_year: 2023, sentiment: 'positive' },
    ]);
    console.log('Reviews seeded');
  }
};

// Initialize data
mongoose.connection.once('open', () => {
  seedDealers();
  seedReviews();
});

// Routes
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealers = await Dealer.find({});
    res.json(dealers);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealers = await Dealer.find({ state: req.params.state });
    res.json(dealers);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealer = await Dealer.findOne({ id: parseInt(req.params.id) });
    res.json(dealer);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const reviews = await Review.find({ dealership: parseInt(req.params.id) });
    res.json(reviews);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/insertReview', async (req, res) => {
  try {
    const review = new Review(req.body);
    await review.save();
    res.json({ status: 200, message: 'Review inserted' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Dealer microservice running on port ${PORT}`));
