import React, { useState } from "react";
import GameList from "./pages/GameList";
import Game from "./pages/Game";

function App() {
  const [gameId, setGameId] = useState<string | null>(null);

  if (gameId === null) return <GameList setGameId={setGameId}></GameList>;

  return <Game gameId={gameId} />;
}

export default App;
