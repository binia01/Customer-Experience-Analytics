import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class ThemeClassifier:
    def __init__(self):
        # Expanded Dictionary based on standard FinTech taxonomy
        self.theme_map = {
            "Security & Access": [
                'login', 'signin', 'password', 'otp', 'fingerprint', 'code', 
                'biometric', 'register', 'verification', 'sms'
            ],
            "Transaction Performance": [
                'slow', 'transfer', 'transaction', 'sent', 'money', 'deducted', 
                'network', 'connection', 'stuck', 'pending', 'load'
            ],
            "App Stability": [
                'crash', 'close', 'bug', 'error', 'open', 'update', 
                'install', 'force', 'working', 'screen'
            ],
            "UI/UX": [
                'interface', 'design', 'easy', 'confusing', 'user', 
                'navigation', 'color', 'dark mode', 'layout'
            ],
            "Customer Support": [
                'support', 'service', 'call', 'branch', 'respond', 
                'staff', 'help', 'contact', 'queue'
            ]
        }

    def _classify_single(self, text):
        """
        Classifies a single text string. 
        Returns 'General Feedback' if no keywords match.
        """
        if not isinstance(text, str) or not text.strip():
            return "Unclassified"

        text_lower = text.lower()
        
        # Priority Check: Technical issues usually outweigh UI praise
        # Check specific themes in order of severity
        for theme, keywords in self.theme_map.items():
            if any(k in text_lower for k in keywords):
                return theme
        
        return "General Feedback"

    def apply_themes(self, df):
        """
        Applies classification to the DataFrame.
        """
        logging.info("Applying Rule-Based Theme Classification...")
        
        if df.empty:
            logging.warning("Input DataFrame is empty. Skipping classification.")
            return df

        try:
            # Use .loc to avoid SettingWithCopy warnings
            df = df.copy() 
            df['theme'] = df['review'].apply(self._classify_single)
            
            # Validation
            unclassified_count = len(df[df['theme'] == 'Unclassified'])
            if unclassified_count > 0:
                logging.warning(f"{unclassified_count} reviews could not be classified.")
                
            logging.info("Theme classification complete.")
            return df
            
        except Exception as e:
            logging.error(f"Critical error in theme classification: {e}")
            raise e