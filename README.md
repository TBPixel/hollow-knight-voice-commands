# Hollow Knight speech-to-text commands

A fun little tool to play Hollow Knight with only voice commands.

## Installation

Download the latest build from [releases](https://github.com/TBPixel/hollow-knight-voice-commands/releases). When you run for the first time it will generate a `config.yaml` file in the same directory. You can edit this file to change the default keybinds and command text, or use the defaults.

*Note:* Some special keyboard characters like `[` will need to be wrapped in quotes in the config. For example, `'['`. Refer to the [example.config.yaml](./example.config.yaml) for reference of defaults.

## Development

Clone the repository, cd inside and setup your virtual environment.

```shell
git clone git@github.com:TBPixel/hollow-knight-voice-commands.git
cd hollow-knight-voice-commands
python -m venv .
./Scripts/activate
```

You'll need `pipwin` to get pyaudio setup.

```shell
pip install pipwin
pipwin install pyaudio
```

Run with

```shell
pip install -r requirements.txt
python ./hk-voice-commands.py
```

Build with

```shell
pyinstaller --onefile ./hk-voice-commands.py
```
