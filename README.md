# MP3 Converter

A command-line tool to convert FLAC, AIFF, and WAV files to MP3 format.

## Installation

You can install MP3 Converter using Homebrew:

```
brew tap Rendiere/mp3_converter
brew install mp3_converter
```

## Usage

To convert all FLAC, AIFF, and WAV files in a directory:

```
mp3_converter /path/to/your/audio/directory
```

To convert and remove the original files:

```
mp3_converter /path/to/your/audio/directory --remove
```

## Features

- Converts FLAC, AIFF, and WAV files to MP3 format
- Preserves metadata when possible
- Option to remove original files after conversion
- Processes entire directories, including subdirectories

## Requirements

- Python 3.10+ & <3.13
- ffmpeg (will be installed automatically by Homebrew)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
