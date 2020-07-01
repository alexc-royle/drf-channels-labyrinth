import { useSelector } from 'react-redux';
import { getPlayer } from '../reducers';

const useGetPlayer = ({ playerId }) => {
  return useSelector(state => getPlayer(state, playerId));
}

export default useGetPlayer;
