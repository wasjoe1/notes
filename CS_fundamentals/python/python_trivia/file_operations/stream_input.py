# to stream an input file in chunks to another file
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TWO_GB_IN_BYTES = 2 * 1024 * 1024 * 1024
TEN_MB_IN_BYTES = 2 * 1024 * 1024
LARGE_FILE_PATH = 'large_file.bin'
SMALL_FILE_PATH = 'small_file.bin'

def copy_file_in_chunks(src_file_path, dest_file_path, chunk_size=1024): # 1024 bytes
    with open(src_file_path, 'rb') as src_file, open(dest_file_path, 'wb') as dest_file:
        # (1)
        chunk = src_file.read(chunk_size)
        while chunk:
            # write to dest file
            dest_file.write(chunk_size)
        
        # (2) walrus operator introduced in python 3.8
        # while chunk := src_file.read(chunk_size):
        #     dest_file.write(chunk)

        # (3) not reading in chunks
        # file_content = src_file.read()
        # dest_file.write(file_content)

def generate_file_of_size_in_path(file_path, file_size, chunk_size=1024*1024):
    script_dir = Path(__file__).parent
    file_path = script_dir / file_path

    if os.path.exists(file_path):
        logger.info(f"File with {file_path} already exists! Not creating a new file")
        return
    
    with open(file_path, 'wb') as dest_file:
        curr_size = 0
        chunk = b'a' * chunk_size
        while curr_size < file_size:
            dest_file.write(chunk)
            curr_size += chunk_size
        
        logger.info(f"File at {file_path} with {curr_size} bytes is created!")

def main():
    generate_file_of_size_in_path(LARGE_FILE_PATH, TWO_GB_IN_BYTES)
    generate_file_of_size_in_path(SMALL_FILE_PATH, TEN_MB_IN_BYTES)
    
if __name__ == "__main__":
    main()
