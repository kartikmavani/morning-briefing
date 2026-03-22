import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

class AudioService:
    """
    A 0-byte dependency service that hooks into specifically Apple's internal macOS 
    High-Fidelity Neural TTS system (NSSpeechSynthesizer) via the 'say' command.
    """
    def __init__(self):
        logger.info("Initializing offline MacOS Audio Synthesizer...")
        pass

    def generate_podcast(self, text: str, output_path: str):
        logger.info(f"Synthesizing script to {output_path}...")
        
        # Ensure the target directory structure exists
        target_file = Path(output_path)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # -o outputs an uncompressed AIFF high-fidelity audio file natively supported on Mac devices.
            subprocess.run(["say", "-o", str(target_file), text], check=True)
            logger.info(f"✅ Podcast generated successfully: {target_file}")
            return str(target_file)
        except subprocess.CalledProcessError as e:
            logger.error(f"macOS 'say' command failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to generate podcast audio: {e}")
            raise
