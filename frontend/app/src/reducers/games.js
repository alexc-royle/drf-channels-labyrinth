import game from './game';

const games = (state = {}, action) => {
  switch(action.type) {
    case "GAME_SET_CURRENT_PLAYER":
    case "GAME_SET_STATUS_DSPLAY":
    case "GAME_UPDATE":
      const currentGame = state[action.payload.id];
      return {
          ...state,
          [action.payload.id]: game(currentGame, action)
      }
    case "GAMES_LIST_RESPONSE_RECEIVED":
    case "GAME_RESPONSE_RECEIVED":
      return {
        ...state,
        ...action.response.entities.game
      }
    default:
      return state;
  }
}

export default games;

export const getAllGames = (state) => state;
export const getGame = (state, gameId) => (gameId in state) ? state[gameId] : false;
