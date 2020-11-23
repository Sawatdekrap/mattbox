import * as WebSocket from "ws";
import { BaseUser } from "../baseUser";
import { BaseMessage } from "../baseMessage";
import { BaseGame } from "../baseGame";

class User extends BaseUser {}

class Message extends BaseMessage {
  data: string;

  constructor(data: WebSocket.Data) {
    super();
    this.data = data.toString();
  }
}

export class Game extends BaseGame<User, Message> {
  createUser(sock: WebSocket) {
    return new BaseUser({sock});
  }

  decodeMessage(data: WebSocket.Data): Message {
    return new Message(data.toString());
  }

  onNewMessage(user: User, message: Message) {
    console.log(`${user.uuid}: ${message.data}`)
    user.sock.send("Thanks");
  }
}
