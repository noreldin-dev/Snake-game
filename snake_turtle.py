import turtle
import time
import random

# Screen setup
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake body segments
segments = []

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Score
score = 0
high_score = 0

# Score display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

# --- Feature: Pause/Resume ---
paused = False

def toggle_pause():
    global paused
    paused = not paused

wn.onkey(toggle_pause, "p")

# --- Feature: Restart ---
def restart():
    global score, segments, paused
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    score = 0
    score_display.clear()
    score_display.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))
    paused = False

wn.onkey(restart, "r")

# --- Feature: Game Over Message ---
game_over_display = turtle.Turtle()
game_over_display.hideturtle()
game_over_display.color("yellow")
game_over_display.penup()
game_over_display.goto(0, 0)

def show_game_over():
    game_over_display.clear()
    game_over_display.write("GAME OVER! Press 'r' to restart", align="center", font=("Courier", 24, "bold"))

def hide_game_over():
    game_over_display.clear()

# Functions

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

def move():
    x, y = head.xcor(), head.ycor()
    if head.direction == "up":
        y += 20
    elif head.direction == "down":
        y -= 20
    elif head.direction == "left":
        x -= 20
    elif head.direction == "right":
        x += 20
    # Edge infinity logic
    if x > 290:
        x = -290
    elif x < -290:
        x = 290
    if y > 290:
        y = -290
    elif y < -290:
        y = 290
    head.goto(x, y)

# Keyboard bindings
wn.listen()
wn.onkey(go_up, "Up")
wn.onkey(go_down, "Down")
wn.onkey(go_left, "Left")
wn.onkey(go_right, "Right")

# --- Main game loop with features ---
speed = 0.1
while True:
    wn.update()
    if paused:
        time.sleep(0.1)
        continue

    # Remove border collision reset (edge infinity is active)

    # Check for collision with food
    if head.distance(food) < 20:
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        food.goto(x, y)
        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("lightgreen")
        new_segment.penup()
        segments.append(new_segment)
        score += 10
        # --- Feature: Speed Increase ---
        if speed > 0.04:
            speed -= 0.005
        # --- Feature: Scoreboard Color Change ---
        if score > high_score:
            high_score = score
            score_display.color("cyan")
        else:
            score_display.color("white")
        score_display.clear()
        score_display.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Move the end segments first in reverse order
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x, y)
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Check for collision with body
    for segment in segments:
        if segment.distance(head) < 20:
            show_game_over()
            time.sleep(1)
            paused = True
            restart()  # Optionally auto-restart, or comment this line to require 'r'
            hide_game_over()
            break

    time.sleep(speed)

wn.mainloop()
