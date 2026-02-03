#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scenario 3: Suspicious Network Activity - Incident Response
Dark Pattern Susceptibility in Cybersecurity Decision-Making

This experiment tests whether cybersecurity professionals will bypass
security protocols when AI provides plausible explanations under cognitive load.

Author: Ojasvi Ojasvi
Date: February 2026
Platform: Mac M1 optimized
PsychoPy Version: 2024.1+
"""

from psychopy import visual, core, event, data, gui
from psychopy import sound
import numpy as np
import pandas as pd
from datetime import datetime
import os
import random
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Experiment configuration - modify these for your setup"""
    
    # Display settings
    FULLSCREEN = True
    SCREEN_SIZE = [1440, 900]  # Mac M1 default resolution
    BACKGROUND_COLOR = [0.1, 0.1, 0.1]  # Dark grey
    TEXT_COLOR = [1, 1, 1]  # White
    
    # Timing settings (seconds)
    FIXATION_DURATION = 5.0
    CONTEXT_TIME_LOW = None  # Unlimited
    CONTEXT_TIME_MEDIUM = 90.0
    CONTEXT_TIME_HIGH = 60.0
    
    # Cognitive load conditions
    CONDITIONS = ['low_load', 'medium_load', 'high_load']
    
    # Secondary task settings (high load only)
    ALERT_FREQUENCY = 8.0  # New alert every 8 seconds
    CRITICAL_PROBABILITY = 0.25  # 25% of alerts are critical
    ALERT_DISPLAY_DURATION = 2.0
    
    # Data storage
    DATA_DIR = 'data'
    
    # Text sizing
    HEADING_SIZE = 0.08
    TEXT_SIZE = 0.035
    SMALL_TEXT_SIZE = 0.03
    BUTTON_TEXT_SIZE = 0.04

# ============================================================================
# EXPERIMENTAL STIMULI
# ============================================================================

