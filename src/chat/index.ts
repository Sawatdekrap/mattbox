import * as WebSocket from 'ws';
import { BaseGame, BaseUser, BaseMessage } from '../server';

class Message extends BaseMessage {
  text: string;
  constructor(data: WebSocket.Data) {
    super(data);
    this.text = data.toString();
  }
}

class User extends BaseUser {}

class Game extends BaseGame<User, Message> {
  createNewUser(sock: WebSocket): User {
    return new User({sock: sock});
  }
  decodeMessage(data: WebSocket.Data): Message {
    return new Message(data);
  }
  postNewUser(user: User) {
    console.log(`User (${user.uuid}) has connected`)
  }
  postNewMessage(user: User, message: Message) {
    console.log(`Message from ${user.uuid}: ${message.text}`)
  }
  postRemoveUser(user: User) {
    console.log(`User ${user.uuid} has disconnected`);
  }
}

const game = new Game({capacity: 8});
game.start({port: 8080});
