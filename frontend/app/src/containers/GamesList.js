import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { connect } from 'react-redux';
import * as actions from '../actions';
import { getAllGames, getCurrentPagination } from '../reducers';

class GamesList extends Component {
  componentDidMount() {
    const { getGamesList } = this.props;
    getGamesList();
  }

  render() {
    const { games, pagination, match } = this.props;
    if (pagination.results) {
        const gamesList =  pagination.results.map((item, key) => {
            const currentGame = games[item];
            if (currentGame) {
                return (<li><Link to={`${match.path}game/${currentGame.id}`}>{currentGame.id}</Link></li>);
            }
            return null;
        })
        return (
          <div className="games-list">{gamesList}</div>
        );
    }
    return null;
  }
}

const mapStateToProps = (state, props) => {
  return {
    games: getAllGames(state),
    pagination: getCurrentPagination(state)
  }
}

const ConnectedGamesList = connect(
  mapStateToProps,
  actions
)(GamesList);

export default withRouter(ConnectedGamesList);
