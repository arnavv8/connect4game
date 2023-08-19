import pygame
import sys

# Constants
WIDTH, HEIGHT = 640, 480
ROWS, COLS = 6, 7
CELL_SIZE = 80
RADIUS = int(CELL_SIZE / 2 - 5)
GRID_OFFSET = 20  # Offset for the grid to center it
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
BOARD_COLOR = (0, 0, 255)  # Blue
LINE_COLOR = (0, 0, 0)  # Black
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

# Load Algerian font
pygame.font.init()
algerian_font = pygame.font.Font("Algerian.ttf", 40)

def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(screen, board):
    # Draw the board grid
    pygame.draw.rect(screen, BOARD_COLOR, (GRID_OFFSET, GRID_OFFSET, GRID_WIDTH, GRID_HEIGHT))
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.circle(screen, LINE_COLOR,
                               (GRID_OFFSET + (col + 0.5) * CELL_SIZE, GRID_OFFSET + (row + 0.5) * CELL_SIZE),
                               RADIUS)

    # Draw the tokens
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == PLAYER1:
                pygame.draw.circle(screen, RED,
                                   (GRID_OFFSET + (col + 0.5) * CELL_SIZE, GRID_OFFSET + (row + 0.5) * CELL_SIZE),
                                   RADIUS)
            elif board[row][col] == PLAYER2:
                pygame.draw.circle(screen, YELLOW,
                                   (GRID_OFFSET + (col + 0.5) * CELL_SIZE, GRID_OFFSET + (row + 0.5) * CELL_SIZE),
                                   RADIUS)

    pygame.display.update()

def is_valid_move(board, col):
    return board[0][col] == EMPTY

def drop_token(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return True
    return False

def check_winner(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def is_board_full(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == EMPTY:
                return False
    return True

def show_welcome_screen(screen):
    # Yellow background
    screen.fill(YELLOW)

    # Black border
    pygame.draw.rect(screen, BLACK, (20, 20, WIDTH - 40, HEIGHT - 40), 5)

    text_welcome = algerian_font.render("WELCOME TO CONNECT 4", True, RED)
    text_click_play = algerian_font.render("Click to Play", True, BLACK)
    screen.blit(text_welcome, (WIDTH // 2 - text_welcome.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(text_click_play, (WIDTH // 2 - text_click_play.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

def show_game_end_screen(screen, winner):
    # Yellow background
    screen.fill(YELLOW)

    # Black border
    pygame.draw.rect(screen, RED, (20, 20, WIDTH - 40, HEIGHT - 40), 5)

    text_congrats = algerian_font.render(f"{winner} wins!", True, RED)
    text_play_again = algerian_font.render("Click to play Again", True, BLACK)
    screen.blit(text_congrats, (WIDTH // 2 - text_congrats.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(text_play_again, (WIDTH // 2 - text_play_again.get_width() // 2, HEIGHT // 2 + 70))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HEIGHT // 2 + 10 <= event.pos[1] <= HEIGHT // 2 + 10 + algerian_font.get_height():
                    return False  # Go back to welcome screen
                elif HEIGHT // 2 + 70 <= event.pos[1] <= HEIGHT // 2 + 70 + algerian_font.get_height():
                    return True  # Play again

def reset_game():
    board = create_board()
    turn = PLAYER1
    return board, turn


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect Four")
    clock = pygame.time.Clock()

    while True:
        show_welcome_screen(screen)

        while True:
            board, turn = reset_game()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        col = (event.pos[0] - GRID_OFFSET) // CELL_SIZE
                        if 0 <= col < COLS and is_valid_move(board, col):
                            if drop_token(board, col, turn):
                                draw_board(screen, board)
                                if check_winner(board, turn):
                                    draw_board(screen, board)
                                    winner = "Player 1" if turn == PLAYER1 else "Player 2"
                                    play_again = show_game_end_screen(screen, winner)
                                    if play_again:
                                        board, turn = reset_game()  # Reset board and turn variables
                                        break  # Restart the game
                                    else:
                                        break  # Go back to the main welcome screen
                                elif is_board_full(board):
                                    draw_board(screen, board)
                                    show_game_end_screen(screen, "No one")
                                    pygame.time.wait(1000)  # Wait for 1 second
                                    board, turn = reset_game()  # Reset board and turn variables
                                    break  # Go back to the main welcome screen
                                turn = PLAYER2 if turn == PLAYER1 else PLAYER1

                screen.fill(BLACK)
                draw_board(screen, board)

                pygame.display.update()
                clock.tick(60)

if __name__ == "__main__":
    main()
