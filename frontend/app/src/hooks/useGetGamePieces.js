import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { getGamePiecesByGame } from '../reducers';
import { requestGamePieces } from '../actions';

const useGetGamePieces = ({ gameId }) => {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(requestGamePieces(gameId));
  }, [dispatch, gameId]);
  return useSelector(state => getGamePiecesByGame(state, gameId));
}

export default useGetGamePieces;
