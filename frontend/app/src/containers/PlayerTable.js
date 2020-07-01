import React from 'react';
import PlayerTableItemWrapper from './PlayerTableItemWrapper';

const PlayerTable = ({ players }) => {
  if (players) {
    return players.map((playerId) => <PlayerTableItemWrapper playerId={playerId} />);
  }
  return null;
}

export default PlayerTable;
