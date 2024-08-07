import os
import shutil
import pytest
from mp3_converter.mp3_converter import convert_to_mp3, copy_metadata, process_directory

@pytest.fixture(scope="session")
def fixtures_dir():
    return os.path.join(os.path.dirname(__file__), 'fixtures')

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

@pytest.fixture
def sample_files(fixtures_dir, temp_dir):
    for file in ['sample.flac', 'sample.aiff', 'sample.wav']:
        source = os.path.join(fixtures_dir, file)
        if os.path.exists(source):
            shutil.copy(source, temp_dir)
        else:
            pytest.skip(f"Fixture file {file} not found. Run download_tests.sh to download test fixtures.")
    return temp_dir

def test_convert_to_mp3(sample_files):
    input_path = os.path.join(sample_files, "sample.flac")
    output_path = os.path.join(sample_files, "output.mp3")
    convert_to_mp3(input_path, output_path)
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0

def test_copy_metadata(sample_files):
    input_path = os.path.join(sample_files, "sample.flac")
    output_path = os.path.join(sample_files, "output.mp3")
    convert_to_mp3(input_path, output_path)
    copy_metadata(input_path, output_path)
    # Here you would typically check if the metadata was correctly copied
    # This would require reading the metadata from both files and comparing them

def test_process_directory(sample_files):
    success, failed = process_directory(str(sample_files), remove_original=False, bypass_prompt=True)
    assert success + failed > 0, "No files were processed"
    assert any(f.endswith('.mp3') for f in os.listdir(sample_files)), "No MP3 files were created"

def test_process_directory_with_remove(sample_files):
    original_files = ['sample.flac', 'sample.aiff', 'sample.wav']
    for file in original_files:
        shutil.copy(os.path.join(sample_files, file), os.path.join(sample_files, f"copy_{file}"))
    
    success, failed = process_directory(str(sample_files), remove_original=True, bypass_prompt=True)
    assert success + failed > 0, "No files were processed"
    
    for file in original_files:
        mp3_file = os.path.splitext(file)[0] + '.mp3'
        assert os.path.exists(os.path.join(sample_files, mp3_file)), f"MP3 file not created: {mp3_file}"
        assert os.path.getsize(os.path.join(sample_files, mp3_file)) > 0, f"MP3 file is empty: {mp3_file}"
        assert not os.path.exists(os.path.join(sample_files, file)), f"Original file not removed: {file}"
        assert os.path.exists(os.path.join(sample_files, f"copy_{file}")), f"Copy file removed: copy_{file}"

def test_unsupported_file_type(sample_files):
    unsupported_file = os.path.join(sample_files, "unsupported.txt")
    with open(unsupported_file, 'w') as f:
        f.write("This is not an audio file")
    
    success, failed = process_directory(str(sample_files), remove_original=False, bypass_prompt=True)
    assert os.path.exists(unsupported_file)
    assert not os.path.exists(os.path.join(sample_files, "unsupported.mp3"))