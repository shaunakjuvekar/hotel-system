// server.js
const express = require('express');
const https = require('https');
const fs = require('fs');
const path = require('path');

const app = express();

const options = {
    key: fs.readFileSync(path.resolve(__dirname, './certs/server.key')), // replace with your key path
    cert: fs.readFileSync(path.resolve(__dirname, './certs/server.crt')), // replace with your certificate path
};

// Serve static files like CSS, JavaScript, images, etc.
app.use('/scripts', express.static(path.join(__dirname, 'scripts')));
app.use('/css', express.static(path.join(__dirname, 'css')));
app.use('/images', express.static(path.join(__dirname, 'images')));
app.use('/pages', express.static(path.join(__dirname, 'pages')));

// Serve the HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

https.createServer(options, app).listen(5000, () => {
    console.log('Server is running on port 5000');
});
