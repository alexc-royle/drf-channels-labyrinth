import React from 'react';
import { Switch, Route, useRouteMatch } from 'react-router-dom';
import PrivateRoute from '../hoc/PrivateRoute';


const LoggedInContent = () => {
    const { path } = useRouteMatch();
    return (
        <Switch>
            <Route exact path={`${path}`} component={Lobby} />
            <Route path={`${path}game`} component={Game} />
        </Switch>
    );
}

const Lobby = () => <h2>Lobby</h2>;
const Game = () => <h2>Game</h2>;

const PrivateLoggedInContent = PrivateRoute(LoggedInContent);
export default PrivateLoggedInContent;
