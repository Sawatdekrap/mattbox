import * as WebSocket from "ws";
import { UUID } from "common/types";

export interface BaseUserProps {
  sock: WebSocket;
};

export class BaseUser {
  sock: WebSocket;
  uuid: UUID;
  connected: boolean;

  constructor(props: BaseUserProps) {
    this.sock = props.sock;
    this.uuid = (Math.random() * 9999999999).toString() // TODO change
    this.connected = true;
  }
}
