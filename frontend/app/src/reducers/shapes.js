
const shapes = (state = {
  all: {},
  loaded: false,
  loading: false
}, action) => {
  switch(action.type) {
    case "SHAPE_REQUEST_SUBMITTED":
      return {
        ...state,
        loading: true
      }
    case "SHAPE_RESPONSE_RECEIVED":
      return {
        all: {
          ...state,
          ...action.response.entities.shape
        },
        loaded: true,
        loading: false
      }
    default:
      return state;
  }
}

export default shapes;

export const getAllShapes = (state) => state.all;
export const getShape = (state, shapeId) => (shapeId in state.all) ? state.all[shapeId] : false;
export const getShapesLoaded = (state) => state.loaded;
export const getShapesLoading = (state) => state.loading;
