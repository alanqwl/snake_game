import turtle
import time
import random

# These are global variables.
g_screen = None             # the largest screen of the game.
g_second_margin = None      # the upper status area.
g_third_margin = None       # the central motion area.
g_info1 = None              # This is a pen to write in the upper status area.
g_info2 = None              # This is a pen to write in the central motion area.
g_snake_head = None         # the snake's head.
g_monster = None            # the monster's head.
g_contact_number = 0        # the number of the monster cross the snake's body
g_start_time = None         # record the starting time of the game which will be used in the timer.
g_renew = True              # indicates whether the upper status area needs to update
g_body_id = []              # store the id of the snake's body which is consists of turtles in square shape
g_body_pos = []             # store the location of the snake's body
g_body_length = 5           # set the original length of the snake to be 5
g_state = 0                 # detect whether the snake starts to move or not at the beginning of the game
g_food_list = []            # store all the turtles which are used to represent food.
g_eat_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]        # indicates whether the food is eaten
g_x_numlist = []              # store all the possible x coordinates of the food
g_y_numlist = []              # store all the possible y coordinates of the food
# store data into the two lists
i = -280
while i <= 200:
    g_y_numlist.append(i)
    i += 20                 # to make the food better align at the snake's head.
k = -240
while k <= 240:
    g_x_numlist.append(k)
    k += 20

# Functions for configurations: screen settings, click setting and key settings.
def draw_g_screen():                               # Settings for the largest screen. 
    global g_screen
    global g_second_margin
    width1 = 660
    height1 = 740
    g_screen = turtle.Screen()
    g_screen.setup(width1, height1)
    g_screen.title('Snake & monster')
    g_screen.tracer(0)                             # Turn off the built-in automatic screen refresh.
    return g_screen

# Set the upper status area.
def draw_g_second_margin():                        
    global g_second_margin
    global g_screen
    g_second_margin = turtle.Turtle()
    g_second_margin.up()                           # Avoid line drawing.
    g_second_margin.shape('square')
    g_second_margin.color('black', '')
    g_second_margin.shapesize(4, 25, 5)            # The size of the margin would be 80h * 500w.
    g_second_margin.goto(0, 250) # The margins between the status area and the screen edges would be 80 pixels around.
    g_screen.update()                              # Update manually.
    return g_second_margin

# Print the initial information in the status area.
def print_g_info1(contact_time, time, motion_status):       
    global g_info1
    global g_screen
    g_info1 = turtle.Turtle()
    g_info1.hideturtle()                           # Hide the pen.
    g_info1.up()                                   # Avoid line drawing.
    g_info1.goto(0, 250)                           # Print the information at the center of the status area.
    g_info1.write('Contact:%d        Time:%d       Motion:%s'%(contact_time, time,\
        motion_status), align = 'center', font = ('Arial', 14, 'normal'))
    g_screen.update()
    return g_info1

# settings for the motion area
def draw_g_third_margin():                         
    global g_third_margin
    global g_screen
    g_third_margin = turtle.Turtle()
    g_third_margin.up()
    g_third_margin.shape('square')
    g_third_margin.shapesize(25, 25, 5)            # The size of the margin would be 500w * 500w.
    g_third_margin.color('black', '')               
    g_third_margin.goto(0, -40)
    g_screen.update()
    return g_third_margin

# Print the initial information in the motion area.
def print_g_info2():                               
    global g_info2
    global g_screen
    g_info2 = turtle.Turtle()
    g_info2.hideturtle()
    g_info2.up()
    g_info2.goto(-200, 50)
    content = '''
    Welcome to Alan\'s version of snake....

    You are going to use the four arrow keys to move the snake 
    around the screen, trying to consume all the food items 
    before the g_monster catches you....
    
    Click anywhere on the screen to start.... 
    '''
    g_info2.write(content, align = 'left', font = ('Arial', 10, 'normal'))
    g_screen.update()
    return g_info2

# Create the initial interface.
def setScreen():
    draw_g_screen()
    draw_g_second_margin()
    draw_g_third_margin()
    print_g_info1(0, 0, 'Paused')
    print_g_info2()
    init_snake()
    init_g_monster()
    return

