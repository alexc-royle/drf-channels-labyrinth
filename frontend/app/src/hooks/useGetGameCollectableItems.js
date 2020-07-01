import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { getCollectableItemsByGame } from '../reducers';
import { requestGameCollectableItems } from '../actions';

const useGetGameCollectableItems = ({ gameId }) => {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(requestGameCollectableItems(gameId));
  }, [dispatch, gameId]);
  return useSelector(state => getCollectableItemsByGame(state, gameId));
}

export default useGetGameCollectableItems;
