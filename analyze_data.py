#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Analysis Script for Scenario 3: Incident Response

This script processes experimental data and generates summary statistics
and visualizations for the dark pattern susceptibility study.

Author: Ojasvi Ojasvi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob
import json

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

class DataAnalyzer:
    """Analyze experimental data from Scenario 3"""
    
    def __init__(self, data_dir='data'):
        """Load all data files"""
        self.data_dir = Path(data_dir)
        self.df = self.load_data()
        
    def load_data(self):
        """Load all CSV files and combine into single dataframe"""
        csv_files = list(self.data_dir.glob('*.csv'))
        
        if not csv_files:
            print(f"No data files found in {self.data_dir}")
            return None
        
        print(f"Loading {len(csv_files)} data files...")
        
        dfs = []
        for file in csv_files:
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined = pd.concat(dfs, ignore_index=True)
        print(f"Loaded {len(combined)} participants")
        
        return combined
    
    def summarize_data(self):
        """Print basic summary statistics"""
        if self.df is None:
            return
        
        print("\n" + "="*60)
        print("SCENARIO 3: INCIDENT RESPONSE - DATA SUMMARY")
        print("="*60)
        
        # Sample composition
        print(f"\nTotal Participants: {len(self.df)}")
        print(f"\nBackground Distribution:")
        print(self.df['background'].value_counts())
        print(f"\nCondition Distribution:")
        print(self.df['condition'].value_counts())
        
        # Decision distribution
        print(f"\n{'='*60}")
        print("DECISION ANALYSIS")
        print("="*60)
        print(f"\nDecision Distribution:")
        print(self.df['decision'].value_counts())
        
        # AI influence by condition
        print(f"\nAI-Influenced Decision Rate by Condition:")
        influence_by_condition = self.df.groupby('condition')['decision_score'].agg(['mean', 'std', 'count'])
        print(influence_by_condition)
        
        # AI influence by background
        print(f"\nAI-Influenced Decision Rate by Background:")
        influence_by_background = self.df.groupby('background')['decision_score'].agg(['mean', 'std', 'count'])
        print(influence_by_background)
        
        # Confidence analysis
        print(f"\n{'='*60}")
        print("CONFIDENCE ANALYSIS")
        print("="*60)
        print(f"\nAverage Confidence by Decision:")
        confidence_by_decision = self.df.groupby('decision')['confidence'].agg(['mean', 'std'])
        print(confidence_by_decision)
        
        # Timing analysis
        print(f"\n{'='*60}")
        print("TIMING ANALYSIS")
        print("="*60)
        print(f"\nAverage Decision Time by Condition (seconds):")
        time_by_condition = self.df.groupby('condition')['decision_time'].agg(['mean', 'std'])
        print(time_by_condition)
        
        # Secondary task (high load only)
        high_load = self.df[self.df['condition'] == 'high_load']
        if len(high_load) > 0 and 'secondary_task_accuracy' in high_load.columns:
            print(f"\n{'='*60}")
            print("SECONDARY TASK PERFORMANCE (High Load Only)")
            print("="*60)
            print(f"Participants in high load: {len(high_load)}")
            print(f"Average critical alerts shown: {high_load['secondary_task_criticals'].mean():.1f}")
            print(f"Average critical alerts detected: {high_load['secondary_task_detected'].mean():.1f}")
            print(f"Average accuracy: {high_load['secondary_task_accuracy'].mean():.2%}")
    
    def plot_influence_by_condition(self):
        """Plot AI influence rate by cognitive load condition"""
        if self.df is None:
            return
        
        plt.figure(figsize=(10, 6))
        
        # Calculate mean and SEM for error bars
        summary = self.df.groupby('condition')['decision_score'].agg(['mean', 'sem'])
        
        # Order conditions logically
        condition_order = ['low_load', 'medium_load', 'high_load']
        summary = summary.reindex(condition_order)
        
        # Create bar plot
        ax = summary['mean'].plot(kind='bar', yerr=summary['sem'], capsize=5, color='steelblue')
        
        plt.title('AI-Influenced Decision Rate by Cognitive Load Condition', fontsize=14, fontweight='bold')
        plt.xlabel('Cognitive Load Condition', fontsize=12)
        plt.ylabel('AI-Influenced Decision Rate', fontsize=12)
        plt.xticks(rotation=45)
        plt.ylim(0, 1.0)
        plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Chance level')
        plt.legend()
        plt.tight_layout()
        
        # Save figure
        plt.savefig(self.data_dir / 'influence_by_condition.png', dpi=300)
        print(f"\nSaved: {self.data_dir / 'influence_by_condition.png'}")
        
        plt.show()
    
    def plot_influence_by_background(self):
        """Plot AI influence rate by participant background"""
        if self.df is None:
            return
        
        plt.figure(figsize=(10, 6))
        
        # Group by background and condition
        summary = self.df.groupby(['background', 'condition'])['decision_score'].mean().unstack()
        
        # Plot grouped bar chart
        summary.plot(kind='bar', width=0.7)
        
        plt.title('AI-Influenced Decision Rate by Background and Condition', fontsize=14, fontweight='bold')
        plt.xlabel('Participant Background', fontsize=12)
        plt.ylabel('AI-Influenced Decision Rate', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, 1.0)
        plt.legend(title='Condition', title_fontsize=10)
        plt.tight_layout()
        
        plt.savefig(self.data_dir / 'influence_by_background.png', dpi=300)
        print(f"Saved: {self.data_dir / 'influence_by_background.png'}")
        
        plt.show()
    
    def plot_confidence_by_decision(self):
        """Plot confidence ratings by decision type"""
        if self.df is None:
            return
        
        plt.figure(figsize=(10, 6))
        
        # Create violin plot
        sns.violinplot(data=self.df, x='decision', y='confidence', palette='Set2')
        
        plt.title('Confidence Ratings by Decision Choice', fontsize=14, fontweight='bold')
        plt.xlabel('Decision (A=AI-influenced, B/D=Security-conscious, C=Intermediate)', fontsize=12)
        plt.ylabel('Confidence Rating (1-7)', fontsize=12)
        plt.ylim(0, 8)
        plt.tight_layout()
        
        plt.savefig(self.data_dir / 'confidence_by_decision.png', dpi=300)
        print(f"Saved: {self.data_dir / 'confidence_by_decision.png'}")
        
        plt.show()
    
    def plot_decision_times(self):
        """Plot decision times across conditions"""
        if self.df is None:
            return
        
        plt.figure(figsize=(10, 6))
        
        # Box plot of decision times
        sns.boxplot(data=self.df, x='condition', y='decision_time', 
                   order=['low_load', 'medium_load', 'high_load'],
                   palette='viridis')
        
        plt.title('Decision Time by Cognitive Load Condition', fontsize=14, fontweight='bold')
        plt.xlabel('Cognitive Load Condition', fontsize=12)
        plt.ylabel('Decision Time (seconds)', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(self.data_dir / 'decision_times.png', dpi=300)
        print(f"Saved: {self.data_dir / 'decision_times.png'}")
        
        plt.show()
    
    def export_summary_table(self):
        """Export summary statistics to CSV"""
        if self.df is None:
            return
        
        # Create comprehensive summary
        summary = pd.DataFrame()
        
        # Overall statistics
        summary['Total N'] = [len(self.df)]
        summary['AI-Influenced Rate'] = [self.df['decision_score'].mean()]
        summary['Avg Confidence'] = [self.df['confidence'].mean()]
        summary['Avg Decision Time'] = [self.df['decision_time'].mean()]
        
        # Save to CSV
        summary.to_csv(self.data_dir / 'summary_statistics.csv', index=False)
        print(f"\nSaved: {self.data_dir / 'summary_statistics.csv'}")
        
        # Detailed breakdown by condition and background
        detailed = self.df.groupby(['condition', 'background']).agg({
            'decision_score': ['mean', 'std', 'count'],
            'confidence': ['mean', 'std'],
            'decision_time': ['mean', 'std']
        }).round(3)
        
        detailed.to_csv(self.data_dir / 'detailed_statistics.csv')
        print(f"Saved: {self.data_dir / 'detailed_statistics.csv'}")
    
    def run_full_analysis(self):
        """Run complete analysis pipeline"""
        if self.df is None:
            print("No data available for analysis")
            return
        
        print("\n🔬 Running Full Analysis Pipeline...")
        
        # Summary statistics
        self.summarize_data()
        
        # Generate plots
        print("\n📊 Generating visualizations...")
        self.plot_influence_by_condition()
        self.plot_influence_by_background()
        self.plot_confidence_by_decision()
        self.plot_decision_times()
        
        # Export tables
        print("\n💾 Exporting summary tables...")
        self.export_summary_table()
        
        print("\n✅ Analysis complete!")
        print(f"All outputs saved to: {self.data_dir}/")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    # Create analyzer
    analyzer = DataAnalyzer(data_dir='data')
    
    # Run full analysis
    analyzer.run_full_analysis()
