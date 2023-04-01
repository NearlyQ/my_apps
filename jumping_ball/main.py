from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)
from kivy.vector import Vector
from kivy.clock import Clock


# Constant arguments. G - acceleration of gravity. С - Pixels in meter 
G = 9.8
C = 0.05


# Functions, that calculates psysical quantities
# Throw force returns a list with 2 coordinates:
# when ball was thrown and its position on previous frame
def throw_force(throw_force, num, item):
    if len(throw_force) < num:
        throw_force.append(item)
    elif len(throw_force) == num:
        throw_force.pop(0)
        throw_force.append(item)
    return throw_force
def find_velocity_y(y: float, tmp: int, smth: bool):
    speed = round(((2*G*(tmp-y)*C))**(1/2), 2)
    if smth:
        return -speed
    else:
        return speed
def find_velocity_x(coords):
    if len(coords) == 2:
        return (coords[1][0]-coords[0][0])*C
    else:
        return 0

def find_height_max(velocity_zero: float):
    return (velocity_zero**2)/(2*G)/C

def find_additional_velocity_zero(coords: list):
    if len(coords) == 2:
        return (coords[1][1]-coords[0][1])*C
    else:
        return 0


# Class JumpingBall, that has main jumper characteristics and functions
class JumpingBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity_zero = 0
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    moving = False
    coordinates = []
    gravitation = False
    falling = True
    condition_for_falling = True


# Moves ball according to his velocity
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


# When ball touches ground or walls, his horisontal velocity changes. 
# If horisontal velocity module less than 0.1, it became 0
    def change_velocity_x(self):
        if -0.1 >= self.velocity_x <= 0.1:
            self.velocity_x = 0
        else:
            self.velocity_x *= 0.8


# Main function, that simulates physics
    def physic(self):
        if self.condition_for_falling and self.gravitation:
            if self.y <= 0 and not self.moving:
                self.y = 1
                self.falling = False
                if (self.tmp*0.49) >= 2:
                    self.tmp = int(self.tmp*0.49)
                else:
                    self.condition_for_falling = False

            elif self.y >= self.tmp and not self.moving:
                self.y = self.tmp-1
                self.falling = True

            if not self.moving:
                self.velocity_y = find_velocity_y(self.y, self.tmp, self.falling)
        elif not self.condition_for_falling:
            self.velocity_y = 0

        if 0 <= self.y <= 4:
            if -0.01 <= self.velocity_x <= 0.01:
                self.velocity_x = 0
            else:
                self.velocity_x *= 0.95


# Main Window class
class JumpingBallGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    start = Label(text='Tap to turn on gravity')
    visible = True


# Function serves the ball to current position
    def serve_ball(self):
        self.ball.center = (self.center_x, self.top*0.8)
        self.ball.tmp = self.ball.y


# When button is pressed, gravitation turns on
    def turn_on_gravity(self):
        self.visible = False
        self.ball.gravitation = True
        self.start.text = ' '
        return self.ball.gravitation


# Update function, that executes dt times per second
    def update(self, dt):
        self.ball.physic()
        self.ball.move()
        
        if self.ball.x < 0:
            self.ball.x = 0
            self.ball.velocity_x *= -0.8
        elif self.ball.x > self.right - 50:
            self.ball.x = self.right - 50
            self.ball.velocity_x *= -0.8
    

# When player taps on the ball, it stops
    def on_touch_down(self, touch):
        if (self.ball.x-25) < touch.x < (self.ball.x+75) and \
            (self.ball.y-25) < touch.y < (self.ball.y+75) and \
            25 < touch.x < self.right-25 and \
            25 < touch.y < self.top-25:
            self.ball.velocity_zero = 0
            self.ball.velocity_y = 0
            self.ball.velocity_x = 0
            self.ball.moving = True


# When player moves the cursor after touching the ball, ball will follow the cursor
    def on_touch_move(self, touch):
        if self.ball.moving and 25 < touch.x < self.right-25 and \
            25 < touch.y < self.top-25:
            self.ball.velocity_y = 0
            self.ball.center_y = touch.y
            self.ball.center_x = touch.x
            throw_force(self.ball.coordinates, 2, (self.ball.center_x, self.ball.center_y))


# When player releases the cursor, the ball is thrown
    def on_touch_up(self, touch):
        if not self.visible and self.ball.moving:
            self.throw()
            self.ball.coordinates = []
            self.ball.num_of_bounce = 0
        else:
            self.turn_on_gravity()


# Function, that throws the ball
    def throw(self):
        self.ball.velocity_zero = find_additional_velocity_zero(self.ball.coordinates)
        self.ball.tmp = int(self.ball.y)+find_height_max(self.ball.velocity_zero)
        self.ball.velocity_x = find_velocity_x(self.ball.coordinates)
        self.ball.moving = False
        self.ball.condition_for_falling = True
        if self.ball.velocity_zero > 0:
            self.ball.falling = False
        elif self.ball.velocity_zero <= 0:
            self.ball.falling = True


# Main class, that starts the game
class JumpingBallApp(App):
    def build(self):
        game = JumpingBallGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    JumpingBallApp().run()
