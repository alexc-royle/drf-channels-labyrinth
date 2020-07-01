import React from 'react';

import hooks from '../hooks';
import './GamePiece.css';

const GamePiece = ({ gamePiece }) => {
  const { id: gamePieceId, game: gameId, orientation: orientationId, collectable_item: collectableItemId, order } = gamePiece;
  const players = hooks.useGetPlayersByGameAndPiece({ gameId, gamePieceId });
  const orientation = hooks.useGetOrientation({ orientationId });
  const openSides = ['up', 'down', 'left', 'right'].reduce((acc, value) => orientation[value] ? [...acc, value] : acc, []).join(' ');
  const shape = hooks.useGetShape({ shapeId: orientation.shape });
  const collectableItem = hooks.useGetGameCollectableItem({ collectableItemId });
  const collectableItemClass = collectableItem ? `collectable ${collectableItem.class_name}` : 'noCollectable';
  const classes = `gamePiece ${openSides} ${shape.title} ${collectableItemClass}`;
  return (
    <div className={classes}>
      <div className="outerWrapper">
        <div className="row top">
          <div className="column left"></div>
          <div className="column centre"></div>
          <div className="column right"></div>
        </div>
        <div className="row middle">
          <div className="column left"></div>
          <div className="column centre">
            <div className="corner-filler"></div>
            <div className="collectableHolder"></div>
          </div>
          <div className="column right"></div>
        </div>
        <div className="row bottom">
          <div className="column left"></div>
          <div className="column centre"></div>
          <div className="column right"></div>
        </div>
      </div>
    </div>
  );
}

export default GamePiece;
