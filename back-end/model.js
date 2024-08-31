const mongoose = require('mongoose');
const { Schema } = mongoose;
mongoose.connect('mongodb://localhost:27017/smart_parking_system', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('Database Connected!');
});

const userSchema = new Schema({
  name: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  },
  role: {
    type: String,
    default: "NORMAL",
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const User = mongoose.model('Custom_User', userSchema)


module.exports = User;
