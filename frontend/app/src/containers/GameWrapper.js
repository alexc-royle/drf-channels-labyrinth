import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { getGame, getGamePiecesByGame, getGamePiece, getPlayersByGame, getPlayer, getPlayersByGameAndPiece } from '../reducers';
import { requestGame, requestGamePieces, requestGamePlayers } from '../actions';

const useGetGame = ({ gameId }) => {
  const dispatch = useDispatch();
  useEffect(() => {
      dispatch(requestGame(gameId));
  }, [dispatch, gameId]);
  return useSelector(state => getGame(state, gameId));
}

const useGetGamePieces = ({ gameId }) => {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(requestGamePieces(gameId));
  }, [dispatch, gameId]);
  return useSelector(state => getGamePiecesByGame(state, gameId));
}

const useGetGamePlayers = ({ gameId }) => {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(requestGamePlayers(gameId));
  }, [dispatch, gameId]);
  return useSelector(state => getPlayersByGame(state, gameId));
}

const GameWrapper = ({ match }) => {
    const gameId = match.params.gameId;
    const game = useGetGame({ gameId });
    if (game) {
        console.log(game);
        return (
          <GameDataLoader gameId={gameId} />
        );
    }
    return null;
}

export default GameWrapper;

const GameDataLoader = ({ gameId }) => {
  const gamePieces = useGetGamePieces({ gameId });
  const players = useGetGamePlayers({ gameId });
  if (gamePieces && players) {
    return (
      <div className="gameWrapper">
        <PlayerTable players={players} />
        <GamePieceList gamePieces={gamePieces} />
      </div>
    )
  }
  return null;
}

const GamePieceList = ({ gamePieces }) => {
  console.log(gamePieces);
  if (gamePieces) {
    return gamePieces.map((gamePieceId) => <GamePieceWrapper gamePieceId={gamePieceId} />);
  }
  return null;
}

const GamePieceWrapper = ({ gamePieceId }) => {
    const gamePiece = useSelector(state => getGamePiece(state, gamePieceId));
    if (gamePiece && gamePiece.order) {
      return (<GamePiece gamePiece={gamePiece} />);
    }
    return null;
}

const GamePiece = ({ gamePiece }) => {
  const { id, game, orientation, collectable_item, order } = gamePiece;
  const players = useSelector(state => getPlayersByGameAndPiece(state, game, id));
  return (
    <p>
      {id} : {order} : {players.join(',')} : { orientation } : { collectable_item }
    </p>
  );
}

const PlayerTable = ({ players }) => {
  if (players) {
    return players.map((playerId) => <PlayerTableItemWrapper playerId={playerId} />);
  }
  return null;
}

const PlayerTableItemWrapper = ({ playerId }) => {
  const player = useSelector(state => getPlayer(state, playerId));
  if (player) {
    return <PlayerTableItem player={player} />
  }
}

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
