import * as WebSocket from "ws";
import { BaseUser } from "./baseUser";
import { BaseMessage } from "./baseMessage";

interface BaseGameProps {}

export abstract class BaseGame<U extends BaseUser, M extends BaseMessage> {
  users: U[];

  constructor(props: BaseGameProps) {
    this.users = [];
  }

  start(serverProps: WebSocket.ServerOptions) {
    const wss = new WebSocket.Server(serverProps);
    wss.on("connection", (sock: WebSocket) => this.handleNewConnections(sock));
  }

  handleNewConnections(sock: WebSocket) {
    const allowConnection = this.preNewConnection(sock);
    if (allowConnection) {
      this.onNewConnection(sock);
      this.postNewConnection(sock);
    } else {
      sock.close();
    }
    const user = this.createUser(sock);
    const allowUser = this.preNewUser(user);
    if (allowUser) {
      this.registerEvents(user, sock);
      this.onNewUser(user);
      this.postNewUser(user);
    } else {
      sock.close(); // TODO message?
    }
  }

  private registerEvents(user: U, sock: WebSocket) {
    sock.on("message", (data: WebSocket.Data) => {
      const message = this.decodeMessage(data);
      const allowMessage = this.preNewMessage(user, message);
      if (allowMessage) {
        this.onNewMessage(user, message);
        this.postNewMessage(user, message);
      }
    });

    sock.on("close", () => {
      this.preRemoveUser(user);
      this.onRemoveUser(user);
      this.postRemoveUser(user);
    });
  }

  abstract createUser(sock: WebSocket): U;
  abstract decodeMessage(data: WebSocket.Data): M;

  preNewConnection(sock: WebSocket): boolean {return true}
  onNewConnection(sock: WebSocket) {}
  postNewConnection(sock: WebSocket) {}

  preNewUser(user: U): boolean {return true}
  onNewUser(user: U) {}
  postNewUser(user: U) {}

  preNewMessage(user: U, message: M): boolean {return true}
  onNewMessage(user: U, message: M) {}
  postNewMessage(user: U, message: M) {}

  preRemoveUser(user: U): boolean {return true}
  onRemoveUser(user: U) {}
  postRemoveUser(user: U) {}
}
