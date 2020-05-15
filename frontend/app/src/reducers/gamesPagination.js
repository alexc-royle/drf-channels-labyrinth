
const gamesPagination = (state = {
  current: -1,
  pages: {}
}, action) => {
  switch(action.type) {
    case "GAMES_LIST_RESPONSE_RECEIVED":
      return {
        current: action.response.result,
        pages: {
          ...state.pages,
          ...action.response.entities.gamesPagination
        }
      }
    default:
      return state;
  }
}

export default gamesPagination;

export const getCurrentPagination = (state) => {
  if (state.current > -1) {
    return state.pages[state.current];
  }
  return [];
}
