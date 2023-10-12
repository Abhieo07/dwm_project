import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from scipy import stats

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
            
            self.clean()
            self.outliers()
            self.transform()
            self.categorical()

            

        except Exception as e:
            f'An error ocuured {str(e)}'

    def clean(self):
        self.missing_values = self.df.isnull().sum() # Identify missing values
        
        self.df = self.df.dropna() # Remove rows with missing values

        # Replace missing val with mean
        for column in self.df:
            if self.df[column].dtype != object: #str doesn't have mean
                self.df[column].fillna(self.df[column].mean(), inplace=True)

        self.df = self.df.drop_duplicates() # Remove duplicate rows
    
    # Correct data entry errors i.e., typos 
    def replace(self,column = None, error_value  = None, correct_value  = None):
        if self.df[column].dtype == object: # only str
            self.df[column] = self.df[column].str.replace(error_value, correct_value)

    #This is out of line
    def outliers(self):
        # z_scores = (self.df - self.df.mean()) / self.df.std()
        # self.df = self.df[(z_scores < 3).all(axis=1)]
        # print(self.df)

        for column in self.df:
            if self.df[column].dtype != object:
                z_scores = np.abs(stats.zscore(self.df[column]))
                self.df = self.df[(z_scores < 3)]
                # print(self.df)
        
    # This will transform one column and also for categorizes the column 
    def transform(self):
        # print(self.df)
        for column in self.df:
            if self.df[column].dtype != object:
                # self.df[column] = np.log(self.df[column])

                # Min-Max scaling
                # print(self.df[column])
                self.df[column] = (self.df[column] - self.df[column].min()) / (self.df[column].max() - self.df[column].min())
                # print(self.df[column])

    def categorical(self):
        # one-hot encoding
        for column in self.df:
            if len(self.df[column].unique()) == len(self.df):
                continue
            if self.df[column].dtype == object:
                self.df = pd.get_dummies(self.df, columns=[column])

        le = LabelEncoder()
        for column in self.df:
            if len(self.df[column].unique()) == len(self.df):
                continue
            if self.df[column].dtype == object:
                self.df[column] = le.fit_transform(self.df[column])


    def cleaned_data(self):
        cleaned_data_json = self.df.to_json(orient='columns')
        # new_file = self.df.to_json('cleaned.json')
        return cleaned_data_json
