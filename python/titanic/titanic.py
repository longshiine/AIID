import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score

train = pd.read_csv('./titanic/train.csv')
#-------------------------------------------------------------------------------
train['Age'] = train['Age'].fillna(29)
print(train['Age'])
train['Sex'] = train['Sex'].map({'male' : 0, 'female' : 1})
#-------------------------------------------------------------------------------
train_x = train[['Pclass', 'SibSp','Age', 'Sex']]
train_y = train['Survived']
# 모델 만들기
model = DecisionTreeClassifier()
# 학습하기
model.fit(train_x, train_y)
# 평가하기
scores = cross_val_score(model, train_x, train_y, scoring = 'accuracy', cv = 3)
print(scores.mean())
# 테스트 데이터 예측하기
test = pd.read_csv('./titanic/test.csv')
#-------------------------------------------------------------------------------
test['Age'] = test['Age'].fillna(29)
test['Sex'] = test['Sex'].map({'male' : 0, 'female' : 1})
#-------------------------------------------------------------------------------
test_x = test[['Pclass', 'SibSp', 'Age', 'Sex']]
test_y_pred = model.predict(test_x)
#print(test_y_pred)
# 제출 파일에 맞게 변형하여 저장하기
# submission = pd.read_csv("./titanic/sample_submission.csv")
# submission['Survived'] = test_y_pred
# submission.to_csv('submission.csv', index = False)