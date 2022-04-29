import random


def message(st, c, sn, p):
    if len(sn) > 6:
        print('=' * 70, '\nStock size:', len(st), '\nComputer pieces:', len(c), '\n\n', *sn[:3], '...', *sn[-3:], '\n\nYour pieces:')
    else:
        print('=' * 70, '\nStock size:', len(st), '\nComputer pieces:', len(c), '\n\n', *sn, '\n\nYour pieces:')
    for t in range(len(p)):
        print('{}:{}'.format(t + 1, p[t]))


def winner(c, sn, p):
    if len(p) == 0:
        print('\nStatus: The game is over. You won!')
        return True
    if len(c) == 0:
        print('\nStatus: The game is over. The computer won!')
        return True
    if sn[0][0] == sn[-1][1] and sum(x.count(sn[0][0]) for x in sn) == 8:
        print('\nStatus: The game is over. It\'s a draw!')
        return True


while True:
    stock = [[x, y] for x in range(0, 7) for y in range(x, 7)]
    computer, player, snake = [list() for _ in range(0, 3)]
    for _ in range(0, 7):
        n = random.randrange(0, len(stock), 1)
        computer.append(stock[n])
        stock.remove(stock[n])
        m = random.randrange(0, len(stock), 1)
        player.append(stock[m])
        stock.remove(stock[m])
    for i in range(6, -1, -1):
        if [i, i] in player:
            snake.append([i, i])
            player.remove([i, i])
            next_move = 'computer'
            break
        if [i, i] in computer:
            snake.append([i, i])
            computer.remove([i, i])
            next_move = 'player'
            break
    if next_move:
        break
message(stock, computer, snake, player)

while True:
    if winner(computer, snake, player):
        break
    if next_move == 'player':
        while True:
            move = input('\nStatus: It\'s your turn to make a move. Enter your command.\n')
            if move.lstrip('-').isdigit() and abs(int(move)) <= len(player):
                move = int(move)
            else:
                while True:
                    move = input('Invalid input. Please try again.\n')
                    if move.lstrip('-').isdigit() and abs(int(move)) <= len(player):
                        move = int(move)
                        break
            if move == 0:
                n = random.randrange(0, len(stock), 1)
                player.append(stock[n])
                stock.remove(stock[n])
                break
            if move > 0 and snake[-1][1] == player[move - 1][0]:
                snake.append(player[move - 1])
                player.remove(player[abs(move) - 1])
                break
            elif move > 0 and snake[-1][1] == player[move - 1][1]:
                snake.append([player[move - 1][1], player[move - 1][0]])
                player.remove(player[abs(move) - 1])
                break
            elif move < 0 and snake[0][0] == player[abs(move) - 1][1]:
                snake.insert(0, player[abs(move) - 1])
                player.remove(player[abs(move) - 1])
                break
            elif move < 0 and snake[0][0] == player[abs(move) - 1][0]:
                snake.insert(0, [player[abs(move) - 1][1], player[abs(move) - 1][0]])
                player.remove(player[abs(move) - 1])
                break
            else:
                while True:
                    move = input('Illegal move. Please try again.\n')
                    if move.lstrip('-').isdigit() and abs(int(move)) <= len(player):
                        move = int(move)
                    if move == 0:
                        n = random.randrange(0, len(stock), 1)
                        player.append(stock[n])
                        stock.remove(stock[n])
                        break
                    elif move > 0 and snake[-1][1] == player[move - 1][0]:
                        snake.append(player[move - 1])
                        player.remove(player[abs(move) - 1])
                        break
                    elif move > 0 and snake[-1][1] == player[move - 1][1]:
                        snake.append([player[move - 1][1], player[move - 1][0]])
                        player.remove(player[abs(move) - 1])
                        break
                    elif move < 0 and snake[0][0] == player[abs(move) - 1][1]:
                        snake.insert(0, player[abs(move) - 1])
                        player.remove(player[abs(move) - 1])
                        break
                    elif move < 0 and snake[0][0] == player[abs(move) - 1][0]:
                        snake.insert(0, [player[abs(move) - 1][1], player[abs(move) - 1][0]])
                        player.remove(player[abs(move) - 1])
                        break
                break
        next_move = 'computer'
    else:
        choices = []
        move = input('\nStatus: Computer is about to make a move. Press Enter to continue...\n')
        for x in range(len(computer)):
            if snake[-1][1] == computer[x][0] or snake[-1][1] == computer[x][1]:
                choices.append(x + 1)
            elif snake[0][0] == computer[x][0] or snake[0][0] == computer[x][1]:
                choices.append(-(x + 1))
        if len(choices) > 0:
            move = random.choice(choices)
            if move > 0 and snake[-1][1] == computer[move - 1][0]:
                snake.append(computer[move - 1])
                computer.remove(computer[abs(move) - 1])
            elif move > 0 and snake[-1][1] == computer[move - 1][1]:
                snake.append([computer[move - 1][1], computer[move - 1][0]])
                computer.remove(computer[abs(move) - 1])
            elif move < 0 and snake[0][0] == computer[abs(move) - 1][1]:
                snake.insert(0, computer[abs(move) - 1])
                computer.remove(computer[abs(move) - 1])
            elif move < 0 and snake[0][0] == computer[abs(move) - 1][0]:
                snake.insert(0, [computer[abs(move) - 1][1], computer[abs(move) - 1][0]])
                computer.remove(computer[abs(move) - 1])
        next_move = 'player'
    message(stock, computer, snake, player)
