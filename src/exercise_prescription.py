"""
Exercise prescription and routine management
"""
import streamlit as st
from typing import Dict, List
import json
from datetime import datetime, timedelta

class ExercisePrescription:
    def __init__(self):
        self.prescriptions = {
            'beginner': {
                'name': 'Beginner Cervical Routine',
                'duration_weeks': 2,
                'exercises': [
                    {
                        'name': 'Chin Tuck (Retract chin)',
                        'sets': 3,
                        'reps': 10,
                        'hold_time': 5,
                        'rest_between_sets': 30,
                        'frequency_per_week': 5
                    },
                    {
                        'name': 'Cervical Flexion (Chin-to-chest)',
                        'sets': 2,
                        'reps': 8,
                        'hold_time': 3,
                        'rest_between_sets': 30,
                        'frequency_per_week': 4
                    }
                ]
            },
            'intermediate': {
                'name': 'Intermediate Cervical Routine',
                'duration_weeks': 4,
                'exercises': [
                    {
                        'name': 'Chin Tuck (Retract chin)',
                        'sets': 4,
                        'reps': 12,
                        'hold_time': 7,
                        'rest_between_sets': 30,
                        'frequency_per_week': 6
                    },
                    {
                        'name': 'Cervical Flexion (Chin-to-chest)',
                        'sets': 3,
                        'reps': 10,
                        'hold_time': 5,
                        'rest_between_sets': 30,
                        'frequency_per_week': 5
                    },
                    {
                        'name': 'Cervical Extension (Look upward)',
                        'sets': 3,
                        'reps': 8,
                        'hold_time': 4,
                        'rest_between_sets': 30,
                        'frequency_per_week': 4
                    },
                    {
                        'name': 'Lateral Neck Tilt (Left and Right)',
                        'sets': 2,
                        'reps': 6,
                        'hold_time': 4,
                        'rest_between_sets': 30,
                        'frequency_per_week': 4
                    }
                ]
            }
        }
    
    def get_prescription(self, level: str) -> Dict:
        """Get exercise prescription for given level"""
        return self.prescriptions.get(level, self.prescriptions['beginner'])
    
    def create_weekly_schedule(self, prescription: Dict) -> Dict:
        """Create a weekly exercise schedule"""
        schedule = {day: [] for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
        
        days = list(schedule.keys())
        
        for exercise in prescription['exercises']:
            freq = exercise['frequency_per_week']
            # Distribute exercises across the week
            selected_days = days[:freq]
            
            for day in selected_days:
                schedule[day].append({
                    'exercise': exercise['name'],
                    'sets': exercise['sets'],
                    'reps': exercise['reps'],
                    'hold_time': exercise['hold_time'],
                    'rest': exercise['rest_between_sets']
                })
        
        return schedule