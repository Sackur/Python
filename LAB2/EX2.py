import hashlib
from typing import Dict, Union
import os

#  Configuration for testing
HASH_FILE_1 = 'hash_data_1.txt'
HASH_FILE_2 = 'hash_data_2.txt'


def generate_file_hashes(*file_paths: str) -> Union[Dict[str, str], None]:
    """
    Computes SHA-256 hashes for all provided files.
    (Task 2, Points 1, 2, 3, 5)
    """
    file_hashes: Dict[str, str] = {}

    for path in file_paths:
        hasher = hashlib.sha256()
        try:
            # 1. Open file in binary mode ('rb').
            with open(path, 'rb') as file:
                # 2. Compute SHA-256 in chunks.
                while chunk := file.read(4096):
                    hasher.update(chunk)

            # 3. Store the hash.
            file_hashes[path] = hasher.hexdigest()

        except (FileNotFoundError, IOError) as e:
            # 4. Handle exceptions.
            print(f"Error in Task 2 ({type(e).__name__}): Failed to hash '{path}': {e}")

    return file_hashes


#  EXECUTION BLOCK
if __name__ == '__main__':
    #  SETUP: Create dummy files for hashing
    if not os.path.exists(HASH_FILE_1):
        with open(HASH_FILE_1, 'w') as f: f.write("Test content 1.")
    if not os.path.exists(HASH_FILE_2):
        with open(HASH_FILE_2, 'w') as f: f.write("Test content 2 is different.")
    print(f"SETUP: Created dummy {HASH_FILE_1} and {HASH_FILE_2}.")

    print("\n Running Task 2: Hash Generator ")

    # Pass both dummy files and a non-existent one to test error handling
    results = generate_file_hashes(HASH_FILE_1, HASH_FILE_2, 'non_existent_hash.dat')

    if results:
        for path, hsh in results.items():
            print(f"File: {path}, SHA-256 Hash: {hsh}")