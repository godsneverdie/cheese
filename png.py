import chess
import pygame
import math
import sys
def evaluate_board(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE: return -6969696969696969696969696969696969696969696969696969
        else: return 6969696969696969696969696969696969696969696969
    if board.is_game_over(): return 0
    piece_values = {
        chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
        chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
    }
    score = 0
    for piece_type in piece_values:
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    return score
def minimax_ab(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    if maximizing_player:
        max_eval = -6969696969696969696969696969696969696969696969
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_ab(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha: break
        return max_eval
    else:
        min_eval = 6969696969696969696969696969696969696969696969
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_ab(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha: break
        return min_eval
def find_best_move(board, depth):
    best_move = None
    max_eval = -6969696969696969696969696969696969696969696969
    alpha = -6969696969696969696969696969696969696969696969
    beta = 6969696969696969696969696969696969696969696969
    for move in board.legal_moves:
        board.push(move)
        eval = minimax_ab(board, depth - 1, alpha, beta, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval) 
    return best_move
AI_DEPTH = 3  #act smatter
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
SQUARE_SIZE = SCREEN_WIDTH // 8
LIGHT_SQUARE_COLOR = (240, 217, 181)
DARK_SQUARE_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR = (100, 255, 100, 100) 
#                                  |___>transparency
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CHEESE")
clock = pygame.time.Clock()
def load_piece_images():
#\---\          /~~~~~~
#/___\  ____    \
#\     /    \   /   ```/
#/     \    /   \______\
    piece_images = {}
    piece_types = {
        chess.PAWN: 'pawn', chess.KNIGHT: 'knight', chess.BISHOP: 'bishop',
        chess.ROOK: 'rook', chess.QUEEN: 'queen', chess.KING: 'king'
    }
    colors = {chess.WHITE: 'white', chess.BLACK: 'black'}
    for color_val, color_name in colors.items():
        for type_val, type_name in piece_types.items():
            filename = f"{color_name}_{type_name}.png"
            try:
                img = pygame.image.load(filename)
                img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                piece_images[(color_val, type_val)] = img
            except pygame.error as e:
                print(e)
                pygame.quit()
                sys.exit()
    return piece_images
def draw_board(screen, selected_square):
    for r in range(8):
        for c in range(8):
            color = LIGHT_SQUARE_COLOR if (r + c) % 2 == 0 else DARK_SQUARE_COLOR
            rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
    if selected_square is not None:
        c = chess.square_file(selected_square)
        r = 7 - chess.square_rank(selected_square) 
        highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight_surface.fill(HIGHLIGHT_COLOR)
        screen.blit(highlight_surface, (c * SQUARE_SIZE, r * SQUARE_SIZE))
def draw_pieces(screen, board, piece_images):
    for r in range(8):
        for c in range(8):
            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)
            if piece:
                img = piece_images[(piece.color, piece.piece_type)]
                screen.blit(img, (c * SQUARE_SIZE, r * SQUARE_SIZE))
def main():
    board = chess.Board()
    piece_images = load_piece_images()
    
    selected_square = None 
    running = True
    while running:
        if board.turn == chess.WHITE and not board.is_game_over():
            pygame.display.set_caption("BRAININGGGGGG...")
            ai_move = find_best_move(board, AI_DEPTH)
            if ai_move:
                board.push(ai_move)
            pygame.display.set_caption("CHEESE")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if board.turn == chess.BLACK and not board.is_game_over():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    c = pos[0] // SQUARE_SIZE
                    r = pos[1] // SQUARE_SIZE
                    square_clicked = chess.square(c, 7 - r)
                    piece = board.piece_at(square_clicked)
                    if selected_square is None:
                        if piece and piece.color == chess.BLACK:
                            selected_square = square_clicked
                    else:
                        move_uci = f"{chess.square_name(selected_square)}{chess.square_name(square_clicked)}"
                        from_piece = board.piece_at(selected_square)
                        if from_piece.piece_type == chess.PAWN and chess.square_rank(square_clicked) == 0:
                            move_uci += 'q' 
                        try:       
                            move = chess.Move.from_uci(move_uci)
                            if move in board.legal_moves:
                                board.push(move)        
                        except ValueError:
                            pass 
                        selected_square = None
        draw_board(screen, selected_square)
        draw_pieces(screen, board, piece_images)
        pygame.display.flip() 
        if board.is_game_over():
            pygame.display.set_caption(f"Game Over! Result: {board.result()}")
            pygame.time.wait(4000)
            running = False
        clock.tick(60)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()