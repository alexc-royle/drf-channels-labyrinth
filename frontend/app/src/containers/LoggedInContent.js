import React from 'react';
import { Switch, Route, useRouteMatch } from 'react-router-dom';
import PrivateRoute from '../hoc/PrivateRoute';
import GamesList from './GamesList';
import GameWrapper from './GameWrapper';


const LoggedInContent = () => {
    const { path } = useRouteMatch();
    return (
        <Switch>
            <Route exact path={`${path}`} component={Lobby} />
            <Route path={`${path}game/:gameId`} component={GameWrapper} />
        </Switch>
    );
}

const Lobby = () => (
  <>
    <h2>Lobby</h2>
    <GamesList />
  </>
);

const PrivateLoggedInContent = PrivateRoute(LoggedInContent);
export default PrivateLoggedInContent;
