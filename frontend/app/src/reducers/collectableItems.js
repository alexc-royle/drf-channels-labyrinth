const collectableItems = (state = {
    all: {},
    byGame: {}
}, action) => {
  switch(action.type) {
    case "GAME_COLLECTABLE_ITEMS_RESPONSE_RECEIVED":
      return {
        all: {
            ...state.all,
            ...action.response.entities.collectableItem
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

export default collectableItems;

export const getAllCollectableItems = (state) => state.all;
export const getCollectableItem = (state, gamePieceId) => (gamePieceId in state.all) ? state.all[gamePieceId] : false;
export const getCollectableItemsByGame = (state, gameId) => (gameId in state.byGame) ? state.byGame[gameId] : false;
