"""
Audio feedback system for exercise guidance
"""
import pyttsx3
import threading
import time
from typing import Dict

class AudioFeedbackSystem:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.8)  # Volume level
            self.is_enabled = True
            self.last_feedback_time = 0
            self.feedback_interval = 3  # Minimum seconds between feedbacks
        except:
            self.engine = None
            self.is_enabled = False
    
    def speak(self, text: str):
        """Speak the given text"""
        if not self.is_enabled or self.engine is None:
            return
        
        current_time = time.time()
        if current_time - self.last_feedback_time < self.feedback_interval:
            return
        
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
        
        # Run in separate thread to avoid blocking
        thread = threading.Thread(target=_speak)
        thread.daemon = True
        thread.start()
        
        self.last_feedback_time = current_time
    
    def provide_exercise_feedback(self, analysis: Dict):
        """Provide audio feedback based on exercise analysis"""
        if not self.is_enabled:
            return
        
        status = analysis.get('status', '')
        exercise = analysis.get('exercise', '')
        
        feedback_messages = {
            'Good': [
                "Great job! Perfect position.",
                "Excellent form! Hold it.",
                "Perfect! You're in the target range."
            ],
            'Too little': [
                "Move a little more.",
                "Increase the range slightly.",
                "You can go a bit further."
            ],
            'Too much': [
                "Ease back a little.",
                "Reduce the range slightly.",
                "Not so far, come back a bit."
            ],
            'Forward head': [
                "Pull your chin back.",
                "Retract your head.",
                "Bring your head back over your shoulders."
            ]
        }
        
        messages = feedback_messages.get(status, ["Adjust your position."])
        import random
        message = random.choice(messages)
        self.speak(message)
    
    def enable_audio(self):
        """Enable audio feedback"""
        self.is_enabled = True
    
    def disable_audio(self):
        """Disable audio feedback"""
        self.is_enabled = False