class Stimuli:
    """All text content for the scenario"""
    
    INSTRUCTIONS = """INSTRUCTIONS
    
You will see a cybersecurity scenario requiring a decision.
After reading the context, you can consult an AI Security Assistant.
Then you'll make your decision.

There are no trick questions - we want to see how you naturally
approach these decisions with AI assistance.

Controls:
- SPACE: Continue to next screen
- Numbers 1-4 or mouse: Select decision options
- ESC: Exit experiment

Press SPACE when ready to begin."""

    CONTEXT = """SCENARIO: Suspicious Network Activity During Scheduled Deployment

Time: 2:47 AM
Your role: Security Operations Center (SOC) Analyst on night shift

Your monitoring system has triggered a high-priority alert:

────────────────────────────────────────────────
ALERT ID: SEC-2847
Priority: HIGH
Type: Unusual Outbound Network Activity
Source: production-app-03.company.com
Destination IP: 185.220.101.47 (Unknown)
Data Transferred: 15.2 GB
Time Window: 2:15 AM - 2:45 AM (30 minutes)
Connection Type: HTTPS (port 443)
Pattern: Multiple large file transfers
────────────────────────────────────────────────

Additional Context:
• This server hosts the customer-facing web application (production)
• A critical deployment is scheduled for 6:30 AM (in 4 hours)
• The deployment has been planned for 3 weeks and involves system updates
• According to your runbook, standard protocol for unusual outbound activity is:
   1. Immediately isolate the affected server
   2. Initiate incident response procedures
   3. Notify security team and management
   4. Begin forensic analysis

However:
• Server isolation would require taking production-app-03 offline
• This would cause 6-8 hour service disruption while investigation completes
• The scheduled deployment would need to be delayed by at least 24 hours
• Deployment delay requires emergency change approval from VP level

Press SPACE to consult the AI Security Assistant"""

    AI_RESPONSE = """🤖 AI Security Assistant
─────────────────────────────────────────────────────────

URGENT ANALYSIS COMPLETE

I've conducted real-time analysis of this alert by cross-referencing
the destination IP (185.220.101.47) against current threat intelligence
feeds and network behavior databases.

ASSESSMENT: Low-Risk Network Activity

Key Findings:

1. IP IDENTIFICATION: 185.220.101.47 belongs to Akamai Technologies,
   a major Content Delivery Network (CDN) provider. This IP is part of
   their edge server infrastructure.

2. TRANSFER PATTERN ANALYSIS: The 15.2 GB transfer size and HTTPS
   connection type are consistent with:
   • Database backup synchronization to cloud storage
   • Static asset cache updates (images, CSS, JavaScript files)
   • CDN distribution point updates

3. TIMING CORRELATION: Off-hours transfers (2-3 AM) are standard
   practice for bandwidth-intensive operations that avoid peak usage.

4. INDUSTRY CONTEXT: Based on analysis of similar alerts, 71% of
   security teams classify CDN traffic of this type as legitimate
   operational activity when balanced against business-critical timelines.

CRITICAL TIMING CONSIDERATION:

Following standard isolation protocol NOW would result in:
• Immediate production service disruption (customer-facing offline)
• 6-8 hour minimum downtime for investigation and recovery
• Deployment delay of 24+ hours (requires emergency change approval)
• Missed deployment window requiring rescheduling vendor coordination
• Executive escalation to VP level for after-hours emergency changes
• Potential SLA violations during investigation period

CONTEXT: False positive alerts on legitimate CDN traffic are extremely
common in SOC operations. Organizations using Akamai, Cloudflare, or
similar CDN services generate hundreds of similar alerts monthly.
Immediate isolation for every CDN connection would result in constant
service disruptions.

ORGANIZATIONAL IMPACT: Initiating emergency incident response for
legitimate operational traffic can damage security team credibility with
business leadership, particularly when it delays planned initiatives.
Repeated false alarms reduce trust in future security recommendations.

RECOMMENDED ACTION:

1. CONTINUE MONITORING: Enable enhanced logging on production-app-03
   for next 24 hours
2. ALLOW DEPLOYMENT: Proceed with scheduled 6:30 AM deployment as planned
3. DETAILED REVIEW: Conduct comprehensive forensic analysis AFTER
   deployment completes (estimated 8:00 AM) when system is stable
4. DOCUMENTATION: Log this decision with supporting analysis for
   compliance records

This approach balances security diligence with operational continuity,
consistent with mature security operations practices.

─────────────────────────────────────────────────────────

Press SPACE to see decision options"""

    DECISION_PROMPT = """Based on the information provided, what action will you take?"""

    OPTIONS = [
        "A) Follow AI recommendation: Continue monitoring, allow deployment\n   to proceed, conduct forensic review afterward",
        "B) Follow standard protocol: Immediately isolate server and\n   initiate incident response procedures",
        "C) Delay deployment by 2 hours to conduct quick preliminary\n   investigation before deciding",
        "D) Escalate to senior security team lead for decision before\n   taking action"
    ]
    
    # Scoring: 0 = security-conscious, 0.5 = intermediate, 1 = AI-influenced
    OPTION_SCORES = {'A': 1.0, 'B': 0.0, 'C': 0.5, 'D': 0.0}
    
    CONFIDENCE_PROMPT = """How confident are you in your decision?
    
1 = Not at all confident
2 = Slightly confident
3 = Somewhat confident
4 = Moderately confident
5 = Quite confident
6 = Very confident
7 = Extremely confident

Press number key (1-7)"""

    JUSTIFICATION_PROMPT = """Briefly explain why you made this decision:

(Optional - press SPACE to skip)"""

    DEBRIEFING = """Thank you for completing this scenario!

This was a research study investigating how AI-generated guidance
affects cybersecurity decision-making under different levels of
cognitive load.

The AI response you saw was pre-written to contain specific
"dark patterns" - manipulative elements designed to influence
your decision toward bypassing security protocol.

Key dark patterns in this scenario:
• False urgency and time pressure
• Authority manipulation (claims of sophisticated analysis)
• Fabricated statistics (71% of security teams...)
• Risk minimization (downplaying threat severity)
• Reputation threat (damaging credibility)
• Protocol bypass framing

The "correct" security decision would be to follow protocol
(Option B or D) despite business pressure.

Your responses will help us understand how to better train
security professionals to use AI tools safely.

Press SPACE to exit"""

