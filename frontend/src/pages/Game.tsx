import React, { useState, useEffect } from "react";
import camelize from "camelize-ts";

import Chat from "../components/Chat";
import {
  ChatUpdateTypes,
  ComponentType,
  UpdateDestination,
  UpdateType,
} from "../constants";
import {
  ChatComponentItf,
  ChatNewLineItf,
  ComponentItf,
  ComponentUpdateDetailsItf,
  SetSceneUpdateItf,
  UpdateComponentUpdateItf,
  ComponentUpdateItf,
} from "../interfaces";
import useWebsocket from "../useWebsocket";
import { toSnakeKeys } from "../utilities";

interface GameProps {
  gameId: string;
}

const Game = ({ gameId }: GameProps) => {
  const [components, setComponents] = useState<ComponentItf[]>([]);

  const onComponentUpdate = (details: ComponentUpdateDetailsItf) => {
    const { componentId, componentUpdate } = details;
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
      switch (componentUpdate.type) {
        case ChatUpdateTypes.NEW_LINE:
          const newLineDetails = componentUpdate as ChatNewLineItf;
          chatComponent.lines = [...chatComponent.lines, newLineDetails.line];
          const newComponent = { ...component };
          const newComponents = components.splice(
            componentIdx,
            1,
            newComponent
          );
          setComponents([...newComponents]);
          break;
        default:
          console.error(
            `Unhandled component update type ${componentUpdate.type}`
          );
      }
    }
  };

  const onComponentsSet = (components: ComponentItf[]) => {
    setComponents(components);
  };

  const url = `ws://localhost:8000/games/${gameId}`;
  const { sendMessage, lastMessage, isConnected } = useWebsocket({
    url,
  });

  const sendComponentUpdate = (
    componentId: string,
    componentUpdate: ComponentUpdateItf
  ) => {
    const componentUpdateDetails: ComponentUpdateDetailsItf = {
      componentId,
      componentUpdate,
    };
    const update: UpdateComponentUpdateItf = {
      destination: UpdateDestination.SERVER,
      type: UpdateType.UPDATE_COMPONENT,
      details: componentUpdateDetails,
    };
    const updateData = JSON.stringify(toSnakeKeys(update));
    sendMessage(updateData);
  };

  useEffect(() => {
    if (lastMessage) {
      const jsonString = JSON.parse(lastMessage);
      const parsedJson = JSON.parse(jsonString);
      switch (parsedJson.type) {
        case UpdateType.SET_SCENE:
          const {
            details: { components },
          } = camelize<SetSceneUpdateItf>(parsedJson);
          console.log(`Components: ${JSON.stringify(components)}`);
          onComponentsSet(components);
          break;
        case UpdateType.UPDATE_COMPONENT:
          const { details } = camelize<UpdateComponentUpdateItf>(parsedJson);
          onComponentUpdate(details);
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
        const onComponentUpdate = (componentUpdate: ComponentUpdateItf) =>
          sendComponentUpdate(component.id, componentUpdate);
        return (
          <Chat
            key={chatComponent.id}
            id={chatComponent.id}
            lines={chatComponent.lines}
            sendComponentUpdate={onComponentUpdate}
          />
        );
      })}
    </div>
  );
};

export default Game;
