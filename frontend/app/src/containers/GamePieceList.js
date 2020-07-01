import React from 'react';
import GamePieceWrapper from './GamePieceWrapper';

const GamePieceList = ({ gamePieces }) => {
  if (gamePieces) {
    return gamePieces.map((gamePieceId) => <GamePieceWrapper gamePieceId={gamePieceId} />);
  }
  return null;
}

export default GamePieceList;