# Realize the updates after the user click the screen.
def Click(x, y):
    global g_screen, g_start_time, g_info2, g_screen
    global g_snake_head, g_food_list
    g_start_time = time.time()
    cor = pick_cor()                               # select places for the food
    set_food(cor)                                  # place all the food
    g_info2.clear()     
    g_monstermove()                                # Let the monster move.
    upgrade_g_info1()
    Keys()                                         # finish key configuration
    g_screen.onscreenclick(None)                   # avoid the effects of follow-up clicking the screen.

# keys configuration:up, down, left, right, and paused
def Keys():
    global g_screen
    g_screen.onkey(snake_up, 'Up')
    g_screen.onkey(snake_down, 'Down')
    g_screen.onkey(snake_left, 'Left')
    g_screen.onkey(snake_right, 'Right')
    g_screen.onkey(g_state_control, 'space')
    g_screen.listen()

# Functions for snake settings.
# initialize the snake.
def init_snake():
    global g_snake_head
    global g_screen
    g_snake_head = turtle.Turtle()
    g_snake_head.up()
    g_snake_head.goto(0, -40)
    g_snake_head.shape('square')
    g_snake_head.shapesize(1, 1, 1)
    g_snake_head.color('', 'red')
    g_screen.update()
    return g_snake_head

# The following four functions are used to control the snake's direction while moving.
def snake_up():
    global g_snake_head, g_screen, g_state, g_renew
    g_snake_head.setheading(90)
    if g_renew == False:                           # check whether the game is paused at half way
        g_renew = not g_renew                      # Pressing 'up' can unpaused the game.
    if g_state == 0:                               # When the game is on but the snake has not started to extend,
        gaming()                                   # start the main function of the game.

def snake_down():
    global g_snake_head, g_screen, g_state, g_renew
    g_snake_head.setheading(270)
    if g_renew == False:
        g_renew = not g_renew
    if g_state == 0:
        gaming()

def snake_right():
    global g_snake_head, g_screen, g_state, g_renew
    g_snake_head.setheading(0)
    if g_renew == False:
        g_renew = not g_renew
    if g_state == 0:
        gaming()

def snake_left():
    global g_snake_head, g_screen, g_state, g_renew
    g_snake_head.setheading(180)
    if g_renew == False:
        g_renew = not g_renew
    if g_state == 0:
        gaming()

# Check whether the snake needs to extend or move. 
# refresh the length of the snake
def update_bodylength(length):
    global g_food_list, g_snake_head, g_eat_list
    for i in range(0, len(g_food_list)):             # All the food turtles are stored in the g_food_list.
        # check whether the snake has eat the food
        # The food would be eaten if the location of the snake's head is matched with the following conditions and the food hasn't been eaten.
        if abs(g_snake_head.ycor() - g_food_list[i].ycor() - 5) <= 5 and\
            abs(g_snake_head.xcor() - g_food_list[i].xcor()) <= 5 and\
            g_eat_list[i] == 0:
            length = length + i + 1                  # update the length of the snake's body.
            g_eat_list[i] = 1                        # '1' represents that the food is consumed.
            g_food_list[i].clear()
            return length
    return length

# Check whether the snake can move.
def move_ability():
    if check_win() == False and check_game_over() == False and\
        reach_boundary() == False:
        return True
    else:
        return False

# Functions for g_monster settings.
# initialize the monster.
def init_g_monster():
    global g_monster, g_screen, g_x_numlist, g_y_numlist, g_snake_head
    # randomly pick x and y coordinates until they match the condition.
    while True:
        x = random.choice(list(range(-240, 240)))
        y = random.choice(list(range(-280, 200)))
        if g_snake_head.distance(x, y) >= 150:       # set the distance between the monster and the snake to be larger or equal to 150 pixels.
            g_monster = turtle.Turtle()
            g_monster.up()
            g_monster.goto(x, y)
            g_monster.shape('square')
            g_monster.shapesize(1, 1, 1)
            g_monster.color('', 'purple')
            g_screen.update()
            break
        else:
            continue

# select the correct direction for the monster to move.
def g_monster_dir():
    global g_monster, g_snake_head
    g_monster.up()
    g_monster.setheading(0)
    angle = g_monster.towards(g_snake_head)
    # Choosing the angles properly such that the monster can always move toward the snake.
    if angle <= 45 or angle > 315:
        g_monster.setheading(0)
    elif 45 < angle <= 135:
        g_monster.setheading(90)
    elif 135 < angle <= 225:
        g_monster.setheading(180)
    elif 225 < angle <= 315:
        g_monster.setheading(270)

