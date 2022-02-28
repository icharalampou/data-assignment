import re

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

#read file with json schemas to dataframe
df = pd.read_json('converted_data.json')

# drop nan values in contents_of_violation column, all row
df.dropna(subset=['contents_of_violation'], how='all', inplace=True)

# convert string to datetime format
df['datetime'] = pd.to_datetime(df['publication_day'], format="%Y/%m/%d")

#remove sympols from contents_of_violations values and create y value
chars_to_remove = ['.', '-', '(', ')', '', '/', ':']
regular_expression = '[' + re.escape (''. join (chars_to_remove)) + ']'

#y = contents_of_violation -> target
y = df['contents_of_violation'].str.replace(regular_expression, '', regex=True)

#drop irrelevant columns and target to keep only columns for model fitting
X = df.drop(['other_info', 'url', 'source', 'contents_of_violation', 'publication_day'], axis=1)

#remove sympols from items values
X['items'] = X['item'].str.replace(regular_expression, '', regex=True)

#split data to train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=27)

#initialize RandomForestClassifier
rf = RandomForestClassifier()

#train  model with train values (x,y)
rf.fit(X_train, y_train)

#predict x test (to find ytest)
pred = rf.predict(X_test)

#find accuracy
print(accuracy_score(pred, y_test))
