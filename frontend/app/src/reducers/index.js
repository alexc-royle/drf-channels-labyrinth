import { combineReducers } from 'redux';
import login, * as fromLogin from './login';
import registration, * as fromRegistration from './register';
import user, * as fromUser from './user';
import games, * as fromGames from './games';
import tempNewGames, * as fromTempNewGames from './tempNewGames';
import gamePieces, * as fromGamePieces from './gamePieces';
import gamesPagination, * as fromGamesPagination from './gamesPagination';
import players, * as fromPlayers from './players';
import collectableItems, * as fromCollectableItems from './collectableItems';
import orientations, * as fromOrientations from './orientations';
import shapes, * as fromShapes from './shapes';

const app = combineReducers({
  login,
  registration,
  user,
  games,
  tempNewGames,
  gamesPagination,
  gamePieces,
  players,
  collectableItems,
  orientations,
  shapes
});
export default app;

export const getIsUserAuthenticated = (state) => fromUser.getIsUserAuthenticated(state.user);
export const getUserToken = (state) => fromUser.getUserToken(state.user);

export const getLoginUsername = (state) => fromLogin.getUsername(state.login);
export const getLoginPassword = (state) => fromLogin.getPassword(state.login);
export const getIsLoginError = (state) => fromLogin.getIsError(state.login);
export const getIsAwaitingLoginResponse = (state) => fromLogin.getIsAwaitingResponse(state.login);

export const getRegistrationUsername = (state) => fromRegistration.getUsername(state.registration);
export const getRegistrationEmail = (state) => fromRegistration.getEmail(state.registration);
export const getRegistrationPassword = (state) => fromRegistration.getPassword(state.registration);
export const getHasRegistrationErrors = (state) => fromRegistration.getHasErrors(state.registration);
export const getIsAwaitingRegistrationResponse = (state) => fromRegistration.getIsAwaitingResponse(state.registration);
export const getRegistrationUsernameErrors = (state) => fromRegistration.getUsernameErrors(state.registration);
export const getRegistrationEmailErrors = (state) => fromRegistration.getEmailErrors(state.registration);
export const getRegistrationPasswordErrors = (state) => fromRegistration.getPasswordErrors(state.registration);
export const getIsRegistrationSuccessful = (state) => fromRegistration.getIsSuccessful(state.registration);

export const getAllGames = (state) => fromGames.getAllGames(state.games);
export const getGame = (state, gameId) => fromGames.getGame(state.games, gameId);
export const getCurrentPagination = (state) => fromGamesPagination.getCurrentPagination(state.gamesPagination);

export const getTempNewGame = (state) => fromTempNewGames.getTempNewGame(state.tempNewgames);

export const getAllGamePieces = (state) => fromGamePieces.getAllGamePieces(state.gamePieces);
export const getGamePiece = (state, gamePieceId) => fromGamePieces.getGamePiece(state.gamePieces, gamePieceId);
export const getGamePiecesByGame = (state, gameId) => fromGamePieces.getGamePiecesByGame(state.gamePieces, gameId);

export const getAllPlayers = (state) => fromPlayers.getAllPlayers(state.players);
export const getPlayer = (state, playerId) => fromPlayers.getPlayer(state.players, playerId);
export const getPlayersByGame = (state, gameId) => fromPlayers.getPlayersByGame(state.players, gameId);
export const getPlayersByGameAndPiece = (state, gameId, pieceId) => fromPlayers.getPlayersByGameAndPiece(state.players, gameId, pieceId);

export const getAllCollectableItems = (state) => fromCollectableItems.getAllCollectableItems(state.collectableItems);
export const getCollectableItem = (state, collectableItemId) => fromCollectableItems.getCollectableItem(state.collectableItems, collectableItemId);
export const getCollectableItemsByGame = (state, gameId) => fromCollectableItems.getCollectableItemsByGame(state.collectableItems, gameId);

export const getAllOrientations = (state) => fromOrientations.getAllOrientations(state.orientations);
export const getOrientation = (state, orientationId) => fromOrientations.getOrientation(state.orientations, orientationId);
export const getOrientationsLoaded = (state) => fromOrientations.getOrientationsLoaded(state.orientations);
export const getOrientationsLoading = (state) => fromOrientations.getOrientationsLoading(state.orientations);

export const getAllShapes = (state) => fromShapes.getAllShapes(state.shapes);
export const getShape = (state, shapeId) => fromShapes.getShape(state.shapes, shapeId);
export const getShapesLoaded = (state) => fromShapes.getShapesLoaded(state.shapes);
export const getShapesLoading = (state) => fromShapes.getShapesLoading(state.shapes);

export const helpers = {
  getIsUserAuthenticated,
  getUserToken,
  getLoginUsername,
  getLoginPassword,
  getIsLoginError,
  getIsAwaitingLoginResponse,
  getRegistrationUsername,
  getRegistrationEmail,
  getRegistrationPassword,
  getHasRegistrationErrors,
  getIsAwaitingRegistrationResponse,
  getRegistrationUsernameErrors,
  getRegistrationEmailErrors,
  getRegistrationPasswordErrors,
  getIsRegistrationSuccessful
};
