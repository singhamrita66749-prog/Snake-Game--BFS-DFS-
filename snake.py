import turtle
import time
import random
from collections import deque

delay = 150
score = 0
high_score = 0
segments = []
mode = "BFS"   

wn = turtle.Screen()
wn.title("Snake Game AI (BFS & DFS)")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0)

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

def update_score():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}  Mode: {mode}",
              align="center", font=("Courier", 16, "normal"))

update_score()

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def set_bfs():
    global mode
    mode = "BFS"
    update_score()

def set_dfs():
    global mode
    mode = "DFS"
    update_score()

def set_manual():
    global mode
    mode = "MANUAL"
    update_score()

wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

wn.onkeypress(set_bfs, "b")
wn.onkeypress(set_dfs, "d")
wn.onkeypress(set_manual, "m")

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

def bfs(start, goal):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == goal:
            return path

        for dx, dy, direction in [(20,0,"right"), (-20,0,"left"),
                                 (0,20,"up"), (0,-20,"down")]:
            nx, ny = x+dx, y+dy

            if -300 < nx < 300 and -300 < ny < 300:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [direction]))
    return []

def dfs(start, goal):
    stack = [(start, [])]
    visited = set()

    while stack:
        (x, y), path = stack.pop()

        if (x, y) == goal:
            return path

        for dx, dy, direction in [(20,0,"right"), (-20,0,"left"),
                                 (0,20,"up"), (0,-20,"down")]:
            nx, ny = x+dx, y+dy

            if -300 < nx < 300 and -300 < ny < 300:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append(((nx, ny), path + [direction]))
    return []

def game_loop():
    global score, high_score

    wn.update()

    if mode in ["BFS", "DFS"]:
        start = (round(head.xcor()/20)*20, round(head.ycor()/20)*20)
        goal = (round(food.xcor()/20)*20, round(food.ycor()/20)*20)

        if mode == "BFS":
            path = bfs(start, goal)
        else:
            path = dfs(start, goal)

        if path:
            head.direction = path[0]

    if (head.xcor() > 290 or head.xcor() < -290 or
        head.ycor() > 290 or head.ycor() < -290):

        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        for seg in segments:
            seg.goto(1000, 1000)

        segments.clear()
        score = 0
        update_score()

    if head.distance(food) < 20:
        food.goto(random.randint(-280,280), random.randint(-280,280))

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        score += 10
        if score > high_score:
            high_score = score

        update_score()

    for i in range(len(segments)-1, 0, -1):
        segments[i].goto(segments[i-1].pos())

    if segments:
        segments[0].goto(head.pos())

    move()

    wn.ontimer(game_loop, delay)

game_loop()
wn.mainloop()