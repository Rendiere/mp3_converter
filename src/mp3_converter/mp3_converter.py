import os
import wave
import subprocess
from pydub import AudioSegment
from mutagen.flac import FLAC
from mutagen.aiff import AIFF
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def print_colored(text, color, bold=False):
    style = Style.BRIGHT if bold else ""
    print(f"{style}{color}{text}{Style.RESET_ALL}")

def convert_to_mp3(input_file, output_file):
    try:
        logger.info(f"Attempting to convert {input_file} to MP3")
        if input_file.lower().endswith('.flac'):
            audio = AudioSegment.from_file(input_file, format="flac")
        elif input_file.lower().endswith('.aiff'):
            audio = AudioSegment.from_file(input_file, format="aiff")
        elif input_file.lower().endswith('.wav'):
            audio = AudioSegment.from_file(input_file, format="wav")
        else:
            raise ValueError(f"Unsupported file format: {input_file}")

        logger.info(f"File loaded successfully. Duration: {len(audio)} ms")
        
        logger.info(f"Exporting to MP3: {output_file}")
        audio.export(output_file, format="mp3", bitrate="320k")
        logger.info(f"Conversion successful: {output_file}")
        print_colored(f"Converted: {input_file}", Fore.GREEN)
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
        raise
    except pydub.exceptions.CouldntDecodeError as e:
        logger.error(f"Failed to decode {input_file}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error converting {input_file} to MP3: {str(e)}")
        raise

def copy_metadata(input_file, output_file):
    try:
        if input_file.lower().endswith('.flac'):
            input_audio = FLAC(input_file)
        elif input_file.lower().endswith('.aiff'):
            input_audio = AIFF(input_file)
        elif input_file.lower().endswith('.wav'):
            input_audio = wave.open(input_file, 'rb')
        else:
            raise ValueError(f"Unsupported file format: {input_file}")

        output_audio = MP3(output_file, ID3=EasyID3)
        
        if input_file.lower().endswith('.wav'):
            # WAV files don't typically contain metadata, so we'll add some basic info
            output_audio['title'] = os.path.splitext(os.path.basename(input_file))[0]
            output_audio['artist'] = 'Unknown'
        else:
            for key, value in input_audio.tags.items():
                if key in EasyID3.valid_keys.keys():
                    output_audio[key] = value
        
        output_audio.save()
        print_colored(f"Metadata copied: {input_file} -> {output_file}", Fore.BLUE)
    except Exception as e:
        logger.error(f"Error copying metadata from {input_file} to {output_file}: {str(e)}")
        raise

def process_directory(directory, remove_original, bypass_prompt=False):
    total_files = sum(1 for root, _, files in os.walk(directory) 
                      for file in files if file.lower().endswith(('.flac', '.aiff', '.wav')))
    
    print_colored(f"Found {total_files} FLAC/AIFF/WAV files to convert.", Fore.CYAN, bold=True)
    print_colored(f"Original files will be {'removed' if remove_original else 'kept'}.", Fore.YELLOW)
    
    if not bypass_prompt:
        confirm = input("Do you want to continue? (y/n): ").lower().strip()
        if confirm != 'y':
            print_colored("Operation cancelled.", Fore.RED)
            return 0, 0

    processed = 0
    success = 0
    failed = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.flac', '.aiff', '.wav')):
                input_path = os.path.join(root, file)
                output_path = os.path.splitext(input_path)[0] + '.mp3'
                
                try:
                    convert_to_mp3(input_path, output_path)
                    copy_metadata(input_path, output_path)
                    if remove_original and not file.startswith("copy_"):
                        os.remove(input_path)
                        print_colored(f"Removed original file: {input_path}", Fore.YELLOW)
                    success += 1
                except Exception as e:
                    print_colored(f"Error processing {input_path}: {str(e)}", Fore.RED)
                    failed += 1
                
                processed += 1
                print_colored(f"Progress: {processed}/{total_files}", Fore.BLUE)

    print_colored(f"Conversion complete. Processed {processed} files.", Fore.CYAN, bold=True)
    print_colored(f"Successful conversions: {success}", Fore.GREEN)
    print_colored(f"Failed conversions: {failed}", Fore.RED)

    return success, failed

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert FLAC, AIFF, and WAV files to MP3")
    parser.add_argument("directory", help="Directory to process")
    parser.add_argument("--remove", action="store_true", help="Remove original files after conversion")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print_colored(f"Error: {args.directory} is not a valid directory", Fore.RED)
        return

    process_directory(args.directory, args.remove)

if __name__ == "__main__":
    main()