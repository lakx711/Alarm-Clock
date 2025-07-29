# 🔔 Python Alarm Clock

A feature-rich desktop alarm clock application built with Python and tkinter, featuring a modern GUI interface with customizable alarm tones and snooze functionality.

## Features

- **Real-time Clock Display**: Shows current time and date
- **Multiple Alarms**: Set and manage multiple alarms simultaneously
- **Custom Alarm Tones**: Choose from default sounds or select your own audio files
- **Snooze Functionality**: Snooze alarms for customizable durations (1, 3, 5, 10, or 15 minutes)
- **User-friendly GUI**: Clean and intuitive interface built with tkinter
- **Advanced Alarm Management**: 
  - Add, remove, and edit alarms
  - Clear all alarms at once
  - Right-click context menu for quick actions
  - Test alarm functionality
- **Visual Alarm Controls**: Prominent Stop and Snooze buttons with status indicators
- **Audio Support**: Supports MP3, WAV, OGG, and M4A audio formats

## Installation & Running

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Quick Start

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd alarm-clock
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python alarm_clock.py
   ```

### Alternative Ways to Run

#### Windows Users
```bash
# Method 1: Direct Python command
python alarm_clock.py

# Method 2: Using the batch file (automatically installs dependencies)
run_alarm_clock.bat

# Method 3: Using Python 3 explicitly
python3 alarm_clock.py
```

#### macOS/Linux Users
```bash
# Method 1: Using Python 3
python3 alarm_clock.py

# Method 2: Using the shell script (automatically installs dependencies)
./run_alarm_clock.sh

# Method 3: Make script executable first, then run
chmod +x run_alarm_clock.sh
./run_alarm_clock.sh
```

#### Using Virtual Environment (Recommended)
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

### Testing the Installation
```bash
# Run the test suite to verify everything works
python test_alarm.py
```

## Usage

### Setting an Alarm

1. **Enter Time**: Type the alarm time in HH:MM format (e.g., 07:30)
2. **Choose Sound**: Select "Default" for system sound or "Custom File" to browse for your own audio file
3. **Add Alarm**: Click "Add Alarm" to set the alarm

### Managing Alarms

- **View Alarms**: All active alarms are displayed in the "Active Alarms" section
- **Remove Alarms**: 
  - Select an alarm and click "🗑️ Remove Selected"
  - Right-click on an alarm for context menu options
  - Use "🗑️ Clear All" to remove all alarms at once
- **Edit Alarms**: Right-click on an alarm and select "📝 Edit Alarm" to change the time
- **Test Alarms**: Use "🔔 Test Alarm" or right-click "🔔 Test This Alarm" to test functionality
- **Alarm Status**: Alarms show their current status (Active, Ringing, etc.)

### When Alarm Goes Off

- **Alarm Dialog**: A popup notification appears when the alarm time is reached
- **Visual Indicators**: The "Alarm Controls" section shows "🔔 ALARM RINGING!" in red
- **Stop Alarm**: Click "⏹️ Stop Alarm" to turn off the alarm completely
- **Snooze**: Click "⏰ Snooze" to delay the alarm for the specified duration

### Snooze Settings

- **Customize Duration**: Choose snooze duration from 1, 3, 5, 10, or 15 minutes
- **Quick Snooze**: Use the "Snooze" button during alarm to delay it

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- OGG (.ogg)
- M4A (.m4a)

## System Requirements

- Python 3.6 or higher
- Windows, macOS, or Linux
- Audio playback capability

## Dependencies

- **tkinter**: GUI framework (included with Python)
- **pygame**: Audio playback and mixing
- **datetime**: Time and date handling
- **threading**: Background audio processing

## File Structure

```
alarm-clock/
├── alarm_clock.py      # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

### Common Issues & Solutions

#### Audio Issues
- **No sound when alarm rings**: Ensure your system has audio drivers installed
- **Audio file not playing**: Check that the audio file format is supported (MP3, WAV, OGG, M4A)
- **Sound continues after stopping**: This has been fixed in the latest version
- **Try using a different audio file** if playback fails

#### GUI Issues
- **Tkinter not found**: Make sure tkinter is available (usually included with Python)
- **On Linux**: Install tkinter separately:
  ```bash
  sudo apt-get install python3-tk  # Ubuntu/Debian
  sudo dnf install python3-tkinter # Fedora
  ```

#### Python/Dependency Issues
- **Module not found errors**: Run `pip install -r requirements.txt`
- **Permission errors**: Use a virtual environment or run with appropriate permissions
- **Python version issues**: Ensure you're using Python 3.6 or higher

#### Running Issues
- **Command not found**: Make sure Python is in your PATH
- **Script not executable** (Linux/macOS): Run `chmod +x run_alarm_clock.sh`
- **Batch file not working** (Windows): Right-click and "Run as administrator"

### Getting Help
If you encounter issues:
1. Run the test suite: `python test_alarm.py`
2. Check Python version: `python --version`
3. Verify dependencies: `pip list | grep -E "(pygame|numpy|scipy)"`

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## License

This project is open source and available under the MIT License.

## Version History

- **v1.0.0**: Initial release with basic alarm functionality
  - Real-time clock display
  - Multiple alarm support
  - Custom audio files
  - Snooze functionality
  - Modern GUI interface 