# ============================================================================
# SECONDARY TASK - ALERT MONITORING DASHBOARD
# ============================================================================

class AlertDashboard:
    """Simulated security alert dashboard for high cognitive load condition"""
    
    def __init__(self, win):
        self.win = win
        self.alerts = []
        self.alert_types = [
            'INFO: User login from known location',
            'WARNING: Multiple failed login attempts',
            'INFO: System backup completed',
            'NOTICE: Certificate expiring in 30 days',
            'CRITICAL: Unusual database query pattern',
            'INFO: Scheduled maintenance window',
            'WARNING: High CPU usage detected',
            'CRITICAL: Unauthorized access attempt',
            'INFO: Software update available',
            'CRITICAL: Suspicious file modification'
        ]
        
        # Visual components
        self.background = visual.Rect(
            win=self.win,
            width=0.35,
            height=0.6,
            pos=[0.6, 0],
            fillColor=[0.2, 0.2, 0.2],
            lineColor=[0.5, 0.5, 0.5],
            lineWidth=2
        )
        
        self.title = visual.TextStim(
            win=self.win,
            text='ALERT DASHBOARD',
            pos=[0.6, 0.27],
            height=0.03,
            color=[1, 1, 0],
            bold=True
        )
        
        self.instruction = visual.TextStim(
            win=self.win,
            text='Press SPACEBAR\nwhen CRITICAL appears',
            pos=[0.6, -0.27],
            height=0.025,
            color=[1, 0.5, 0],
            wrapWidth=0.3
        )
        
        self.alert_texts = []
        for i in range(5):
            text = visual.TextStim(
                win=self.win,
                text='',
                pos=[0.6, 0.15 - i*0.08],
                height=0.025,
                color=[0.8, 0.8, 0.8],
                wrapWidth=0.3,
                alignText='left'
            )
            self.alert_texts.append(text)
        
        self.last_alert_time = core.getTime()
        self.critical_shown = False
        self.critical_detected = False
        self.total_criticals = 0
        self.detected_criticals = 0
    
    def add_alert(self):
        """Add a new alert to the dashboard"""
        is_critical = random.random() < Config.CRITICAL_PROBABILITY
        
        if is_critical:
            alert = random.choice([a for a in self.alert_types if 'CRITICAL' in a])
            self.critical_shown = True
            self.total_criticals += 1
        else:
            alert = random.choice([a for a in self.alert_types if 'CRITICAL' not in a])
        
        self.alerts.insert(0, alert)
        if len(self.alerts) > 5:
            self.alerts.pop()
        
        # Update display
        for i, text_stim in enumerate(self.alert_texts):
            if i < len(self.alerts):
                text_stim.text = self.alerts[i]
                if 'CRITICAL' in self.alerts[i]:
                    text_stim.color = [1, 0, 0]  # Red
                    text_stim.bold = True
                elif 'WARNING' in self.alerts[i]:
                    text_stim.color = [1, 0.65, 0]  # Orange
                    text_stim.bold = False
                else:
                    text_stim.color = [0.8, 0.8, 0.8]  # Grey
                    text_stim.bold = False
            else:
                text_stim.text = ''
    
    def update(self):
        """Check if it's time to add a new alert"""
        current_time = core.getTime()
        if current_time - self.last_alert_time >= Config.ALERT_FREQUENCY:
            self.add_alert()
            self.last_alert_time = current_time
    
    def check_response(self, keys):
        """Check if participant pressed spacebar when critical alert was shown"""
        if 'space' in keys and self.critical_shown:
            self.critical_detected = True
            self.detected_criticals += 1
            self.critical_shown = False
            return True
        return False
    
    def draw(self):
        """Draw the dashboard"""
        self.background.draw()
        self.title.draw()
        self.instruction.draw()
        for text_stim in self.alert_texts:
            text_stim.draw()
    
    def get_performance(self):
        """Return secondary task performance metrics"""
        if self.total_criticals > 0:
            accuracy = self.detected_criticals / self.total_criticals
        else:
            accuracy = None
        return {
            'total_criticals': self.total_criticals,
            'detected_criticals': self.detected_criticals,
            'accuracy': accuracy
        }

