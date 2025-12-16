import re
import os
from typing import Dict, Union


def analyze_log_file(log_file_path: str) -> Union[Dict[str, int], None]:
    """
    Analyzes the log file, counting unique HTTP response codes.
    (Task 1, Points 1, 2, 3, 5)
    """
    response_codes_counts: Dict[str, int] = {}
    # Regex to find the 3-digit status code.
    code_pattern = re.compile(r'\s(\d{3})\s')

    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = code_pattern.search(line)
                if match:
                    code = match.group(1)
                    # Store results (Task 1, Point 3).
                    response_codes_counts[code] = response_codes_counts.get(code, 0) + 1

        return response_codes_counts

    except (FileNotFoundError, IOError) as e:
        # Task 1, Point 4: Handle exceptions.
        print(f"Error in Task 1 ({type(e).__name__}): {e}")
        return None


# EXECUTION BLOCK
if __name__ == '__main__':
    LOG_FILE_NAME = 'apache_logs.txt'

    #  SETUP: Create a dummy log file if it doesn't exist for testing
    if not os.path.exists(LOG_FILE_NAME):
        import os

        dummy_content = """
127.0.0.1 - - [16/Dec/2025:10:00:00 +0200] "GET /index.html HTTP/1.1" 200 1234
127.0.0.1 - - [16/Dec/2025:10:00:01 +0200] "GET /image.png HTTP/1.1" 200 5678
127.0.0.1 - - [16/Dec/2025:10:00:02 +0200] "GET /missing.css HTTP/1.1" 404 98
127.0.0.1 - - [16/Dec/2025:10:00:03 +0200] "POST /submit HTTP/1.1" 302 0
"""
        with open(LOG_FILE_NAME, 'w', encoding='utf-8') as f:
            f.write(dummy_content)
        print(f"SETUP: Created dummy {LOG_FILE_NAME}.")

    print(" Running Task 1: Log Analyzer ")
    results = analyze_log_file(LOG_FILE_NAME)
    if results is not None:
        print(f"Analysis Results: {results}")

        # Test error handling
    analyze_log_file('non_existent.txt')