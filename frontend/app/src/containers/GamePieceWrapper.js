import React from 'react';

import hooks from '../hooks';
import GamePiece from './GamePiece';

const GamePieceWrapper = ({ gamePieceId }) => {
    const gamePiece = hooks.useGetGamePiece({ gamePieceId });
    if (gamePiece && gamePiece.order) {
      return (<GamePiece gamePiece={gamePiece} />);
    }
    return null;
}

export default GamePieceWrapper;
