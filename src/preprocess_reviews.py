import os
import pandas as pd

class DataCleaner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.filepath)

    def preprocess(self):
        """Applies cleaning rules."""
        if self.df is None:
            raise ValueError("Data not loaded.")

        # 1. Rename Columns
        cols_map = {'content': 'review', 'score': 'rating', 'at': 'date'}
        self.df.rename(columns=cols_map, inplace=True)
        
        # 2. Filter Columns
        keep_cols = ['review', 'rating', 'date', 'bank', 'source']
        self.df = self.df[keep_cols]

        # 3. Drop Duplicates & Nulls
        initial_len = len(self.df)
        self.df.dropna(subset=['review', 'rating'], inplace=True)
        self.df.drop_duplicates(subset=['review', 'bank'], inplace=True)
        
        # 4. Normalize Date
        self.df['date'] = pd.to_datetime(self.df['date']).dt.strftime('%Y-%m-%d')
        
        print(f"Cleaning Complete. Dropped {initial_len - len(self.df)} rows.")
        return self.df

    def save(self, output_path):
        os.makedirs(os.path.dirname(os.path.dirname(output_path)), exist_ok=True)
        self.df.to_csv(output_path, index=False)
        print(f"Cleaned data saved to {output_path}")