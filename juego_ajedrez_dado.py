import pygame
import random
from enum import Enum

# Inicializar Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
UI_HEIGHT = 100
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GREY = (128, 128, 128)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
GREEN = (34, 177, 76)
YELLOW = (255, 255, 0)
GOLD = (255, 223, 0)

# Cargar imágenes de piezas
IMAGES = {
    "white_soldier": pygame.image.load("assets/soldier_white.svg"),
    "black_soldier": pygame.image.load("assets/soldier_black.svg"),
    "white_king": pygame.image.load("assets/king_white.svg"),
    "black_king": pygame.image.load("assets/king_black.svg")
}

# Escalar imágenes al tamaño de casilla
for key in IMAGES:
    IMAGES[key] = pygame.transform.scale(IMAGES[key], (SQUARE_SIZE, SQUARE_SIZE))

# Ventana
WIN = pygame.display.set_mode((WIDTH, HEIGHT + UI_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Juego de Ajedrez con Dado")

# Fuente
FONT = pygame.font.SysFont("arial", 18)
BIG_FONT = pygame.font.SysFont("arial", 36)

class MoveType(Enum):
    PEON = "peon"
    TORRE = "torre"
    ALFIL = "alfil"
    CABALLO = "caballo"
    REINA = "reina"
    NONE = "none"
    
# Cargar íconos visuales para el dado según color
DICE_ICONS = {
    "white": {
        MoveType.PEON: pygame.image.load("assets/peon_blanco.svg"),
        MoveType.TORRE: pygame.image.load("assets/torre_blanco.svg"),
        MoveType.CABALLO: pygame.image.load("assets/caballo_blanco.svg"),
        MoveType.ALFIL: pygame.image.load("assets/alfil_blanco.svg"),
        MoveType.REINA: pygame.image.load("assets/reina_blanco.svg"),
    },
    "black": {
        MoveType.PEON: pygame.image.load("assets/peon_negro.svg"),
        MoveType.TORRE: pygame.image.load("assets/torre_negro.svg"),
        MoveType.CABALLO: pygame.image.load("assets/caballo_negro.svg"),
        MoveType.ALFIL: pygame.image.load("assets/alfil_negro.svg"),
        MoveType.REINA: pygame.image.load("assets/reina_negro.svg"),
    }
}

# Escalar todos los íconos a 40x40
for color_dict in DICE_ICONS.values():
    for key in color_dict:
        color_dict[key] = pygame.transform.scale(color_dict[key], (40, 40))

class Piece:
    def __init__(self, row, col, color, is_king=False):
        self.row = row
        self.col = col
        self.color = color
        self.is_king = is_king

    def draw(self, win):
        key = f"{self.color}_{'king' if self.is_king else 'soldier'}"
        image = IMAGES[key]
        win.blit(image, (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE))

    def move(self, row, col):
        self.row = row
        self.col = col

class Dice:
    faces = [MoveType.PEON, MoveType.PEON, MoveType.TORRE, MoveType.CABALLO, MoveType.ALFIL, MoveType.REINA]

    def roll(self):
        return random.choice(self.faces)

def create_initial_board():
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]

    # Blancas (fila 6 y 7)
    for col in range(COLS):
        board[6][col] = Piece(6, col, "white")
        board[7][col] = Piece(7, col, "white")
    board[7][4] = Piece(7, 4, "white", is_king=True)

    # Negras (fila 0 y 1)
    for col in range(COLS):
        board[0][col] = Piece(0, col, "black")
        board[1][col] = Piece(1, col, "black")
    board[0][4] = Piece(0, 4, "black", is_king=True)

    return board

def get_valid_moves(piece, board, move_type):
    directions = []
    moves = []

    if piece.is_king:
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dr, dc in directions:
            r, c = piece.row + dr, piece.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if not board[r][c] or board[r][c].color != piece.color:
                    moves.append((r, c))
        return moves

    if move_type == MoveType.PEON:
        dir = -1 if piece.color == "white" else 1
        front = piece.row + dir
        if 0 <= front < ROWS and board[front][piece.col] is None:
            moves.append((front, piece.col))
        for dc in [-1, 1]:
            c = piece.col + dc
            if 0 <= c < COLS and 0 <= front < ROWS:
                if board[front][c] and board[front][c].color != piece.color:
                    moves.append((front, c))
        return moves

    if move_type == MoveType.CABALLO:
        jumps = [(-2, -1), (-1, -2), (-2, 1), (-1, 2),
                 (2, -1), (1, -2), (2, 1), (1, 2)]
        for dr, dc in jumps:
            r, c = piece.row + dr, piece.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if not board[r][c] or board[r][c].color != piece.color:
                    moves.append((r, c))
        return moves

    if move_type == MoveType.TORRE:
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
    elif move_type == MoveType.ALFIL:
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
    elif move_type == MoveType.REINA:
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]

    for dr, dc in directions:
        r, c = piece.row + dr, piece.col + dc
        while 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] is None:
                moves.append((r, c))
            elif board[r][c].color != piece.color:
                moves.append((r, c))
                break
            else:
                break
            r += dr
            c += dc
    return moves

