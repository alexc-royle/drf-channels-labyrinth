import { useSelector } from 'react-redux';
import { getGamePiece } from '../reducers';

const useGetGamePiece = ({ gamePieceId }) => {
  return useSelector(state => getGamePiece(state, gamePieceId));
}

export default useGetGamePiece;
