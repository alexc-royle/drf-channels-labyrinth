import React from 'react';

import hooks from '../hooks';
import GameDataLoader from './GameDataLoader';

const GameWrapper = ({ match }) => {
    const gameId = match.params.gameId;
    const game = hooks.useGetGame({ gameId });
    if (game) {
        return (
          <GameDataLoader gameId={gameId} />
        );
    }
    return null;
}

export default GameWrapper;
