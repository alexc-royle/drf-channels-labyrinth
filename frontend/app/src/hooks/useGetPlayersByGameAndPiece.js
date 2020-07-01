import { useSelector } from 'react-redux';
import { getPlayersByGameAndPiece } from '../reducers';

const useGetPlayersByGameAndPiece = ({ gameId, gamePieceId }) => {
  return useSelector(state => getPlayersByGameAndPiece(state, gameId, gamePieceId));
}

export default useGetPlayersByGameAndPiece;
