import React, { useCallback } from 'react';
import { Switch, Route, useRouteMatch } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import shortid from 'shortid';
import PrivateRoute from '../hoc/PrivateRoute';
import GamesList from './GamesList';
import GameWrapper from './GameWrapper';
import { createGame } from '../actions';
import { getGame } from '../reducers';



const LoggedInContent = () => {
    const { path } = useRouteMatch();
    return (
        <Switch>
            <Route exact path={`${path}`} component={Lobby} />
            <Route path={`${path}game/:gameId`} component={GameWrapper} />
        </Switch>
    );
}

const Lobby = () => {
  const dispatch = useDispatch();
  const callCreateGame = useCallback(() => {
    const newGameId = shortid.generate();
    dispatch(createGame(newGameId));
  }, [dispatch]);
  return (
    <>
      <h2>Lobby</h2>
      <button onClick={callCreateGame}>Create Game</button>
      <GamesList />
    </>
  );
}


const PrivateLoggedInContent = PrivateRoute(LoggedInContent);
export default PrivateLoggedInContent;
