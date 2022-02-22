import asyncio
import math
import pyautogui
import speech_recognition as sr
import yaml
import os.path

# FRAMERATE defines the target input polling framerate
FRAMERATE = 60
# FRAMETIME defines the time between each frame
FRAMETIME = 1 / FRAMERATE

async def reset_timer(config: dict):
    keybind: str = config['keybinds']['livesplit_timer']
    pyautogui.press(keybind)
    await asyncio.sleep(1.0)
    pyautogui.press(keybind)
    await asyncio.sleep(1.0)
    pyautogui.press(keybind)

async def panic(config: dict):
    for i in range(5):
        await asyncio.sleep(FRAMETIME)
        direction = 'left'
        if i % 2 == 0:
            direction = 'right'
        await press_and_hold_key(config['keybinds'][direction], FRAMETIME*2)
        await press_and_hold_key(config['keybinds']['jump'], 0.1)
        await tap_key(config['keybinds']['nail'])

# press_and_hold_key for a duration in seconds
async def press_and_hold_key(key: str, seconds: float):
    pyautogui.keyDown(key)
    await asyncio.sleep(seconds)
    pyautogui.keyUp(key)

# mask_key for a duration in seconds
async def mash_key(key: str, seconds: float):
    repeats = math.ceil((FRAMERATE * seconds))
    pyautogui.press(key, presses=repeats, interval=FRAMETIME)

async def tap_key(key: str):
    pyautogui.press(key)

def movement_duration(text: str, config: dict) -> float:
    duration = 0.5
    extends: dict = config['commands']['move_extend']
    if extends['small'] in text:
        duration = 1.0
    if extends['medium'] in text:
        duration = 2.0
    if extends['large'] in text:
        duration = 5.0
    
    return duration

# handle the input from speech
async def handle_input(config: dict, mic_text: str):
    inputs = []
    keybinds: dict = config['keybinds']
    commands: dict = config['commands']
    if commands['left'] in mic_text:
        task = asyncio.create_task(press_and_hold_key(keybinds['left'], movement_duration(mic_text, config)))
        inputs.append(task)
    if commands['turn_left'] in mic_text:
        task = asyncio.create_task(press_and_hold_key(keybinds['left'], 0.1))
        inputs.append(task)
    if commands['right'] in mic_text:
        task = asyncio.create_task(press_and_hold_key(keybinds['right'], movement_duration(mic_text, config)))
        inputs.append(task)
    if commands['turn_right'] in mic_text:
        task = asyncio.create_task(press_and_hold_key(keybinds['right'], 0.1))
        inputs.append(task)
    if commands['jump_small'] in mic_text:
        task = asyncio.create_task(tap_key(keybinds['jump']))
        inputs.append(task)
    if  commands['jump_large'] in mic_text:
        task = asyncio.create_task(press_and_hold_key(keybinds['jump'], 1.0))
        inputs.append(task)
    if commands['dash'] in mic_text:
        task = asyncio.create_task(tap_key(keybinds['dash']))
        inputs.append(task)
    if commands['nail'] in mic_text:
        task = asyncio.create_task(mash_key(keybinds['nail'], 1.0))
        inputs.append(task)
    if commands['cast'] in mic_text:
        task = asyncio.create_task(tap_key(keybinds['cast']))
        inputs.append(task)
    if commands['focus'] in mic_text:
        task = asyncio.create_task(press_and_hold_key(keybinds['focus'], 1.3))
        inputs.append(task)
    if commands['load_save_state'] in mic_text:
        task = asyncio.create_task(tap_key(keybinds['load_save_state']))
        task2 = asyncio.create_task(reset_timer(config))
        inputs.append(task)
        inputs.append(task2)
    if commands['panic'] in mic_text:
        task = asyncio.create_task(panic(config))
        inputs.append(task)
    
    await asyncio.gather(*inputs)


async def handle_mic(r: sr.Recognizer, source: sr.Microphone) -> str:
    # wait for a second to let the recognizer
    # adjust the energy threshold based on
    # the surrounding noise level
    r.adjust_for_ambient_noise(source, duration=0.2)

    # listens for the user's input
    audio2 = r.listen(source, phrase_time_limit=2.5)

    # Using google to recognize audio
    mic_text = r.recognize_google(audio2)
    mic_text = mic_text.lower()
    print(mic_text)

    return mic_text


config_template_yaml = """
keybinds:
  jump: z
  left: left
  right: right
  nail: x
  dash: c
  cast: f
  focus: a
  load_save_state: '['
  livesplit_timer: '-'
commands:
  left: left
  right: right
  turn_left: west
  turn_right: east
  move_extend:
    small: long
    medium: long long
    large: uber
  jump_small: hop
  jump_large: jump
  dash: dash
  nail: nail
  cast: cast
  focus: focus
  panic: panic
  load_save_state: here we go again
"""


# main function
async def main():
    if not os.path.exists('config.yaml'):
        config = yaml.safe_load(config_template_yaml)

        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)

    config = yaml.safe_load(open('config.yaml'))

    # Initialize the recognizer
    r = sr.Recognizer()

    for i in range(3, 0, -1):
        print(i)
        await asyncio.sleep(1)
    
    print("Go!")
    print("Parsed mic text below:")

    # Loop infinitely for user to speak
    while(True):
        # Exception handling to handle
        # exceptions at the runtime
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source:
                mic_text = await handle_mic(r, source)
                await handle_input(config, mic_text)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occured")


# Run main
if __name__ == "__main__":
    asyncio.run(main())

