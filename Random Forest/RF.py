import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import random
import numpy
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
df = pd.read_csv('Reservations.csv')
le = LabelEncoder()

for col in df.columns:
    if df[col].dtype == 'object': 
        df[col] = le.fit_transform(df[col].astype(str))
print(df)
print(df.isnull().any(axis=1))

data = np.array(df)
Feature = data[:,:-1]
print(Feature)
Label = data[:,-1]
Label = Label.astype(int)
print(Label)

x_train,x_test,y_train,y_test = train_test_split(Feature, Label, test_size=0.2)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(x_test.shape)

model = RandomForestClassifier(n_estimators=120, bootstrap=False)
model.fit(x_train,y_train)
prediction_x_test = model.predict(x_test)
print(prediction_x_test)

score = accuracy_score(y_test, prediction_x_test)
print(score)



print(x_train.shape)
print(x_train[[2,3]])
def CreateSubDataset(X,Y,num_sample):
  list_rand = []
  for i in range(len(Y)):
    list_rand.append(random.randint(0,len(Y)-1))
  list_sample = random.sample(list_rand,num_sample)

  list_X = X[list_sample]
  list_X = np.array(list_X)
  list_Y = Y[list_sample]
  list_Y= np.array(list_Y)
  return list_X,list_Y

def RandomForest(X,Y,x_test,y_test,so_cay=100):
  jung_pre =[]
  for i in range(so_cay):
    x_tree,y_tree = CreateSubDataset(X,Y,10000)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_tree,y_tree)
    pre = clf.predict(x_test)
    jung_pre.append(pre)
  jung_pre = np.array(jung_pre)
  result = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=jung_pre)
  acc = accuracy_score(y_test, result)
  return acc
accuracy = RandomForest(x_train,y_train,x_test,y_test,120)
print(accuracy)