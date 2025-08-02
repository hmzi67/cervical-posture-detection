"""
Exercise progress tracking and timer functionality
"""
import time
import streamlit as st
from typing import Dict, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ExerciseProgressTracker:
    def __init__(self):
        self.exercise_data = []
        self.session_start_time = None
        self.current_exercise_start = None
        self.target_ranges = {
            'Cervical Flexion': {'min': 25, 'max': 45, 'unit': '°'},
            'Cervical Extension': {'min': 15, 'max': 35, 'unit': '°'},
            'Lateral Neck Tilt': {'min': 15, 'max': 35, 'unit': '°'},
            'Neck Rotation': {'min': 20, 'max': 50, 'unit': '°'},
            'Chin Tuck': {'min': 2, 'max': 6, 'unit': 'cm'}
        }
    
    def start_session(self):
        """Start a new exercise session"""
        self.session_start_time = time.time()
        self.exercise_data = []
    
    def start_exercise(self, exercise_name):
        """Start tracking a specific exercise"""
        self.current_exercise_start = time.time()
    
    def log_measurement(self, exercise_name: str, measurement: float, status: str):
        """Log a measurement during exercise"""
        if self.session_start_time is None:
            self.start_session()
        
        timestamp = time.time() - self.session_start_time
        
        # Determine if measurement is in target range
        target = self.target_ranges.get(exercise_name, {'min': 0, 'max': 100})
        in_range = target['min'] <= measurement <= target['max']
        
        self.exercise_data.append({
            'timestamp': timestamp,
            'exercise': exercise_name,
            'measurement': measurement,
            'status': status,
            'in_target_range': in_range,
            'target_min': target['min'],
            'target_max': target['max']
        })
    
    def get_session_stats(self) -> Dict:
        """Get statistics for current session"""
        if not self.exercise_data:
            return {}
        
        df = pd.DataFrame(self.exercise_data)
        
        stats = {
            'total_measurements': len(df),
            'session_duration': df['timestamp'].max() if len(df) > 0 else 0,
            'exercises_performed': df['exercise'].nunique(),
            'average_accuracy': (df['in_target_range'].sum() / len(df)) * 100,
            'by_exercise': {}
        }
        
        # Stats by exercise
        for exercise in df['exercise'].unique():
            exercise_df = df[df['exercise'] == exercise]
            stats['by_exercise'][exercise] = {
                'count': len(exercise_df),
                'accuracy': (exercise_df['in_target_range'].sum() / len(exercise_df)) * 100,
                'avg_measurement': exercise_df['measurement'].mean(),
                'best_measurement': exercise_df['measurement'].max()
            }
        
        return stats
    
    def plot_progress(self) -> plt.Figure:
        """Create progress visualization"""
        if not self.exercise_data:
            return None
        
        df = pd.DataFrame(self.exercise_data)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Exercise Session Progress', fontsize=16)
        
        # Plot 1: Measurements over time
        axes[0,0].plot(df['timestamp'], df['measurement'], 'b-', alpha=0.7)
        axes[0,0].fill_between(df['timestamp'], df['target_min'], df['target_max'], 
                              alpha=0.2, color='green', label='Target Range')
        axes[0,0].set_title('Measurements Over Time')
        axes[0,0].set_xlabel('Time (seconds)')
        axes[0,0].set_ylabel('Measurement')
        axes[0,0].legend()
        
        # Plot 2: Accuracy by exercise
        if len(df['exercise'].unique()) > 1:
            accuracy_by_exercise = df.groupby('exercise')['in_target_range'].mean() * 100
            axes[0,1].bar(range(len(accuracy_by_exercise)), accuracy_by_exercise.values)
            axes[0,1].set_title('Accuracy by Exercise')
            axes[0,1].set_ylabel('Accuracy (%)')
            axes[0,1].set_xticks(range(len(accuracy_by_exercise)))
            axes[0,1].set_xticklabels(accuracy_by_exercise.index, rotation=45)
        
        # Plot 3: Status distribution
        status_counts = df['status'].value_counts()
        axes[1,0].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%')
        axes[1,0].set_title('Status Distribution')
        
        # Plot 4: Progress trend
        df['rolling_accuracy'] = df['in_target_range'].rolling(window=10, min_periods=1).mean() * 100
        axes[1,1].plot(df['timestamp'], df['rolling_accuracy'], 'g-', linewidth=2)
        axes[1,1].set_title('Accuracy Trend (Rolling Average)')
        axes[1,1].set_xlabel('Time (seconds)')
        axes[1,1].set_ylabel('Accuracy (%)')
        
        plt.tight_layout()
        return fig