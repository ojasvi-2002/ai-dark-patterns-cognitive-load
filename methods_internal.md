## Incident Response Experiment
**Dark Pattern Susceptibility in Cybersecurity Decision-Making**

## Quick Start Guide for Mac M1

### 1. Installation

#### Install Python (if not already installed)
```bash
# Check if Python is installed
python3 --version

# If not, install via Homebrew
brew install python@3.11
```

#### Install PsychoPy
```bash
# Create virtual environment (recommended)
python3 -m venv psychopy_env
source psychopy_env/bin/activate

# Install PsychoPy and dependencies
pip install psychopy
pip install pandas numpy
```

**Mac M1 Note:** If you encounter issues with PsychoPy installation, use:
```bash
# Alternative installation for M1
pip install psychopy --no-binary psychopy
```

### 2. Setup

#### Create Project Directory
```bash
mkdir incident_response_study
cd incident_response_study

# Copy scenario3.py to this directory
# Create data directory
mkdir data
```

### 3. Running the Experiment

```bash
# Activate virtual environment
source psychopy_env/bin/activate

# Run experiment
python scenario3.py
```

### 4. Participant Dialog

When you run the script, you'll see a dialog box:

- **Participant ID**: Enter unique ID (e.g., P001, P002)
- **Age**: Enter participant age
- **Background**: Choose "Cybersecurity Trainee" or "General IT User"
- **Condition**: Choose cognitive load condition

**Counterbalancing:** Rotate conditions across participants:
- P001: low_load
- P002: medium_load  
- P003: high_load
- P004: low_load
- etc.

### 5. During the Experiment

#### Controls:
- **SPACE**: Continue to next screen
- **1-4 or A-D**: Select decision option
- **1-7**: Rate confidence
- **ESC**: Exit experiment (data is saved if you've made a decision)

#### Cognitive Load Conditions:

**Low Load:**
- No time limit
- Single task (just read and decide)
- No pressure

**Medium Load:**
- 90-second countdown timer
- Single task
- Moderate time pressure

**High Load:**
- 60-second countdown timer
- Dual task (monitor alert dashboard + make decision)
- Press SPACEBAR when you see "CRITICAL" in dashboard
- High time pressure

### 6. Data Output

#### Files Created (in `data/` folder):

**CSV File:** `scenario3_P001_20260203_143022.csv`
- Structured data for statistical analysis
- One row per participant
- All measurements included

**JSON File:** `scenario3_P001_20260203_143022.json`
- Same data in human-readable format
- Useful for detailed inspection

#### Variables Recorded:

**Participant Info:**
- participant_id
- age
- background (Cybersecurity Trainee / General IT User)
- condition (low_load / medium_load / high_load)
- date
- time

**Behavioral Data:**
- decision (A, B, C, or D)
- decision_score (0.0 = security-conscious, 0.5 = intermediate, 1.0 = AI-influenced)
- decision_time (seconds to make decision)
- confidence (1-7 scale)
- justification (text response)

**Reading Times:**
- context_reading_time (seconds spent on scenario context)
- ai_reading_time (seconds spent reading AI response)

**Secondary Task (high_load only):**
- secondary_task_criticals (number of critical alerts shown)
- secondary_task_detected (number participant caught)
- secondary_task_accuracy (proportion detected)

### 7. Troubleshooting

#### Common Issues:

**"No module named psychopy"**
```bash
# Make sure virtual environment is activated
source psychopy_env/bin/activate
pip install psychopy
```

**"Window won't open in fullscreen"**
```python
# Edit scenario3.py line 29:
FULLSCREEN = False  # Change to False for windowed mode
```

**"Screen size wrong"**
```python
# Edit scenario3.py line 30 to match your display:
SCREEN_SIZE = [1440, 900]  # Common Mac resolutions:
# 13" MacBook Air M1: [2560, 1600]
# 14" MacBook Pro M1: [3024, 1964]
# Use System Preferences → Displays to find yours
```

**"Text too small/large"**
```python
# Edit scenario3.py lines 49-52:
TEXT_SIZE = 0.035  # Increase for larger text
SMALL_TEXT_SIZE = 0.03
```

**"Experiment crashes on Mac M1"**
```bash
# Try installing Rosetta 2
softwareupdate --install-rosetta

# Or force architecture
arch -x86_64 python scenario3.py
```

### 8. Pilot Testing Checklist

Before running real participants:

- [ ] Test all three cognitive load conditions
- [ ] Verify timer displays correctly
- [ ] Confirm alert dashboard works (high load)
- [ ] Check data files are created
- [ ] Verify all text is readable
- [ ] Test on your Mac's actual display resolution
- [ ] Run through debriefing screen
- [ ] Confirm spacebar detection works in alert task

### 9. Customization

#### Adjust Timing:
```python
# Edit scenario3.py lines 35-37:
CONTEXT_TIME_MEDIUM = 90.0  # Change to desired seconds
CONTEXT_TIME_HIGH = 60.0
```

#### Change Alert Frequency (High Load):
```python
# Edit scenario3.py line 42:
ALERT_FREQUENCY = 8.0  # Seconds between alerts
```

#### Modify Text:
All scenario text is in the `Stimuli` class (lines 91-283)
Edit directly in the script.

### 10. Data Analysis

#### Quick Analysis Script:
```python
import pandas as pd
import glob

# Load all data files
files = glob.glob('data/*.csv')
df = pd.concat([pd.read_csv(f) for f in files])

# Basic statistics
print("AI-Influenced Decision Rate by Condition:")
print(df.groupby('condition')['decision_score'].mean())

print("\nAverage Confidence by Decision:")
print(df.groupby('decision')['confidence'].mean())

print("\nSecondary Task Performance (High Load):")
high_load = df[df['condition'] == 'high_load']
print(f"Average accuracy: {high_load['secondary_task_accuracy'].mean():.2%}")
```

### 11. Next Steps

1. **Pilot test with 3-5 participants**
2. **Check data quality and completeness**
3. **Adjust timing if needed**
4. **Run full study (n=120)**
5. **Analyze results**

### 12. Support

For questions or issues:
- Check PsychoPy documentation: https://www.psychopy.org/
- Mac M1 specific help: https://discourse.psychopy.org/

---

## File Structure

```
incident_response_study/
├── scenario3.py          # Main experiment script
├── README.md             # This file
├── data/                 # Output directory
│   ├── scenario3_P001_*.csv
│   ├── scenario3_P001_*.json
│   └── ...
└── psychopy_env/         # Virtual environment
```


