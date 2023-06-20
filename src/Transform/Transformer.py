import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

class TextProcessor:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.df = pd.read_json(f'../data/{self.file_name}.json')

    def remove_stopwords(self, text):
        stopwords_pt = set(stopwords.words('portuguese'))
        tokens = text.split()
        tokens_cleaned = [token for token in tokens if token.lower() not in stopwords_pt]
        return ' '.join(tokens_cleaned)

    def remove_punctuation(self, text):
        return re.sub(r'[^\w\s]', '', text)

    def remove_line_breaks(self, text):
        return re.sub(r'\n', '', text)
        
    def clean_text(self, remove_date=False, remove_dupes=False):
        df_ct = self.df.copy()

        if remove_date:
            df_ct.drop_duplicates(subset=('link'), ignore_index=True, inplace=True)
            df_ct.drop(columns=['date'], inplace=True)

        df_ct['text'] = df_ct['text'].apply(self.remove_line_breaks)
        df_ct['text'] = df_ct['text'].apply(self.remove_punctuation)
        df_ct['text'] = df_ct['text'].apply(self.remove_stopwords)
        return df_ct['text'].tolist()
    
    def save_clean_text(self, remove_date=False, remove_dupes=False):
        with open(f'../data/{self.file_name}_clean.txt', 'w') as f:
            for text in self.clean_text():
                f.write(text + '\n')