# Let the monster move.
def g_monstermove():
    global g_monster, g_screen, g_renew, g_body_length, g_body_id
    g_monster_dir()
    contact()                             # When the monster is repositioned, update the number of contacts between the monster and the snake's body.
    if check_game_over() == False and check_win() == False:
        if  g_body_length > len(g_body_id):        # When the snake is extending, also slow down the monster's rate.            
            g_monster_rate1 = random.randint(450, 550)      # make the monster a little bit faster or slower than the snake.
            g_monster.forward(20)
            g_screen.update()
            g_screen.ontimer(g_monstermove, g_monster_rate1)
        elif g_body_length == len(g_body_id):      # When the snake is simply moving, make the monster faster. 
            g_monster_rate2 = random.randint(250, 350)
            g_monster.forward(20)
            g_screen.update()
            g_screen.ontimer(g_monstermove, g_monster_rate2)

# Functions for food settings.
# randomly pick coordinates.
def pick_cor():
    global g_x_numlist, g_y_numlist
    random.shuffle(g_x_numlist)
    random.shuffle(g_y_numlist)
    x_chooselist = g_x_numlist[:9:]       # Choose the first nine values to be the x coordinates of the food.
    y_chooselist = g_y_numlist[:9:]       # Choose the first nine y coordinates.
    cor_list = list(zip(x_chooselist, y_chooselist))        
    cor_dict = {1:cor_list[0], 2:cor_list[1], 3:cor_list[2], 4:cor_list[3],\
        5:cor_list[4], 6:cor_list[5], 7:cor_list[6], 8:cor_list[7], 9:cor_list[8]}
    return cor_dict

# Set all the food on the screen.
def set_food(pick_cor):
    global g_food_list  
    i = 1
    while i <= 9:
        g_food_list.append(turtle.Turtle(visible = False))        # Create turtles and hide them.
        i += 1
    for k in range(1, 10):
        g_food_list[k - 1].up()                                   # prevent line drawing.
        g_food_list[k - 1].goto(pick_cor[k][0], pick_cor[k][1] - 5)   # Y coordinates are substracted by five to better align at the snake head.
        g_food_list[k - 1].write(str(k), align = 'center',\
            font = ('Arial', 10, 'normal'))

# Functions for game control.
# control the state of the game: paused or unpaused
def g_state_control():
    global g_renew
    g_renew = not g_renew

# move the snake's body
def move():
    global g_snake_head, g_body_id, g_body_pos, g_screen
    extend()
    g_snake_head.clearstamp(g_body_id[0])       # clear the tail of the snake after adding one unit to the snake's body
    g_body_id.pop(0)                            # pop out the last elements in the id list
    g_body_pos.pop(0)                           # pop out the last elements in the position list

# extend the snake's body
def extend():
    global g_snake_head, g_body_id, g_body_pos
    color = g_snake_head.color()
    g_snake_head.color('blue', 'black')         # change the head's color into the body's color
    g_body_id.append(g_snake_head.stamp())      # use stamp() method to create a new unit of the body
    g_body_pos.append(g_snake_head.position())  
    g_snake_head.color(*color)                  # change the head's color back to its original color
    g_snake_head.forward(20)

# count the number of contact.
def contact():
    global g_contact_number, g_body_pos, g_monster
    for position in g_body_pos:
        # The snake contacts with the monster when the difference between its body's x and y cordinates and the monster's coordinates are less than 10.
        if abs(g_monster.xcor() - position[0]) < 15 and\
            abs(g_monster.ycor()- position[1]) < 15:
            g_contact_number += 1
        else:
            pass

# update information in status area.   
def upgrade_g_info1():
    global g_info1, g_start_time, g_screen, g_snake_head, g_renew, g_contact_number
    current_time = time.time()
    delta_t = current_time - g_start_time
    if check_game_over() == False and check_win() == False:           
        if g_renew == False or g_state == 0:        # the player press paused or the game is on but the player hasn't made any moves
            motion = 'Paused'
        else: 
            if g_snake_head.heading() == 0:
                motion = 'Right'
            elif g_snake_head.heading() == 90:
                motion = 'Up'
            elif g_snake_head.heading() == 180:
                motion = 'Left'
            else:
                motion = 'Down'
        # update the information according to different situations.
        g_info1.clear()    
        g_info1.up()
        g_info1.hideturtle()
        g_info1.write('Contact:' + str(int(g_contact_number)) + '        Time:' +\
            str(int(delta_t)) + '       Motion:' + motion, align = 'center',\
            font = ('Arial', 14, 'normal'))
        g_screen.update()
        g_screen.ontimer(upgrade_g_info1, 500)
    else:
        pass

