import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { getGame } from '../reducers';
import { requestGame } from '../actions';

const useGetGame = ({ gameId }) => {
  const dispatch = useDispatch();
  useEffect(() => {
      dispatch(requestGame(gameId));
  }, [dispatch, gameId]);
  return useSelector(state => getGame(state, gameId));
}

export default useGetGame;
