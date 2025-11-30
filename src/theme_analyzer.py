import pandas as pd

class ThemeClassifier:
    def __init__(self):
        # Define keywords for rule-based classification
        self.theme_map = {
            "Security & Access": ['login', 'signin', 'password', 'otp', 'fingerprint', 'register'],
            "Transaction Issues": ['slow', 'transfer', 'transaction', 'sent', 'money', 'deducted'],
            "App Stability": ['crash', 'close', 'bug', 'error', 'open', 'update'],
            "UI/UX": ['interface', 'design', 'easy', 'confusing', 'user', 'screen'],
            "Customer Support": ['support', 'service', 'call', 'branch', 'respond']
        }

    def _classify_single(self, text):
        text = str(text).lower()
        for theme, keywords in self.theme_map.items():
            if any(k in text for k in keywords):
                return theme
        return "General Feedback"

    def apply_themes(self, df):
        print("Classifying Themes...")
        df['theme'] = df['review'].apply(self._classify_single)
        return df