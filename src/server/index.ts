import * as WebSocket from 'ws';
import { Messages } from '../common/constants';

const wss = new WebSocket.Server({
  port: 8080
});

wss.on('connection', (sock) => {
  sock.on('message', (msg) => {
    console.log(msg);
    sock.send(msg);
  });

  sock.send(Messages.CONNECTED);
});
