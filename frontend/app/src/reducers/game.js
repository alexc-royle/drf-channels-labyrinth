const game = (state = {
    id: 0,
    creator: 0,
    current_player: null,
    status_display: ''
}, action) => {
  switch(action.type) {
    case "GAME_SET_CURRENT_PLAYER":
      return {...state, current_player: action.payload.current_player}
    case "GAME_SET_STATUS_DSPLAY":
      return {...state, status_display: action.payload.status_display}
    case "GAME_UPDATE":
      const { id, creator, current_player, status_display } = action.payload;
      return {
        ...state,
        id,
        creator,
        current_player,
        status_display
      }
    default:
      return state;
  }
}

export default game;