def draw_ui(win, dice_result, current_turn, game_over, winner, has_rolled):
    pygame.draw.rect(win, BLACK, (0, HEIGHT, WIDTH, UI_HEIGHT))

    if game_over:
        win_text = BIG_FONT.render(f"¡{winner.upper()} gana!", True, GOLD)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT + UI_HEIGHT // 2 - 20))
        win.blit(win_text, win_rect)
        restart_text = FONT.render("Haz clic aquí para reiniciar", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT + UI_HEIGHT // 2 + 20))
        win.blit(restart_text, restart_rect)
        pygame.draw.rect(win, YELLOW, restart_rect.inflate(20, 10), 2)
        return restart_rect.inflate(20, 10), None

    # Texto del turno y dado
    turn_text = FONT.render(f"Turno: {'Blancas' if current_turn == 'white' else 'Negras'}", True, WHITE)
    win.blit(turn_text, (10, HEIGHT + 10))

    if dice_result:
        dice_text = FONT.render(f"Dado: {dice_result.name.capitalize()}", True, WHITE)
        win.blit(dice_text, (10, HEIGHT + 40))
        icon = DICE_ICONS[current_turn][dice_result]
        win.blit(icon, (150, HEIGHT + 35))
    else:
        dice_text = FONT.render("Dado: ---", True, WHITE)
        win.blit(dice_text, (10, HEIGHT + 40))

    # Botón reiniciar
    restart_rect = pygame.Rect(WIDTH - 100, HEIGHT + 20, 80, 30)
    pygame.draw.rect(win, GREY, restart_rect)
    pygame.draw.rect(win, WHITE, restart_rect, 2)
    win.blit(FONT.render("Reiniciar", True, WHITE), (WIDTH - 90, HEIGHT + 27))

    # Botón lanzar dado
    dice_rect = pygame.Rect(WIDTH - 200, HEIGHT + 20, 80, 30)
    pygame.draw.rect(win, GREEN if not has_rolled else GREY, dice_rect)
    pygame.draw.rect(win, WHITE, dice_rect, 2)
    win.blit(FONT.render("Lanzar", True, WHITE), (WIDTH - 185, HEIGHT + 27))

    return restart_rect, dice_rect

def draw_board(win, board, selected_piece, valid_moves):
    # Dibujar fondo del tablero
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Dibujar primero las fichas enemigas sobre casillas marcadas como captura
    if selected_piece:
        for move in valid_moves:
            r, c = move
            if board[r][c] and board[r][c].color != selected_piece.color:
                # Dibujar marco rojo sobre ficha capturable
                pygame.draw.rect(win, RED, (c * SQUARE_SIZE + 4, r * SQUARE_SIZE + 4, SQUARE_SIZE - 8, SQUARE_SIZE - 8), 4)

    # Dibujar todas las piezas normalmente
    for row in board:
        for piece in row:
            if piece:
                piece.draw(win)

    # Resaltado de selección y movimientos válidos
    if selected_piece:
        # Casilla de pieza seleccionada
        pygame.draw.rect(win, YELLOW, (selected_piece.col*SQUARE_SIZE, selected_piece.row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
        for move in valid_moves:
            r, c = move
            if not board[r][c]:
                # Casilla vacía: círculo amarillo
                pygame.draw.circle(win, YELLOW, (c*SQUARE_SIZE + SQUARE_SIZE//2, r*SQUARE_SIZE + SQUARE_SIZE//2), 10)

def reset_game():
    return {
        "board": create_initial_board(),
        "dice": Dice(),
        "dice_result": None,
        "current_turn": "white",
        "selected_piece": None,
        "valid_moves": [],
        "has_rolled": False,
        "game_over": False,
        "winner": None
    }

def run_game():
    clock = pygame.time.Clock()
    state = reset_game()

    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(BLACK)
        draw_board(WIN, state["board"], state["selected_piece"], state["valid_moves"])
        restart_button, dice_button = draw_ui(WIN, state["dice_result"], state["current_turn"], state["game_over"], state["winner"], state["has_rolled"])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Pantalla de victoria
            if state["game_over"]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(pygame.mouse.get_pos()):
                        state = reset_game()
                continue

            # Click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Botón reiniciar
                if restart_button.collidepoint((mx, my)):
                    state = reset_game()
                    continue

                # Botón lanzar dado
                if dice_button and dice_button.collidepoint((mx, my)) and not state["has_rolled"]:
                    state["dice_result"] = state["dice"].roll()
                    state["has_rolled"] = True
                    state["selected_piece"] = None
                    state["valid_moves"] = []
                    continue

                # Clic sobre el tablero
                if my >= HEIGHT:
                    continue
                row, col = my // SQUARE_SIZE, mx // SQUARE_SIZE
                piece = state["board"][row][col]

                if state["selected_piece"] and (row, col) in state["valid_moves"]:
                    dest = state["board"][row][col]
                    if dest and dest.is_king:
                        state["game_over"] = True
                        state["winner"] = state["selected_piece"].color
                    state["board"][state["selected_piece"].row][state["selected_piece"].col] = None
                    state["selected_piece"].move(row, col)
                    state["board"][row][col] = state["selected_piece"]
                    state["selected_piece"] = None
                    state["valid_moves"] = []
                    state["has_rolled"] = False
                    state["dice_result"] = None
                    state["current_turn"] = "black" if state["current_turn"] == "white" else "white"

                elif piece and piece.color == state["current_turn"]:
                    if piece.is_king or (state["dice_result"] and not piece.is_king):
                        state["selected_piece"] = piece
                        move_type = MoveType.NONE if piece.is_king else state["dice_result"]
                        state["valid_moves"] = get_valid_moves(piece, state["board"], move_type)
                    else:
                        state["selected_piece"] = None
                        state["valid_moves"] = []

    pygame.quit()

if __name__ == "__main__":
    run_game()

