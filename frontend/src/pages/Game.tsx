import React, { useState, useEffect } from "react";
import camelize from "camelize-ts";

import Chat from "../components/Chat";
import { ComponentType, UpdateDestination, UpdateType } from "../constants";
import {
  ChatComponentItf,
  LayoutItf,
  ComponentUpdateItf,
  LayoutUpdateItf,
} from "../interfaces";
import useWebsocket from "../useWebsocket";
import { toSnakeKeys } from "../utilities";

interface GameProps {
  gameId: string;
}

const Game = ({ gameId }: GameProps) => {
  const [layout, setLayout] = useState<LayoutItf>({ components: {} });

  const onComponentUpdate = (componentId: string, data: any) => {
    const component = layout.components[componentId];
    if (component?.type === ComponentType.CHAT) {
      const chatComponent = component as ChatComponentItf;
      chatComponent.lines = [...chatComponent.lines, data.toString()];
      const newComponent = { ...component };
      const newComponents = { ...layout.components };
      newComponents[componentId] = newComponent;
      const newLayout = { ...layout, components: newComponents };
      setLayout(newLayout);
    }
  };

  const onLayoutUpdate = (newLayout: LayoutItf) => {
    setLayout(newLayout);
  };

  const url = `ws://localhost:8000/games/${gameId}`;
  const { sendMessage, lastMessage, isConnected } = useWebsocket({
    url,
  });

  const sendComponentUpdate = (componentId: string, data: any) => {
    const componentUpdate: ComponentUpdateItf = {
      destination: UpdateDestination.SERVER,
      type: UpdateType.COMPONENT,
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
        case UpdateType.LAYOUT:
          const { layout } = camelize<LayoutUpdateItf>(parsedJson);
          console.log(`Layout: ${JSON.stringify(layout)}`);
          onLayoutUpdate(layout);
          break;
        case UpdateType.COMPONENT:
          const { componentId, data } =
            camelize<ComponentUpdateItf>(parsedJson);
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
      {Object.values(layout.components).map((component) => {
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
