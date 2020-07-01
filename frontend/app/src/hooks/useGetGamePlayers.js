import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { getPlayersByGame } from '../reducers';
import { requestGamePlayers } from '../actions';

const useGetGamePlayers = ({ gameId }) => {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(requestGamePlayers(gameId));
  }, [dispatch, gameId]);
  return useSelector(state => getPlayersByGame(state, gameId));
}

export default useGetGamePlayers;
