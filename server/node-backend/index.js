const express = require('express');
const dotenv = require('dotenv');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const cookieParser = require('cookie-parser');
const ws = require('ws');
const Message = require('./models/message');
const fs = require('fs')
const path = require('path');
dotenv.config();

mongoose.connect(process.env.MONGO_URL)
  .then(() => {
    console.log('Mongoose Connected');
  })
  .catch((err) => {
    console.error('Error Connecting:', err);
  });

const app = express();
app.use(express.json());
app.use(cookieParser());
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
app.use(cors({
  credentials: true,
  origin: 'http://localhost:5173',
}));

const jwtSec = 'django-insecure-3fr_%q88m)p8-yp1c7^af^%(hox8p*9nl2i20goum(+m$%5sg_';
const bcryptSalt = bcrypt.genSaltSync(10);

const server = app.listen(4000, () => {
  console.log('Server is running on port 4000');
});

app.get('/messages/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    const userData = await getUserDataFromRequest(req);

    // Convert numerical userId to 24-character hex string
    const recipientIdHex = Number(userId).toString(16).padStart(24, '0');
    const senderIdHex = Number(userData.id).toString(16).padStart(24, '0');

    // Convert to ObjectId
    const recipientId = new mongoose.Types.ObjectId(recipientIdHex);
    const senderId = new mongoose.Types.ObjectId(senderIdHex);

    console.log('Recipient ID:', recipientId);
    console.log('Sender ID:', senderId);

    // Query the messages
    const messages = await Message.find({
      $or: [
        { sender: senderId, recipient: recipientId },
        { sender: recipientId, recipient: senderId }
      ]
    }).sort({ createdAt: 1 });


    res.json(messages);
  } catch (error) {
    console.error('Error fetching messages:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});


function getUserDataFromRequest(req) {
  return new Promise((resolve, reject) => {
    const token = req.headers.authorization?.split(' ')[1]; // Token from Bearer header
    if (token) {
      jwt.verify(token, jwtSec, (err, userData) => {
        if (err) {
          console.error('JWT verification error:', err);
          return reject(err);
        }
        resolve(userData);
      });
    } else {
      reject(new Error('No token provided'));
    }
  });
}

const wss = new ws.WebSocketServer({ server });

wss.on('connection', (connection, req) => {
  function notifyAboutOnlinePeople() {
    const onlineUsers = [...wss.clients].filter(c => c.userId).map(c => ({
      userId: c.userId,
      username: c.username,
    }));
    console.log(onlineUsers)
    wss.clients.forEach(client => {
      client.send(JSON.stringify({ online: onlineUsers }));
    });
  }

  connection.isAlive = true;

  const pingInterval = setInterval(() => {
    connection.ping();
    connection.deathTimer = setTimeout(() => {
      connection.isAlive = false;
      clearInterval(pingInterval);
      connection.terminate();
      notifyAboutOnlinePeople(); 
    }, 3000);
  }, 10000); 

  connection.on('pong', () => {
    clearTimeout(connection.deathTimer);
    connection.isAlive = true;
  });

  const urlParams = new URLSearchParams(req.url.split('?')[1]);
  const token = urlParams.get('token');
  
  if (token) {
    jwt.verify(token, jwtSec, (err, userData) => {
      if (err) {
        console.error('JWT verification error:', err);
        connection.close(); // Close the connection if JWT verification fails
        return; // Exit early on JWT error
      }

      const { id, username } = userData;
      connection.userId = id;
      connection.username = username;
      console.log('New connection established:', connection.username);


      // Notify all clients about the updated list of online users
      notifyAboutOnlinePeople();

      // Set up message handling only after the user is authenticated
      connection.on('message', async (message) => {
        const { recipient, text } = JSON.parse(message.toString());

        console.log('Sender ID:', connection.userId); // Ensure sender ID is correctly set

        if (recipient && text && connection.userId) {
          // Convert recipient and sender to valid MongoDB ObjectId
          const recipientIdHex = Number(recipient).toString(16).padStart(24, '0');
          const senderIdHex = Number(connection.userId).toString(16).padStart(24, '0');

          const senderObjectId = new mongoose.Types.ObjectId(senderIdHex);
          const recipientObjectId = new mongoose.Types.ObjectId(recipientIdHex);

          // Create a new message in the database
          const messageDoc = await Message.create({
            sender: senderObjectId,
            recipient: recipientObjectId,
            text: text,
          });

          // Send the message to the recipient and sender in real-time
          [...wss.clients]
            .filter(c => c.userId === recipient || c.userId === connection.userId)
            .forEach(c => c.send(JSON.stringify({
              text,
              sender: senderObjectId,
              recipient,
              _id: messageDoc._id,
            })));
        } else {
          console.log('Message data missing or invalid.');
        }
      });
    });
  } else {
    console.log('No token provided, closing connection.');
    connection.close(); // Close the connection if no token is provided
  }
});
