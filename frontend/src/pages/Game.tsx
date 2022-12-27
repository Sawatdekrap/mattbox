import React, { useState } from "react";

import { LayoutItf } from "../interfaces";
import useWebsocket from "../useWebsocket";

interface GameProps {
  gameId: string;
}

const Game = ({ gameId }: GameProps) => {
  const [layout, setLayout] = useState<LayoutItf>({ components: [] });

  const onComponentUpdate = () => {};

  const onLayoutUpdate = (newLayout: LayoutItf) => {
    setLayout(newLayout);
  };

  const { sendComponentUpdate } = useWebsocket({
    gameId,
    onComponentUpdate,
    onLayoutUpdate,
  });

  if (!layout) return <h3>Loading...</h3>;

  return (
    <div>
      {layout.components.map((component) => (
        <div key={component.id}>{component.id}</div>
      ))}
    </div>
  );
};

export default Game;
