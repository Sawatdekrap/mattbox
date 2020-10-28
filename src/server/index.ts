import { textSpanIntersectsWith, updateImportEqualsDeclaration } from 'typescript';
import * as WebSocket from 'ws';
import { Messages } from '../common/constants';

interface GameItf {
  capacity: number;
};

type UUID = string;

interface UserProps {
  uuid: UUID;
  sock: WebSocket;
};

class User {
  uuid: UUID;
  sock: WebSocket;
  game: GameItf;

  constructor(props: UserProps, game: GameItf) {
    this.uuid = props.uuid;
    this.sock = props.sock;
    this.game = game;

    this.registerEvents();
  };

  private onMessage(message: string){
    //
  };

  registerEvents() {
    this.sock.on('message', this.onMessage);
  };
};

// TODO move users to game?
class Server {
  users: Record<UUID, User>;
  game: GameItf;
  serverProps: WebSocket.ServerOptions;

  constructor(game: GameItf, serverProps: WebSocket.ServerOptions) {
    this.users = {};
    this.game = game;
    this.serverProps = serverProps;
  };

  private onConnection(sock: WebSocket) {
    const user = new User({
      uuid: (Math.random() * 20).toString(),
      sock: sock,
    }, this.game);

    if (Object.keys(this.users).length < this.game.capacity) {
      this.users[user.uuid] = user;
      sock.on('close', () => {
        delete this.users[user.uuid];
      });
    }
  };

  run() {
    const wss = new WebSocket.Server(this.serverProps);
    wss.on('connection', this.onConnection);
  };
};
