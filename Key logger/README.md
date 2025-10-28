# Basic Keylogger Tool
A simple Python-based keylogger that captures and logs keystrokes to a text file. Designed for educational purposes and authorized testing only.

## Features
- Captures all keyboard keys including special keys
- Logs keystrokes continuously to timestamped log files
- Supports graceful termination on ESC key
- Optionally sends logs via email (SMTP configuration required)
- Uses `pynput` for keyboard event monitoring
- Runs cross-platform (Windows, Linux, Mac)
- Minimal dependencies for easy setup

## Installation
1. Clone the repository:
   ```
   git clone <repo-url>
   ```
2. Install the required Python package:
   ```
   pip install -r requirements.txt
   ```
## Usage
Run the keylogger with:
```
python key_logger.py
```
Press the ESC key to stop logging and save the current log file.

## Ethical Considerations
> This tool is intended solely for ethical and educational use. Unauthorized logging of keystrokes is illegal and unethical. Use only with explicit consent on devices you own or administer.

## Sample Log Output
Stored in the `/logs` directory, filenames include timestamps for easy reference. Example:
```
keylog-2025-10-09-232558_2025-10-09-232658.txt
```
## License
Distributed under the MIT License. See LICENSE file for details.

## Author
Pranav Suryawanshi
