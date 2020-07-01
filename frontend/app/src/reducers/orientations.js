
const orientations = (state = {
  all: {},
  loaded: false,
  loading: false
}, action) => {
  switch(action.type) {
    case "ORIENTATION_REQUEST_SUBMITTED":
      return {
        ...state,
        loading: true
      }
    case "ORIENTATION_RESPONSE_RECEIVED":
      return {
        all: {
          ...state.all,
          ...action.response.entities.orientation
        },
        loaded: true,
        loading: false
      }
    default:
      return state;
  }
}

export default orientations;

export const getAllOrientations = (state) => state.all;
export const getOrientation = (state, orientationId) => (orientationId in state.all) ? state.all[orientationId] : false;
export const getOrientationsLoaded = (state) => state.loaded;
export const getOrientationsLoading = (state) => state.loading;
