import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class Cleaning:

    def __init__(self,file):
        try:
            if str(file).endswith('.csv'):
                self.df = pd.read_csv(file)
            elif str(file).endswith('.json'):
                self.df = pd.read_json(file)
            elif str(file).endswith('.xlsx'):
                self.df = pd.read_excel(file)
            else:
                raise TypeError("Invaid file format")
        except Exception as e:
            f'An error ocuured {str(e)}'

    def clean(self):

        self.missing_values = self.df.isnull().sum() # Identify missing values
        
        self.df = self.df.dropna() # Remove rows with missing values

        # Replace missing val with mean
        for self.column in self.df:
            if self.df[self.column].head(1).dtype != object: #str doesn't have mean
                self.df[self.column].fillna(self.df[self.column].mean(), inplace=True)

        self.df = self.df.drop_duplicates() # Remove duplicate rows

        clean = self.df[:2]
        return f"{clean} is being cleaned"
    
    # Correct data entry errors i.e., typos 
    def replace(self,column = None, error_value  = None, correct_value  = None):
        if self.df[column].head(1).dtype == object: # only str
            self.df[column] = self.df[column].str.replace(error_value, correct_value)

    # This will transform one column and also for categorizes the column 
    def transform(self):
        for self.column in self.df:
            if self.df[self.column].head(1).dtype != object:
                self.df[self.column] = np.log(self.df[self.column])

                # Min-Max scaling
                self.df[self.column] = (self.df[self.column] - self.df[self.column].min()) / (self.df[self.column].max() - self.df[self.column].min())

    def categorical(self, categorical_column = None):
        self.df = pd.get_dummies(self.df, columns=[categorical_column])
        le = LabelEncoder()
        self.df[categorical_column] = le.fit_transform(self.df[categorical_column])

    #This is out of line
    def outliers(self):
        z_scores = (self.df - self.df.mean()) / self.df.std()
        self.df = self.df[(z_scores < 3).all(axis=1)]
