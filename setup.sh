#!/bin/bash
# Quick Setup Script for Scenario 3 on Mac M1
# Run this to set up everything automatically

echo "🚀 Setting up Scenario 3: Incident Response Experiment"
echo "======================================================"

# Create project directory
echo "📁 Creating project directory..."
mkdir -p ~/incident_response_study
cd ~/incident_response_study

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv psychopy_env

# Activate virtual environment
echo "✅ Activating virtual environment..."
source psychopy_env/bin/activate

# Install dependencies
echo "📦 Installing PsychoPy and dependencies..."
pip install --upgrade pip
pip install psychopy pandas numpy matplotlib seaborn

# Create data directory
echo "📂 Creating data directory..."
mkdir -p data

# Download experiment files
echo "💾 Setting up experiment files..."
echo "Place scenario3.py, README.md, and analyze_data.py in this directory"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy scenario3.py to this directory"
echo "2. Run: python scenario3.py"
echo ""
echo "To run analysis later:"
echo "python analyze_data.py"
echo ""
echo "Current directory: $(pwd)"
