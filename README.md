# Hollow Knight speech-to-text commands

A fun little tool to play Hollow Knight with only voice commands.

## Installation

Download the latest build from releases. When you run for the first time it will generate a `config.yaml` file in the same directory. You can edit this file to change the default keybinds and command text, or use the defaults.

## Development

Run with

```shell
./Scripts/activate
pip install -r requirements.txt
python ./speech-to-text.py
```

Build with

```shell
pyinstaller --onefile ./speech-to-text.py
```
