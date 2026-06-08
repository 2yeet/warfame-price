import pyautogui
import time
import keyboard

#capture key reference
#You only have to mark the area where item name appears, 
#notice that it's possible that item name takes two line e.g. wukong prime system blueprint,
#make sure you select the whole area
#keys are set to be 6,7,8,9 in default, bc 1~4 is utility button
#
# 6 . . . . . . . . 7
# . OPENED RELICS . .
# . ITEM NAME ONLY. .
# 9 . . . . . . . . 8
#
#enter a game with full squad(4 ppl), select the area with key 6,7,8,9, press q to exit the program

s_width, s_height = pyautogui.size()
while True:
    x, y = pyautogui.position()
    if keyboard.is_pressed('q'):
        break

    if keyboard.is_pressed('6'):
        x1 = x
        y1 = y
        print("first 1: ", "X= ",x, "Y= ",y)
    if keyboard.is_pressed('7'):
        x2 = x
        y2 = y
        print("first 2: ", "X= ",x, "Y= ",y)
    if keyboard.is_pressed('8'):
        x3 = x
        y3 = y
        print("first 3: ", "X= ",x, "Y= ",y)
    if keyboard.is_pressed('9'):
        x4 = x
        y4 = y
        print("first 4: ", "X= ",x, "Y= ",y)
    time.sleep(0.1)

top = (y1+y2)/2
left = (x1+x4)/2
bottom = (y3+y4)/2
right = (x2+x3)/2

width = right-left
height = bottom - top

print('Suggest replacing line 12 in capture.py with:')
print('g = ' + str([left,top,right,bottom]))

