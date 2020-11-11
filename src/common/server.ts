import * as WebSocket from 'ws';

type UUID = string;

export abstract class BaseMessage {
  skip: boolean;
  constructor(data: WebSocket.Data) {this.skip = false;}
}

interface BaseUserProps {
  sock: WebSocket;
};

export class BaseUser {
  sock: WebSocket;
  uuid: UUID;
  connected: boolean;

  constructor(props: BaseUserProps) {
    this.sock = props.sock;
    this.uuid = (Math.random() * 99999999).toString();
    this.connected = true;
  };
};

interface BaseGameProps {
  capacity: number;
}

export abstract class BaseGame<U extends BaseUser, M extends BaseMessage> {
  capacity: number;
  users: Record<UUID, U>;

  constructor(props: BaseGameProps) {
   this.capacity = props.capacity;
   this.users = {};
  }

  start(serverProps: WebSocket.ServerOptions) {
    const wss = new WebSocket.Server(serverProps);
    // NOTE the following doesn't work: wss.on('connection', this.initNewConnection);
    wss.on('connection', (sock: WebSocket) => this.initNewConnection(sock));
  }

  abstract decodeMessage(data: WebSocket.Data): M;
  abstract createNewUser(sock: WebSocket): U;

  initNewConnection(sock: WebSocket) {
    const user = this.createNewUser(sock);
    if (Object.keys(this.users).length >= this.capacity){
      return;
    }
    this.registerEvents(user, sock);
    this.preNewUser(user);
    this.users[user.uuid] = user;
    this.postNewUser(user);
  }

  private registerEvents(user: U, sock: WebSocket) {
    sock.on('message', data => {
      const message = this.decodeMessage(data);
      const cleanMessage = this.preNewMessage(user, message);
      if (!cleanMessage.skip) {
        this.newMessage(user, cleanMessage);
        this.postNewMessage(user, cleanMessage);
      }
    });

    sock.on('close', (code, reason) => {
      this.preRemoveUser(user);
      user.connected = false;
      this.postRemoveUser(user);
    })
  }

  // User-overridable functions
  preNewUser(user: U) {}
  postNewUser(user: U) {}

  preNewMessage(user: U, message: M): M {return message;}
  postNewMessage(user: U, message: M) {}
  newMessage(user: U, message: M) {}

  preRemoveUser(user: U) {}
  postRemoveUser(user: U) {}
}
