import React from 'react';

import hooks from '../hooks';
import PlayerTableItem from './PlayerTableItem';

const PlayerTableItemWrapper = ({ playerId }) => {
  const player = hooks.useGetPlayer({ playerId });
  if (player) {
    return <PlayerTableItem player={player} />
  }
}

export default PlayerTableItemWrapper;