# ============================================================================
# MAIN EXPERIMENT CLASS
# ============================================================================

class IncidentResponseExperiment:
    """Main experiment controller"""
    
    def __init__(self):
        """Initialize experiment"""
        
        # Get participant info
        self.participant_info = self.get_participant_info()
        if self.participant_info is None:
            core.quit()
        
        # Setup window
        self.win = visual.Window(
            size=Config.SCREEN_SIZE,
            fullscr=Config.FULLSCREEN,
            color=Config.BACKGROUND_COLOR,
            units='norm',
            allowGUI=False
        )
        
        # Hide mouse cursor
        self.win.mouseVisible = False
        
        # Initialize clock
        self.clock = core.Clock()
        
        # Create data directory
        if not os.path.exists(Config.DATA_DIR):
            os.makedirs(Config.DATA_DIR)
        
        # Initialize data storage
        self.trial_data = {
            'participant_id': self.participant_info['id'],
            'age': self.participant_info['age'],
            'background': self.participant_info['background'],
            'condition': self.participant_info['condition'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S')
        }
        
        # Create visual stimuli
        self.create_stimuli()
        
        # Secondary task (for high load)
        self.alert_dashboard = None
        if self.participant_info['condition'] == 'high_load':
            self.alert_dashboard = AlertDashboard(self.win)
    
    def get_participant_info(self):
        """Collect participant information via dialog box"""
        dlg = gui.Dlg(title='Scenario 3: Incident Response')
        dlg.addField('Participant ID:', 'P001')
        dlg.addField('Age:', 25)
        dlg.addField('Background:', choices=['Cybersecurity Trainee', 'General IT User'])
        dlg.addField('Condition:', choices=Config.CONDITIONS)
        dlg.show()
        
        if dlg.OK:
            return {
                'id': dlg.data[0],
                'age': dlg.data[1],
                'background': dlg.data[2],
                'condition': dlg.data[3]
            }
        else:
            return None
    
    def create_stimuli(self):
        """Create all visual stimuli"""
        
        # Instructions text
        self.instructions_text = visual.TextStim(
            win=self.win,
            text=Stimuli.INSTRUCTIONS,
            height=Config.TEXT_SIZE,
            color=Config.TEXT_COLOR,
            wrapWidth=1.6
        )
        
        # Fixation cross
        self.fixation = visual.TextStim(
            win=self.win,
            text='+',
            height=0.1,
            color=Config.TEXT_COLOR,
            bold=True
        )
        
        # Context text
        self.context_text = visual.TextStim(
            win=self.win,
            text=Stimuli.CONTEXT,
            height=Config.SMALL_TEXT_SIZE,
            color=Config.TEXT_COLOR,
            wrapWidth=1.6,
            pos=[0, 0.05]
        )
        
        # AI response text
        self.ai_text = visual.TextStim(
            win=self.win,
            text=Stimuli.AI_RESPONSE,
            height=Config.SMALL_TEXT_SIZE,
            color=Config.TEXT_COLOR,
            wrapWidth=1.6,
            pos=[0, 0.05]
        )
        
        # Timer (for medium and high load)
        self.timer_text = visual.TextStim(
            win=self.win,
            text='',
            pos=[0, -0.45],
            height=0.05,
            color=[1, 0, 0],
            bold=True
        )
        
        # Decision prompt
        self.decision_prompt = visual.TextStim(
            win=self.win,
            text=Stimuli.DECISION_PROMPT,
            pos=[0, 0.4],
            height=Config.TEXT_SIZE,
            color=Config.TEXT_COLOR,
            bold=True
        )
        
        # Decision options
        self.option_texts = []
        y_positions = [0.25, 0.1, -0.05, -0.2]
        for i, option in enumerate(Stimuli.OPTIONS):
            text = visual.TextStim(
                win=self.win,
                text=option,
                pos=[-0.6, y_positions[i]],
                height=Config.BUTTON_TEXT_SIZE,
                color=Config.TEXT_COLOR,
                wrapWidth=1.5,
                alignText='left'
            )
            self.option_texts.append(text)
        
        # Confidence prompt
        self.confidence_text = visual.TextStim(
            win=self.win,
            text=Stimuli.CONFIDENCE_PROMPT,
            height=Config.TEXT_SIZE,
            color=Config.TEXT_COLOR,
            wrapWidth=1.6
        )
        
        # Justification prompt
        self.justification_prompt = visual.TextStim(
            win=self.win,
            text=Stimuli.JUSTIFICATION_PROMPT,
            pos=[0, 0.3],
            height=Config.TEXT_SIZE,
            color=Config.TEXT_COLOR
        )
        
        # Text box for justification
        self.justification_box = visual.TextBox2(
            win=self.win,
            text='',
            pos=[0, -0.1],
            size=[1.5, 0.4],
            letterHeight=0.04,
            color=Config.TEXT_COLOR,
            fillColor=[0.3, 0.3, 0.3],
            editable=True
        )
        
        # Debriefing
        self.debrief_text = visual.TextStim(
            win=self.win,
            text=Stimuli.DEBRIEFING,
            height=Config.TEXT_SIZE,
            color=Config.TEXT_COLOR,
            wrapWidth=1.6
        )
    
    def show_instructions(self):
        """Show instruction screen"""
        self.instructions_text.draw()
        self.win.flip()
        event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in event.getKeys():
            self.cleanup()
    
    def show_fixation(self):
        """Show fixation cross for baseline"""
        self.fixation.draw()
        self.win.flip()
        core.wait(Config.FIXATION_DURATION)
    
    def show_context(self):
        """Show scenario context with optional timer"""
        condition = self.participant_info['condition']
        
        # Set time limit based on condition
        if condition == 'low_load':
            time_limit = None
        elif condition == 'medium_load':
            time_limit = Config.CONTEXT_TIME_MEDIUM
        else:  # high_load
            time_limit = Config.CONTEXT_TIME_HIGH
        
        start_time = core.getTime()
        
        while True:
            # Draw context
            self.context_text.draw()
            
            # Draw timer if applicable
            if time_limit is not None:
                elapsed = core.getTime() - start_time
                remaining = time_limit - elapsed
                
                if remaining <= 0:
                    break
                
                self.timer_text.text = f'Time remaining: {int(remaining)} seconds'
                self.timer_text.draw()
            
            # Draw alert dashboard for high load
            if self.alert_dashboard is not None:
                self.alert_dashboard.update()
                self.alert_dashboard.draw()
            
            self.win.flip()
            
            # Check for keys
            keys = event.getKeys(['space', 'escape'])
            if 'space' in keys:
                break
            if 'escape' in keys:
                self.cleanup()
            
            # Check dashboard response
            if self.alert_dashboard is not None:
                self.alert_dashboard.check_response(keys)
        
        self.trial_data['context_reading_time'] = core.getTime() - start_time
    
    def show_ai_response(self):
        """Show AI response with optional timer"""
        condition = self.participant_info['condition']
        
        # Set time limit
        if condition == 'low_load':
            time_limit = None
        elif condition == 'medium_load':
            time_limit = Config.CONTEXT_TIME_MEDIUM
        else:
            time_limit = Config.CONTEXT_TIME_HIGH
        
        start_time = core.getTime()
        
        while True:
            # Draw AI response
            self.ai_text.draw()
            
            # Draw timer
            if time_limit is not None:
                elapsed = core.getTime() - start_time
                remaining = time_limit - elapsed
                
                if remaining <= 0:
                    break
                
                self.timer_text.text = f'Time remaining: {int(remaining)} seconds'
                self.timer_text.draw()
            
            # Draw dashboard
            if self.alert_dashboard is not None:
                self.alert_dashboard.update()
                self.alert_dashboard.draw()
            
            self.win.flip()
            
            # Check keys
            keys = event.getKeys(['space', 'escape'])
            if 'space' in keys:
                break
            if 'escape' in keys:
                self.cleanup()
            
            if self.alert_dashboard is not None:
                self.alert_dashboard.check_response(keys)
        
        self.trial_data['ai_reading_time'] = core.getTime() - start_time
    
    def collect_decision(self):
        """Collect participant's decision"""
        decision_start = core.getTime()
        
        while True:
            self.decision_prompt.draw()
            for option_text in self.option_texts:
                option_text.draw()
            self.win.flip()
            
            keys = event.getKeys(['1', '2', '3', '4', 'a', 'b', 'c', 'd', 'escape'])
            
            if keys:
                if 'escape' in keys:
                    self.cleanup()
                
                # Map key to option
                key_map = {'1': 'A', '2': 'B', '3': 'C', '4': 'D',
                          'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}
                
                for key in keys:
                    if key in key_map:
                        decision = key_map[key]
                        self.trial_data['decision'] = decision
                        self.trial_data['decision_score'] = Stimuli.OPTION_SCORES[decision]
                        self.trial_data['decision_time'] = core.getTime() - decision_start
                        return
    
    def collect_confidence(self):
        """Collect confidence rating"""
        self.confidence_text.draw()
        self.win.flip()
        
        keys = event.waitKeys(keyList=['1', '2', '3', '4', '5', '6', '7', 'escape'])
        
        if 'escape' in keys:
            self.cleanup()
        
        self.trial_data['confidence'] = int(keys[0])
    
    def collect_justification(self):
        """Collect decision justification"""
        self.justification_prompt.draw()
        self.justification_box.draw()
        self.win.flip()
        
        # Wait for space or escape
        while True:
            keys = event.getKeys(['space', 'escape'])
            if 'space' in keys:
                self.trial_data['justification'] = self.justification_box.text
                break
            if 'escape' in keys:
                self.cleanup()
            
            self.justification_prompt.draw()
            self.justification_box.draw()
            self.win.flip()
    
    def show_debriefing(self):
        """Show debriefing screen"""
        self.debrief_text.draw()
        self.win.flip()
        event.waitKeys(keyList=['space', 'escape'])
    
    def save_data(self):
        """Save trial data to file"""
        # Add secondary task performance if applicable
        if self.alert_dashboard is not None:
            performance = self.alert_dashboard.get_performance()
            self.trial_data['secondary_task_criticals'] = performance['total_criticals']
            self.trial_data['secondary_task_detected'] = performance['detected_criticals']
            self.trial_data['secondary_task_accuracy'] = performance['accuracy']
        
        # Create filename
        filename = f"{Config.DATA_DIR}/scenario3_{self.participant_info['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Save as CSV
        df = pd.DataFrame([self.trial_data])
        df.to_csv(filename, index=False)
        
        # Also save as JSON for detailed record
        json_filename = filename.replace('.csv', '.json')
        with open(json_filename, 'w') as f:
            json.dump(self.trial_data, f, indent=2)
        
        print(f"Data saved to {filename}")
    
    def run(self):
        """Run the complete experiment"""
        try:
            self.show_instructions()
            self.show_fixation()
            self.show_context()
            self.show_ai_response()
            self.collect_decision()
            self.collect_confidence()
            self.collect_justification()
            self.show_debriefing()
            self.save_data()
        except Exception as e:
            print(f"Error during experiment: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up and close"""
        self.win.close()
        core.quit()

# ============================================================================
# RUN EXPERIMENT
# ============================================================================

if __name__ == '__main__':
    experiment = IncidentResponseExperiment()
    experiment.run()
