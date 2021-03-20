from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
import math
import os


sense = SenseHat()
sense.rotation = 180
sense.low_light = True

watering_time = time.time()
colour = [0, 255, 50]
speed = 0.1

# Show hours or days
text_hours = True
off = False
animation = False


def pushed_up(event):
    global text_hours
    if event.action == ACTION_PRESSED:
        text_hours = not text_hours


def pushed_down(event):
    global off
    if event.action == ACTION_PRESSED:
        off = not off 


def pushed_left(event):
    global speed
    if event.action == ACTION_PRESSED:
        if speed > 0.05:
            speed -= 0.02


def pushed_right(event):
    global speed
    if event.action == ACTION_PRESSED:
        if speed < 0.3:
            speed += 0.02


def pushed_middle(event):
    global watering_time
    global animation
    if event.action == ACTION_PRESSED:
        animation = True
        watering_time = event.timestamp


def watering_animation():
    global animation
    frames = os.listdir("animation_frames")
    frames.sort()
    for frame in frames:
        sense.load_image("animation_frames/"+frame)
        time.sleep(0.1)

    #animation finished
    animation = False


def main():
    sense.stick.direction_up = pushed_up
    sense.stick.direction_down = pushed_down
    sense.stick.direction_left = pushed_left
    sense.stick.direction_right = pushed_right
    sense.stick.direction_middle = pushed_middle
    
    while True:
        seconds = time.time() - watering_time
        hours = math.floor(seconds / 60 / 60) 
        days = math.floor(hours / 24)

        if off:
            colour = [0, 0 , 0]
        elif hours > 48:
            colour = [255, 0, 50]
        else:
            colour = [0, 255, 50]
        
        if animation:
            watering_animation()
        else:
            if text_hours:
                sense.show_message("Hours : " + str(hours), text_colour = colour, scroll_speed = speed)
            else:
                sense.show_message("Days : " + str(days), text_colour = colour, scroll_speed = speed)


if __name__ == "__main__":
    main()
