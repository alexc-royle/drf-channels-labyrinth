// import gamePiece from './gamePiece';

const players = (state = {
    all: {},
    byGame: {}
}, action) => {
  switch(action.type) {
    case "GAME_PLAYER_RESPONSE_RECEIVED":
      return {
        all: {
            ...state.all,
            ...action.response.entities.player
        },
        byGame: {
            ...state.byGame,
            [action.gameId]: action.response.result
        }
      }
    default:
      return state;
  }
}

export default players;

export const getAllPlayers = (state) => state.all;
export const getPlayer = (state, playerId) => (playerId in state.all) ? state.all[playerId] : false;
export const getPlayersByGame = (state, gameId) => (gameId in state.byGame) ? state.byGame[gameId] : false;

export const getPlayersByGameAndPiece = (state, gameId, pieceId) => {
  const playersByGame = getPlayersByGame(state, gameId);
  return playersByGame.reduce((acc, playerId) => {
    const player = getPlayer(state, playerId);
    if (player.game_piece === pieceId) {
      return [...acc, playerId];
    }
    return acc;
  }, []);
}
