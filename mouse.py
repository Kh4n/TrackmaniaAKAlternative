import vgamepad as vg
import time
from pynput.keyboard import Key, Listener
from pynput import mouse
from pynput.mouse import Button

ACTIVATION_KEY = 'd'
RESET_KEY = 'f'
LEFT = Key.left
RIGHT = Key.right
GAMEPAD_ATTEMPTS = 5
MOUSE_BUTTON = Button.left

MAX_JOY = 32768
FPS = 120
TARGET = 1/FPS

def clip(v, l, h):
    if v < l:
        return l
    if v > h:
        return h
    return v

class KbSteer:
    gamepad = None
    leftPressed = False
    rightPressed = False
    prevLeftPressed, prevRightPressed = leftPressed, rightPressed
    activated = False
    mouseActive = False
    mousePos = (0, 0)
    reset = False
    steer = 0

    def on_move(self, x, y):
        self.mousePos = (x, y)
    
    def on_click(self, x, y, button, pressed):
        if button == MOUSE_BUTTON:
            self.mouseActive = pressed

    def onPress(self, key):
        try:
            if key.char == ACTIVATION_KEY:
                self.activated = True
            if key.char == RESET_KEY:
                self.reset = True
        except AttributeError:
            if key == LEFT:
                self.leftPressed = True
            if key == RIGHT:
                self.rightPressed = True

    def onRelease(self, key):
        try:
            if key.char == ACTIVATION_KEY:
                self.activated = False
            if key.char == RESET_KEY:
                self.reset = False
        except AttributeError:
            if key == LEFT:
                self.leftPressed = False
            if key == RIGHT:
                self.rightPressed = False

    mouseStart = None
    def attemptMouseUpdate(self):
        if not self.mouseActive:
            self.mouseStart = None
            return
        if self.mouseActive and self.mouseStart is None:
            self.mouseStart = self.mousePos
        self.steer = (self.mousePos[0] - self.mouseStart[0]) / 300
    
    def defaultUpdate(self):
        self.steer = 0
        if self.leftPressed:
            self.steer -= 1.0
        if self.rightPressed:
            self.steer += 1.0
        

    def start(self):
        for _ in range(GAMEPAD_ATTEMPTS):
            try:
                self.gamepad = vg.VX360Gamepad()
                break
            except Exception as e:
                print(f"unable to connect gamepad, error <{e}>, retrying...")
                time.sleep(1)
        else:
            print("unable to connect to virtual gamepad after {GAMEPAD_ATTEMPTS} attempts, exiting")
        self.listener = Listener(
            on_press=self.onPress,
            on_release=self.onRelease
        )
        self.listener.start()

        listener = mouse.Listener(
            on_click=self.on_click,
            on_move=self.on_move
        )
        listener.start()

        while True:
            t = time.perf_counter()

            if self.activated:
                self.attemptMouseUpdate()
            else:
                self.defaultUpdate()
            self.steer = clip(self.steer, -1.0, 1.0)

            if self.steer <= 0:
                self.gamepad.left_joystick(int(MAX_JOY * self.steer), 0)
            elif self.steer > 0:
                self.gamepad.left_joystick(int(MAX_JOY * self.steer) - 1, 0)
            self.gamepad.update()

            delta = time.perf_counter() - t
            time.sleep(max(0, TARGET - delta))

kbsteer = KbSteer()
kbsteer.start()