import React, { useState, useEffect } from "react";
import styled from "styled-components";

import { GameItf } from "../interfaces";

const GameItemList = styled.div``;

const GameItem = styled.button`
  width: 100%;
`;

interface GameListProps {
  setGameId: (gameId: string) => void;
}

const GameList = ({ setGameId }: GameListProps) => {
  const [games, setGames] = useState<GameItf[]>([]);
  const [loading, setLoading] = useState(true);
  const [newGameDisabled, setNewGameDisabled] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/games")
      .then((response) => response.json())
      .then((data) => {
        setGames(data);
        setLoading(false);
      })
      .catch(() => {
        console.error("Failed to retrieve games");
      });
  }, []);

  const clickNewGame = () => {
    setNewGameDisabled(true);
    fetch("http://localhost:8000/games", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: "Test" }),
    })
      .then((response) => response.json())
      .then((data) => {
        const newGameId = data["id"];
        setGameId(newGameId);
      })
      .catch(() => {
        console.error("Failed to create new game");
      })
      .finally(() => {
        setNewGameDisabled(false);
      });
  };

  return (
    <GameItemList>
      {loading ? (
        <h3>Loading...</h3>
      ) : (
        <>
          {games.map((game) => (
            <GameItem key={game.id} onClick={() => setGameId(game.id)}>
              {game.name}
            </GameItem>
          ))}
          <button disabled={newGameDisabled} onClick={clickNewGame}>
            New game
          </button>
        </>
      )}
    </GameItemList>
  );
};

export default GameList;
