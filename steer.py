import vgamepad as vg
import time
from pynput.keyboard import Key, Listener

ACTIVATION_KEY = 'd'
RESET_KEY = 'f'
LEFT = Key.left
RIGHT = Key.right
GAMEPAD_ATTEMPTS = 5

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
    reset = False
    steer = 0

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

    speed = 0.02
    maxSpeedDecay = 0.0125
    decayTime = 0.2
    decayStart = time.perf_counter()
    steerSave = steer
    base = 0.15
    steerCap = 1
    mode = None
    def attempt6_2Update(self):
        if self.leftPressed and self.mode is None:
            self.mode = "left"
            self.steerCap = self.base
            self.decayStart = time.perf_counter()
        if self.rightPressed and self.mode is None:
            self.mode = "right"
            self.steerCap = self.base
            self.decayStart = time.perf_counter()
        speedDecay = clip((time.perf_counter() - self.decayStart) / self.decayTime, 0, 1)*self.maxSpeedDecay
        if self.leftPressed:
            if self.mode == "left":
                self.steerCap += self.speed - speedDecay
            elif self.mode == "right":
                self.steerCap -= self.speed - speedDecay
        if self.rightPressed:
            if self.mode == "right":
                self.steerCap += self.speed - speedDecay
            elif self.mode == "left":
                self.steerCap -= self.speed - speedDecay
        if self.mode == "left":
            self.steer = -self.steerCap
        elif self.mode == "right":
            self.steer = self.steerCap
    
    def defaultUpdate(self):
        self.steer = 0
        self.mode = None
        if self.reset:
            self.steerCap = 1
        if self.leftPressed:
            self.steer -= self.steerCap
        if self.rightPressed:
            self.steer += self.steerCap
        

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

        while True:
            t = time.perf_counter()

            if self.activated:
                self.attempt6_2Update()
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