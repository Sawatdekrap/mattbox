import WebSocket from 'ws';

const ws = new WebSocket("ws://localhost:8080");
ws.on('open', () => {
  console.log('Client connected.');
  ws.send('User connecting!');
});

ws.on('close', () => {
  console.log('Connection has been closed');
  clearInterval(interval);
});

ws.on('message', data => {
  console.log(`Message from server with data ${data}`);
});

const interval = setInterval(() => {
  if (ws.OPEN) {
    console.log('Sending data...');
    ws.send('DATA!');
  }
}, 1000);
