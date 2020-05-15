import { schema } from 'normalizr';

export const gameSchema = new schema.Entity('game');
export const gamesPaginationSchema = new schema.Entity('gamesPagination', {
  results: [gameSchema]
});
export const gamePieceSchema = new schema.Entity('gamePiece');
export const playerSchema = new schema.Entity('player');
export const collectableItemSchema = new schema.Entity('collectableItem');

export const shapeSchema = new schema.Entity('shape');
export const shapePaginationSchema = new schema.Entity('shapePagination', {
    results: [shapeSchema]
});

export const orientationSchema = new schema.Entity('orientation');
export const orientationPaginationSchema = new schema.Entity('orientationPagination', {
    results: [orientationSchema]
});
