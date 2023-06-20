import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

class Transformer:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.df = pd.read_json(f'../data/{self.file_name}.json')

    def print_df(self):
        print(self.df.head())

    def remove_stopwords(self, text):
        stopwords_pt = set(stopwords.words('portuguese'))
        tokens = text.split()
        tokens_cleaned = [token for token in tokens if token.lower() not in stopwords_pt]
        return ' '.join(tokens_cleaned)

    def remove_punctuation(self, text):
        return re.sub(r'[^\w\s]', '', text)

    def remove_line_breaks(self, text):
        return re.sub(r'\n', '', text)
    
    def remove_duplicates(self):
        self.df.drop_duplicates(subset=('link'), ignore_index=True, inplace=True)

        return self.df

    def remove_date(self):
        self.df.drop(columns=['date'], inplace=True)
        
        return self.df
        
    def clean_text(self, save: bool = False):
        df_ct = self.df.copy()

        #check if there is a date column
        if 'date' in df_ct.columns:
            self.remove_date()

        #check if there are duplicates

        if df_ct['link'].duplicated().any():
            self.remove_duplicates()
    
        df_ct['text'] = df_ct['text'].apply(self.remove_line_breaks)
        df_ct['text'] = df_ct['text'].apply(self.remove_punctuation)
        df_ct['text'] = df_ct['text'].apply(self.remove_stopwords)

        #return to save df as json
        
        if save:
            #use utf-8 encoding to avoid problems with special characters
            df_ct.to_json(f'../clean_data/{self.file_name}_cleaned.json', orient='records', force_ascii=False)
            print(f'File {self.file_name}_cleaned.json saved successfully!')

        return df_ct