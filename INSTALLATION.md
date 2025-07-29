# Quick Installation Guide

## Windows Users

**Option 1: One-Click Launch**
- **Double-click** `run_alarm_clock.bat` to automatically install dependencies and start the application.

**Option 2: Command Line**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python alarm_clock.py

# Alternative commands
python3 alarm_clock.py
py alarm_clock.py
```

## macOS/Linux Users

**Option 1: Shell Script**
```bash
# Make executable and run
chmod +x run_alarm_clock.sh
./run_alarm_clock.sh
```

**Option 2: Command Line**
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the application
python3 alarm_clock.py

# Alternative commands
python alarm_clock.py
```

## Manual Installation (All Platforms)

1. **Install Python 3.6+** from [python.org](https://python.org)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python alarm_clock.py
   ```

## Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv alarm_env

# Activate virtual environment
# Windows:
alarm_env\Scripts\activate
# macOS/Linux:
source alarm_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python alarm_clock.py
```

## Test the Installation

Run the test suite to verify everything works:
```bash
python test_alarm.py
```

## Features

- ✅ Real-time clock display
- ✅ Multiple alarm support
- ✅ Custom alarm tones (MP3, WAV, OGG, M4A)
- ✅ Snooze functionality (1, 3, 5, 10, 15 minutes)
- ✅ Modern GUI interface
- ✅ Advanced alarm management:
  - Add, remove, edit alarms
  - Clear all alarms
  - Right-click context menu
  - Test alarm functionality
- ✅ Visual alarm controls with status indicators

## Troubleshooting

### Common Issues

**Audio Issues**
- **No sound**: Ensure your system has audio drivers installed
- **Import errors**: Run `pip install -r requirements.txt`
- **Sound continues after stopping**: Fixed in latest version

**GUI Issues**
- **Tkinter not found**: On Linux, install tkinter:
  ```bash
  sudo apt-get install python3-tk  # Ubuntu/Debian
  sudo dnf install python3-tkinter # Fedora
  ```

**Running Issues**
- **Command not found**: Ensure Python is in your PATH
- **Permission errors**: Use virtual environment or run as administrator
- **Script not executable** (Linux/macOS): Run `chmod +x run_alarm_clock.sh`

### Quick Commands for Testing

```bash
# Check Python version
python --version

# Test the application
python test_alarm.py

# Verify dependencies
pip list | grep -E "(pygame|numpy|scipy)"
``` 