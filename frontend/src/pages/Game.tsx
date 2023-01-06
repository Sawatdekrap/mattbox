import React, { useState, useEffect } from "react";
import camelize from "camelize-ts";

import Chat from "../components/Chat";
import { ComponentType, UpdateDestination, UpdateType } from "../constants";
import {
  ChatComponentItf,
  ComponentItf,
  SetComponentsUpdateItf,
  UpdateComponentUpdateItf,
} from "../interfaces";
import useWebsocket from "../useWebsocket";
import { toSnakeKeys } from "../utilities";

interface GameProps {
  gameId: string;
}

const Game = ({ gameId }: GameProps) => {
  const [components, setComponents] = useState<ComponentItf[]>([]);

  const onComponentUpdate = (componentId: string, data: any) => {
    const componentIdx = components.findIndex((c) => c.id === componentId);
    if (componentIdx === -1) {
      console.error(
        `Unable to update component with id '${componentId}', doesn't exist`
      );
      return;
    }

    const component = components[componentIdx];
    if (component.type === ComponentType.CHAT) {
      const chatComponent = component as ChatComponentItf;
      chatComponent.lines = [...chatComponent.lines, data.toString()];
      const newComponent = { ...component };
      const newComponents = components.splice(componentIdx, 1, newComponent);
      setComponents([...newComponents]);
    }
  };

  const onComponentsSet = (components: ComponentItf[]) => {
    setComponents(components);
  };

  const url = `ws://localhost:8000/games/${gameId}`;
  const { sendMessage, lastMessage, isConnected } = useWebsocket({
    url,
  });

  const sendComponentUpdate = (componentId: string, data: any) => {
    const componentUpdate: UpdateComponentUpdateItf = {
      destination: UpdateDestination.SERVER,
      type: UpdateType.UPDATE_COMPONENT,
      componentId,
      data,
    };
    const updateData = JSON.stringify(toSnakeKeys(componentUpdate));
    sendMessage(updateData);
  };

  useEffect(() => {
    if (lastMessage) {
      const jsonString = JSON.parse(lastMessage);
      const parsedJson = JSON.parse(jsonString);
      switch (parsedJson.type) {
        case UpdateType.SET_COMPONENTS:
          const { components } = camelize<SetComponentsUpdateItf>(parsedJson);
          console.log(`Components: ${JSON.stringify(components)}`);
          onComponentsSet(components);
          break;
        case UpdateType.UPDATE_COMPONENT:
          const { componentId, data } =
            camelize<UpdateComponentUpdateItf>(parsedJson);
          onComponentUpdate(componentId, data);
          break;
        default:
          console.error(`Update type '${parsedJson.type}' unhandled`);
          break;
      }
    }
  }, [lastMessage]);

  if (!isConnected) return <h3>Loading...</h3>;

  return (
    <div>
      {components.map((component) => {
        const chatComponent = component as ChatComponentItf;
        return (
          <Chat
            key={chatComponent.id}
            id={chatComponent.id}
            lines={chatComponent.lines}
            handleSubmission={(value) =>
              sendComponentUpdate(chatComponent.id, value)
            }
          />
        );
      })}
    </div>
  );
};

export default Game;
