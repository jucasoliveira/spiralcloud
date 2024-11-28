const express = require('express');
const fs = require('fs');
const app = express();
app.use(express.json());

// Add this line to serve static files
app.use(express.static(__dirname));


app.post('/add-to-logs', (req, res) => {
  const { log } = req.body;
  // add a line to the file
  fs.appendFileSync('metrics_node.txt', log + '\n', 'utf8');
  res.send('Log added!');
});

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.listen(3000, () => { // clear the file
    fs.writeFileSync('metrics_node.txt', '', 'utf8');
    console.log('Server running on http://localhost:3000')
});
