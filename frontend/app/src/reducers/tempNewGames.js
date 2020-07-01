const tempNewGames = (state = {}, action) => {
  switch(action.type) {
    case "CREATE_GAME_REQUEST_SUBMITTED":
      return {
          ...state,
          [action.tempGameId]: false
      }
    case "CREATE_GAME_RESPONSE_RECEIVED":
      return {
        ...state,
        [action.tempGameId]: action.response.result
      }
    default:
      return state;
  }
}

export default tempNewGames;

export const getTempNewGame = (state, gameTempId) => (gameTempId in state) ? state[gameTempId] : false;