# check whether the monster makes a head-on collision with the snake.
def check_game_over():
    global g_snake_head
    global g_monster
    # Set the difference to be 18 such that the monster overlaps with the snake's head a bit when game is over.
    if abs(g_snake_head.xcor() - g_monster.xcor()) < 18 and abs(g_snake_head.ycor() - g_monster.ycor()) < 18:
        result = True
    else:
        result = False
    return result

# check whether the snake has reached the boundary.      
def reach_boundary():
    global g_snake_head
    x = g_snake_head.xcor()
    y = g_snake_head.ycor()
    # The snake is moving upward and reach the upper boundary.
    if g_snake_head.heading() == 90 and y >= 190:
        return True
    # The snake is moving downward and reach the lower boundary.
    if g_snake_head.heading() == 270 and y <= -270:
        return True
    # The snake is moving leftward and reach the left boundary.
    if g_snake_head.heading() == 180 and x <= -230:
        return True
    # The snake is moving rightward and reach the right boundary.
    if g_snake_head.heading() == 0 and x >= 230:
        return True
    return False

# check whether the player win the game.
def check_win():
    global g_body_id
    # When the snake's body has 50 units, the player win.
    if len(g_body_id) == 50:
        return True
    else:
        return False

# The gaming() function is used to control the main process of the whole game.
def gaming():
    global g_snake_head, g_screen, g_state, g_info2
    global g_body_id, g_body_pos, g_body_length, g_renew
    g_body_length = update_bodylength(g_body_length)
    g_state = 1         # The player enter the game interface and has dicided the direction for the snake to move.
    if move_ability() == True and g_renew == True:
        if g_body_length > len(g_body_id):          # The snake needs to extend.
            extend()
            g_screen.ontimer(gaming, 300)
            g_screen.update()
        elif g_body_length == len(g_body_id):       # The snake moves forward without extending.
            move()
            g_screen.ontimer(gaming, 250)
            g_screen.update()
    elif g_renew == False:                          # The player press space and the game is paused.
        if check_game_over() == True:             
            g_info2.up()
            g_info2.goto(g_snake_head.xcor(), g_snake_head.ycor() + 15)
            g_info2.color('red')
            g_info2.pendown()
            g_info2.write('Game Over', align = 'center',\
                font = ('Arial', 12, 'normal'))
            g_screen.update()
        else:                                       # The player stop the game but hasn't lost the game.
            g_screen.ontimer(gaming, 300)
            g_screen.update()
    elif reach_boundary() == True:                  # The snake reach the boundaries.
        if check_game_over() == True:               # The snake keep still and is hit by the monster.    
            g_renew = False
            g_info2.up()
            g_info2.goto(g_snake_head.xcor(), g_snake_head.ycor() + 15)
            g_info2.color('red')
            g_info2.pendown()
            g_info2.write('Game Over', align = 'center',\
                font = ('Arial', 12, 'normal'))
            g_screen.update()
        else:
            g_screen.ontimer(gaming, 300)
            g_screen.update()
    elif check_game_over() == True:                 # The player lose the game.
        g_renew = False
        g_info2.up()
        g_info2.goto(g_snake_head.xcor(), g_snake_head.ycor() + 15)
        g_info2.color('red')
        g_info2.pendown()
        g_info2.write('Game Over!!!!!!!', align = 'center',\
            font = ('Arial', 12, 'normal'))
        g_screen.update()
    elif check_win() == True:                       # The player wins the game.
        g_renew = False
        g_info2.up()
        g_info2.goto(g_snake_head.xcor(), g_snake_head.ycor() + 15)
        g_info2.color('red')
        g_info2.pendown()
        g_info2.write('Winner!!!!!!!', align = 'center',\
            font = ('Arial', 12, 'normal'))
        g_screen.update()
            
setScreen()                 # set up initial interface.
g_screen.onclick(Click)     # arrange all the events after the player click the screen and enter the gaming interface.
g_screen.listen()
g_screen.mainloop()