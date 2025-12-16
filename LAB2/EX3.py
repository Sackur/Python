import re
from typing import Dict, List, Set
import os

# Configuration
LOG_FILE_NAME = 'apache_logs.txt'
IP_OUTPUT_FILE = 'filtered_ips.txt'
ALLOWED_IPS = ["192.168.1.10", "10.0.0.5", "127.0.0.1"]


def filter_ips(input_file_path: str, output_file_path: str, allowed_ips: List[str]) -> None:
    """
    Filters IPs from the log file against allowed_ips list and writes counts to output file.
    (Task 3, Points 1, 2, 3, 4, 5)
    """
    ip_counts: Dict[str, int] = {}
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    # 2. Use a set for quick O(1) IP lookup.
    allowed_ips_set: Set[str] = set(allowed_ips)

    try:
        # 1. Read IP addresses from the input file.
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                match = ip_pattern.match(line)
                if match:
                    ip_address = match.group(0)
                    # 2. Check if IP is allowed.
                    if ip_address in allowed_ips_set:
                        # 3. Count occurrences.
                        ip_counts[ip_address] = ip_counts.get(ip_address, 0) + 1

    except FileNotFoundError:
        # 5. Handle missing input file.
        print(f"Error in Task 3 (FileNotFoundError): Input log not found: '{input_file_path}'")
        return
    except IOError as e:
        print(f"Error in Task 3 (IOError): Error reading input file '{input_file_path}': {e}")
        return

    # 4. Write the result to the output file.
    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for ip, count in ip_counts.items():
                # Required format: <IP address> - <count>
                outfile.write(f"{ip} - {count}\n")
        print(f"Task 3: Successfully wrote results to '{output_file_path}'")

    except IOError as e:
        # 5. Handle output file writing error.
        print(f"Error in Task 3 (IOError): Error writing to output file '{output_file_path}': {e}")
        return


# EXECUTION BLOCK
if __name__ == '__main__':

    # SETUP: Ensure apache_logs.txt exists for reading
    if not os.path.exists(LOG_FILE_NAME):
        print(f"SETUP: ERROR! Please ensure '{LOG_FILE_NAME}' exists and contains data.")
    else:
        print("--- Running Task 3: IP Filter ---")
        filter_ips(LOG_FILE_NAME, IP_OUTPUT_FILE, ALLOWED_IPS)

        # Verify output content
        if os.path.exists(IP_OUTPUT_FILE):
            print(f"\nContent of {IP_OUTPUT_FILE}:")
            with open(IP_OUTPUT_FILE, 'r') as f:
                print(f.read().strip())