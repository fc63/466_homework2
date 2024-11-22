import pygame
import sys
import copy

pygame.init()
WIDTH, HEIGHT = 1800, 600
BOARD_SIZE = 3
SQUARE_SIZE = 45

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("202011204_466_Homework_2")

PIECES = {
    'N': pygame.image.load("white_knight.png"),
    'R': pygame.image.load("white_rook.png"),
    'b': pygame.image.load("black_bishop.png"),
    'p': pygame.image.load("black_pawn.png"),
    'n': pygame.image.load("black_knight.png")
}

for key in PIECES:
    PIECES[key] = pygame.transform.scale(PIECES[key], (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(x, y, board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            color = GRAY if (row + col) % 2 == 0 else WHITE
            rect = pygame.Rect(x + col * SQUARE_SIZE, y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            piece = board[row][col]
            if piece in PIECES:
                screen.blit(PIECES[piece], rect.topleft)

def create_initial_board():
    return [
        ['.', 'p', '.'],
        ['b', '.', '.'],
        ['N', 'n', 'R']
    ]

def get_possible_moves(board, player):
    moves = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row][col]
            if player == "white" and piece == 'N':

                knight_moves = [(-2, -1), (-1, -2), (-2, 1), (-1, 2), (2, -1), (1, -2), (2, 1), (1, 2)]
                for dr, dc in knight_moves:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                        new_board = copy.deepcopy(board)
                        new_board[row][col], new_board[new_row][new_col] = '.', 'N'
                        moves.append(new_board)

            elif player == "black" and piece == 'n':

                knight_moves = [(-2, -1), (-1, -2), (-2, 1), (-1, 2), (2, -1), (1, -2), (2, 1), (1, 2)]
                for dr, dc in knight_moves:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                        new_board = copy.deepcopy(board)
                        new_board[row][col], new_board[new_row][new_col] = '.', 'n'
                        moves.append(new_board)

            elif player == "white" and piece == 'R':

                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_row, new_col = row, col
                    while True:
                        new_row += dr
                        new_col += dc
                        if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                            target = board[new_row][new_col]
                            if target == '.':
                                new_board = copy.deepcopy(board)
                                new_board[row][col], new_board[new_row][new_col] = '.', 'R'
                                moves.append(new_board)
                            elif target.islower():
                                new_board = copy.deepcopy(board)
                                new_board[row][col], new_board[new_row][new_col] = '.', 'R'
                                moves.append(new_board)
                                break
                            else:
                                break
                        else:
                            break
            elif player == "black" and piece == 'b':

                for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    new_row, new_col = row, col
                    while True:
                        new_row += dr
                        new_col += dc
                        if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                            target = board[new_row][new_col]
                            if target == '.':
                                new_board = copy.deepcopy(board)
                                new_board[row][col], new_board[new_row][new_col] = '.', 'b'
                                moves.append(new_board)
                            elif target.isupper():
                                new_board = copy.deepcopy(board)
                                new_board[row][col], new_board[new_row][new_col] = '.', 'b'
                                moves.append(new_board)
                                break
                            else:
                                break
                        else:
                            break
            elif player == "black" and piece == 'p':

                if row + 1 < BOARD_SIZE and board[row + 1][col] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[row][col], new_board[row + 1][col] = '.', 'p'
                    moves.append(new_board)

                if row + 1 < BOARD_SIZE and col + 1 < BOARD_SIZE and board[row + 1][col + 1].isupper():
                    new_board = copy.deepcopy(board)
                    new_board[row][col], new_board[row + 1][col + 1] = '.', 'p'
                    moves.append(new_board)

                if row + 1 < BOARD_SIZE and col - 1 >= 0 and board[row + 1][col - 1].isupper():
                    new_board = copy.deepcopy(board)
                    new_board[row][col], new_board[row + 1][col - 1] = '.', 'p'
                    moves.append(new_board)
    return moves

def create_game_tree(board, player, depth, parent=None, role="max"):
    if depth == 0:
        return {"board": board, "children": [], "parent": parent, "role": "terminal"}

    moves = get_possible_moves(board, player)
    children = []
    next_role = "min" if role == "max" else "max"
    node = {"board": board, "children": children, "parent": parent, "role": role}

    for move in moves:
        next_player = "black" if player == "white" else "white"
        child = create_game_tree(move, next_player, depth - 1, parent=node, role=next_role)
        children.append(child)
    return node

def evaluate_board(board, player):
    piece_values = {'p': -1, 'b': -3, 'n': -3, 'r': -5, 'q': -9, 'k': -100,
                    'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9, 'K': 100}
    positional_values = {
        'p': [[0, 0, 0], [1, 2, 1], [0, 1, 0]],
        'N': [[2, 3, 2], [3, 4, 3], [2, 3, 2]],
        'n': [[2, 3, 2], [3, 4, 3], [2, 3, 2]],
        'R': [[1, 2, 1], [2, 3, 2], [1, 2, 1]],
        'b': [[2, 3, 2], [3, 4, 3], [2, 3, 2]],
    }

    evaluation = 0
    mobility_bonus = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            cell = board[row][col]
            if cell in piece_values:
                evaluation += piece_values[cell]
            if cell in positional_values:
                evaluation += positional_values[cell][row][col]

    possible_moves = get_possible_moves(board, player)
    mobility_bonus += len(possible_moves) * 0.1  
    evaluation += mobility_bonus

    return evaluation

def minimax(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node["role"] == "terminal":
        node["value"] = evaluate_board(node["board"], "white" if maximizing_player else "black")
        node["is_pruned"] = False  
        return node["value"]

    if maximizing_player:
        max_eval = float('-inf')
        for child in node["children"]:
            eval = minimax(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                child["is_pruned"] = True  
                break
            else:
                child["is_pruned"] = False  
        node["value"] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for child in node["children"]:
            eval = minimax(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                child["is_pruned"] = True  
                break
            else:
                child["is_pruned"] = False  
        node["value"] = min_eval
        return min_eval

def draw_selected_tree(tree, x, y, offset=300):
    node_positions = []

    draw_board(x, y, tree["board"])
    font = pygame.font.Font(None, 24)

    role_text = font.render(tree["role"], True, BLACK)
    value_text = font.render(f"Value: {tree.get('value', '')}", True, BLACK)
    screen.blit(role_text, (x, y - 40))  
    screen.blit(value_text, (x, y - 20))  
    node_positions.append((x, y, tree))

    if tree["children"]:
        child_x_start = x - (len(tree["children"]) - 1) * offset // 2
        child_y = y + 200
        for child in tree["children"]:

            pygame.draw.line(
                screen, BLUE,
                (x + BOARD_SIZE * SQUARE_SIZE // 2, y + BOARD_SIZE * SQUARE_SIZE),
                (child_x_start + BOARD_SIZE * SQUARE_SIZE // 2, child_y),
                2
            )

            draw_board(child_x_start, child_y, child["board"])
            child_role_text = font.render(child["role"], True, BLACK)
            child_value_text = font.render(f"Value: {child.get('value', '')}", True, BLACK)

            if child.get("is_pruned"):
                prune_text = font.render("α >= β : true /other branches were pruned", True, BLACK)
                screen.blit(prune_text, (child_x_start, child_y + BOARD_SIZE * SQUARE_SIZE + 10))

            screen.blit(child_role_text, (child_x_start, child_y - 40))
            screen.blit(child_value_text, (child_x_start, child_y - 20))
            node_positions.append((child_x_start, child_y, child))
            child_x_start += offset

    return node_positions

def draw_back_button():
    button_rect = pygame.Rect(WIDTH - 150, 50, 100, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Geri", True, BLACK)
    screen.blit(text, (WIDTH - 140, 60))
    return button_rect

def game_loop():
    initial_board = create_initial_board()
    game_tree = create_game_tree(initial_board, "white", 4, role="max")
    minimax(game_tree, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
    selected_tree = game_tree

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    back_button = draw_back_button()
                    if back_button.collidepoint(mouse_x, mouse_y) and selected_tree["parent"] is not None:
                        selected_tree = selected_tree["parent"]
                    node_positions = draw_selected_tree(selected_tree, WIDTH // 2 - SQUARE_SIZE * BOARD_SIZE // 2, 50)
                    for x, y, tree in node_positions:
                        if x <= mouse_x <= x + BOARD_SIZE * SQUARE_SIZE and y <= mouse_y <= y + BOARD_SIZE * SQUARE_SIZE:
                            selected_tree = tree

        screen.fill(WHITE)
        draw_selected_tree(selected_tree, WIDTH // 2 - SQUARE_SIZE * BOARD_SIZE // 2, 50)
        draw_back_button()
        pygame.display.flip()

game_loop()
