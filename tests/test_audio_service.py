import pytest
from service.AudioService import AudioService
from config.AppSettings import AppSettings
import subprocess

def test_audio_service_generation(mocker):
    # Isolate from physical OS
    mock_run = mocker.patch("subprocess.run")
    
    service = AudioService()
    
    # Path is mocked so it doesn't write anything during CI
    output_path = "output/test_audio.aiff"
    text = "Good morning!"
    
    result = service.generate_podcast(text, output_path)
    
    # Verification
    assert result == output_path
    mock_run.assert_called_once()
    
    args = mock_run.call_args[0][0]
    assert args == ["say", "-o", output_path, text]
