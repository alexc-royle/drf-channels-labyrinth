const gamePiece = (state = {
    id: 0,
    game: 0,
    orientation: null,
    collectable_item: null,
    order: null
}, action) => {
  switch(action.type) {
    case "GAME_PIECE_UPDATE":
      const { id, game, orientation, collectable_item, order } = action.payload;
      return {
        ...state,
        id,
        game,
        orientation,
        collectable_item,
        order
      }
    default:
      return state;
  }
}

export default gamePiece;
