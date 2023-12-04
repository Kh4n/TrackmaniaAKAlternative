# Trackmania Action Key Alternative

**USE AT YOUR OWN RISK. I AM NOT LIABLE IF YOU GET BANNED FOR USING THIS. THIS IS NOT AN APPROVED INPUT METHOD BY NADEO**

I created this as a test for an idea I had as an alternative to action keys. It works like this:
1. Press and hold the activation key (default `d`)
2. While holding, tap/press left/right to start steering
    - Instead of your steering input being fixed, it will gradually increase from 15% - 100%. Exact rate is 4% / 120th of a second, and decays over 0.2 seconds to 1.5% / 120th of a second
3. Your steering is held as long as you hold the activation key. You can adjust it by pressing left/right
4. Once you release the activation key, it works just like an action key would: your steering is locked to whatever percentage you built it up to while holding
5. Pressing the reset key (default `f`) will bring you back to 100% steering
6. Pressing the activation key again will restart the process

To use:
1. Download and install Python 3
2. Ensure your installation came with `pip`
    - `Windows + R`, type `cmd`, type `pip -V`, you should see something like
    ```
    pip 21.2.4 from C:\Python310\lib\site-packages\pip (python 3.10) 
    ```
3. Run `pip install vgamepad pynput`
4. Run `python steer.py`
5. You can verify it's working by the Windows device connected sound and testing it here: https://hardwaretester.com/gamepad
6. Make sure you unbind left, right, `d`, and `f` from your Trackmania settings. If you change the keys make sure you unbind those instead
7. You can change the keys in the code using the constants at the top

When driving, if you have the dashboard plugin, the input display will flicker between KB and analog steering. I am not sure how to fix this. Binding controller buttons as inputs was not possible when I tried this. I just drove without looking at the dashboard.

Here is a comparison video using this tool + same track on controller: https://www.youtube.com/watch?v=HM0la9-Z4vY 
