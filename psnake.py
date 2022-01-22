import curses, random, time

COLLISION_CODE = "collision"

SNAKE_BODY = "#"
HORIZONTAL_BORDER = "█"
VERTICAL_BORDER = "█"
FOOD = "■"
PADDING = 0

score = 0


def game_over(scr: curses.window):
    height, width = scr.getmaxyx()
    scr.timeout(-1)
    scr.insstr(
        0,
        0,
        "  GAME OVER  | Score: " + str(score) + (" " * width),
        curses.color_pair(2),
    )
    scr.refresh()
    while True:
        time.sleep(9999999)


def pause_game(scr: curses.window):
    scr.timeout(-1)
    height, width = scr.getmaxyx()
    scr.move(height - 1, 0)
    scr.deleteln()
    scr.insstr(
        height - 1, 0, " PAUSED | Continue(p)" + (" " * width), curses.color_pair(2)
    )
    inp = scr.getch()

    scr.timeout(0)


def snake(scr: curses.window):

    curses.use_default_colors()
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.curs_set(0)
    curses.noecho()
    scr.timeout(0)

    height, width = scr.getmaxyx()
    body = [[5, 5]]  # x and y position of snake's body, 1st element is head
    direction = "right"
    food = [10, 10]  # food's x and y position
    global score

    while True:
        scr.clear()

        ## draw borders
        scr.addstr(0, 0, HORIZONTAL_BORDER * width)
        scr.insstr(height - 1, 0, HORIZONTAL_BORDER * width)
        for y_index in range(height):
            scr.insstr(y_index, 0, VERTICAL_BORDER)
            scr.insstr(y_index, width - 1, VERTICAL_BORDER)

        ## score text
        score_text = " Score: " + str(score)
        scr.insstr(0, 0, score_text, curses.color_pair(2))

        ## bottom quit text
        scr.insstr(height - 1, 0, "(Ctrl+c to quit)", curses.color_pair(2))

        ## get input
        inp = scr.getch()
        if inp == curses.KEY_RIGHT and not direction == "left":
            direction = "right"
        elif inp == curses.KEY_LEFT and not direction == "right":
            direction = "left"
        elif inp == curses.KEY_UP and not direction == "down":
            direction = "up"
        elif inp == curses.KEY_DOWN and not direction == "up":
            direction = "down"

        ## update body parts' position (move)
        for body_index in range(len(body) - 1, 0, -1):
            body[body_index] = body[body_index - 1][:]

        ## move head
        if direction == "right":
            body[0][0] += 1
        elif direction == "left":
            body[0][0] -= 1
        elif direction == "up":
            body[0][1] -= 1
        elif direction == "down":
            body[0][1] += 1

        ## draw snake
        for x, y in body:
            scr.delch(y, x)
            scr.insstr(y, x, SNAKE_BODY)

        ## check collisions
        # it's body
        if body[0] in body[1:]:
            game_over(scr)
        # borders
        if body[0][0] in [0, width - 1] or body[0][1] in [0, height - 1]:
            game_over(scr)
        # food
        elif body[0] == food:
            score += 1
            body += [body[-1]]

            while food in body:
                food = [
                    random.randint(1 + PADDING, width - 2 - PADDING),
                    random.randint(1 + PADDING, height - 2 - PADDING),
                ]

        # draw food
        scr.delch(food[1], food[0])
        scr.insstr(food[1], food[0], FOOD, curses.color_pair(3))

        scr.refresh()

        if inp == ord("p"):
            pause_game(scr)

        time.sleep(0.1)


if __name__ == "__main__":
    try:
        code = curses.wrapper(snake)
    except KeyboardInterrupt:
        print("by")
