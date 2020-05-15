// import gamePiece from './gamePiece';

const gamePieces = (state = {
    all: {},
    byGame: {}
}, action) => {
  switch(action.type) {
    case "GAME_PIECES_RESPONSE_RECEIVED":
      return {
        all: {
            ...state.all,
            ...action.response.entities.gamePiece
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

export default gamePieces;

export const getAllGamePieces = (state) => state.all;
export const getGamePiece = (state, gamePieceId) => (gamePieceId in state.all) ? state.all[gamePieceId] : false;
export const getGamePiecesByGame = (state, gameId) => (gameId in state.byGame) ? state.byGame[gameId] : false;
