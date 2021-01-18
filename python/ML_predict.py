import pandas as pd
import numpy as np
from collections import Counter
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC 
from sklearn.neural_network import MLPClassifier


# dataset prepare
RANDOM_SEED = 42
data = pd.read_csv('./data/new.csv')
train, test = train_test_split(data, test_size=0.2, random_state=RANDOM_SEED)

train_x = train[['Target','Month(sin)','Month(cos)','Time(sin)','Time(cos)','Type','Sex','Age','Rain','Sky','Temperature']]
train_y = train['Location']
test_x = test[['Target','Month(sin)','Month(cos)','Time(sin)','Time(cos)','Type','Sex','Age','Rain','Sky','Temperature']]
test_y = test['Location']

## 1. Decision Tree Classifier()
model = DecisionTreeClassifier()
model.fit(train_x, train_y)
scores = cross_val_score(model, train_x, train_y, scoring = 'accuracy', cv = 3)

test_y_pred = model.predict(test_x)
DTC_accuracy = accuracy_score(test_y, test_y_pred)
print("DecisionTreeClassifier: ", DTC_accuracy*100, "%")

## 2. Support Vector Machine()
svm_model_linear = SVC(kernel = 'linear', C = 1, verbose=1).fit(train_x, train_y) 
svm_predictions = svm_model_linear.predict(test_x) 
 
SVM_accuracy = svm_model_linear.score(test_x, test_y) 
print("SupportVectorMachine: ", SVM_accuracy*100, "%")

# ## 3. Multi Layer Perceptron()