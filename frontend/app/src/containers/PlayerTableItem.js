import React from 'react';

const PlayerTableItem = ({ player }) => {
  const {
    id,
    game,
    user,
    game_piece,
    order,
    starting_position,
    starting_game_piece,
    current_turn,
    next_collectable_item_id,
    remaining_collectable_item_count,
    completed
  } = player;
  return (
    <div class="playerItem">
      <span>id: {id}</span> -
      <span>game: {game}</span> -
      <span>user: {user}</span> -
      <span>game piece: {game_piece}</span> -
      <span>order: {order}</span> -
      <span>starting position: {starting_position}</span> -
      <span>starting game piece: {starting_game_piece}</span> -
      <span>current turn: {current_turn ? 'yes' : 'no' }</span> -
      <span>next collectble: {next_collectable_item_id}</span> -
      <span>remaining count: {remaining_collectable_item_count}</span> -
      <span>completed: {completed ? 'yes' : 'no' }</span>
    </div>
  )
}

export default PlayerTableItem;
