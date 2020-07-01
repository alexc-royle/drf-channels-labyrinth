import React from 'react';

import hooks from '../hooks';
import PlayerTable from './PlayerTable';
import GamePieceList from './GamePieceList';

const GameDataLoader = ({ gameId }) => {
  const gamePieces = hooks.useGetGamePieces({ gameId });
  const players = hooks.useGetGamePlayers({ gameId });
  const orientations = hooks.useGetOrientations();
  const shapes = hooks.useGetShapes();
  const collectables = hooks.useGetGameCollectableItems({ gameId });
  if (gamePieces && players && orientations && shapes && collectables) {
    return (
      <div className="gameWrapper">
        <PlayerTable players={players} />
        <div className="board">
          <GamePieceList gamePieces={gamePieces} />
        </div>
      </div>
    )
  }
  return null;
}

export default GameDataLoader;
