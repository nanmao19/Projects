import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.tree import export_graphviz
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

###### Data preparation ######

data = pd.read_csv("data/wine.csv")
#data = pd.read_csv("data/titanic_train.csv")
print(data.head())
print(data.shape)

def data_prep(data, fraction):
    train = data.sample(frac=fraction) # randomly select 60% as training data
    test = data.loc[data.index.difference(train.index)] # set the rest data as test data

    # split data for X and Y
    trainX = train.iloc[:, 0:-1]
    features = trainX.columns.values

    trainY = train.iloc[:, -1]
    class_name = list(map(str, set(trainY)))

    testX = test.iloc[:, 0:-1]
    testY = test.iloc[:, -1]

    return trainX, trainY, testX, testY, features, class_name

###### Decision Tree Visualization ######

clf = tree.DecisionTreeClassifier(random_state=0, criterion='gini', max_depth=3)
trainX, trainY, testX, testY, features, class_name = data_prep(data, 0.6)
clf.fit(trainX, trainY)
export_graphviz(clf, out_file='tree.dot', feature_names=features, class_names=class_name, filled=True, rounded=True, special_characters=True)


# Convert .dot to png
from subprocess import call
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

# Display png in python
plt.figure(figsize = (18, 18))
plt.title('Decision Tree')
plt.imshow(plt.imread('tree.png'))
plt.axis('off')
plt.show()

###### 1. Decision Tree learning curves comparision ######
# plot Learning curve for Decision Tree max-depth=3
clf = tree.DecisionTreeClassifier(random_state=0, criterion='gini', max_depth=3)
score1 = []
score2 = []
size = []
for i in range(1, 95, 1):
    trainX_temp, trainY_temp, testX_temp, testY_temp, features_temp, class_name_temp = data_prep(data, i/100.0)
    clf.fit(trainX_temp, trainY_temp)
    trainpred = clf.predict(trainX_temp)
    testpred = clf.predict(testX_temp)
    size = np.append(size, i/100.0)
    score1 = np.append(score1, accuracy_score(trainY_temp, trainpred))
    score2 = np.append(score2, accuracy_score(testY_temp, testpred))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for Decision Tree max-depth=3', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for Decision Tree max-depth=3.png', fontsize=20)
plt.show()

# plot Learning curve for Decision Tree max-depth=10
clf = tree.DecisionTreeClassifier(random_state=0, criterion='gini', max_depth=10)
score1 = []
score2 = []
size = []
for i in range(1, 95, 1):
    trainX_temp, trainY_temp, testX_temp, testY_temp, features_temp, class_name_temp = data_prep(data, i/100.0)
    clf.fit(trainX_temp, trainY_temp)
    trainpred = clf.predict(trainX_temp)
    testpred = clf.predict(testX_temp)
    size = np.append(size, i/100.0)
    score1 = np.append(score1, accuracy_score(trainY_temp, trainpred))
    score2 = np.append(score2, accuracy_score(testY_temp, testpred))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for Decision Tree max-depth=10', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for Decision Tree max-depth=10.png', fontsize=20)
plt.show()

###### 2. Neural Networks ######

# find best learning rate
score1 = []
score2 = []
lr = []
trainX, trainY, testX, testY, features, class_name = data_prep(data, 60.0/100.0)
for i in np.arange(0.001, 0.05, 0.002):
    clf = MLPClassifier(hidden_layer_sizes=(5,2), solver='adam', activation='logistic',learning_rate_init=i, random_state=100)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    lr = np.append(lr, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Learning Rate': lr,'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Learning Rate', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for Neural Network Learning Rate', fontsize=20)
plt.xlabel('sampling Learning Rate', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for Neural Network Learning Rate.png')
plt.show()

clf = MLPClassifier(hidden_layer_sizes=(5,), solver='adam', activation='logistic', learning_rate_init=0.015, random_state=100)
score1 = []
score2 = []
size = []
for i in range(1, 95, 10):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i / 100.0)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for Neural Network 1-layer', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for Neural Network 1-layer.png')
plt.show()

clf = MLPClassifier(hidden_layer_sizes=(5,2), solver='adam', activation='logistic', learning_rate_init=0.015, random_state=100)
score1 = []
score2 = []
size = []
for i in range(1, 95, 10):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i / 100.0)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))


df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for Neural Network 2-layers', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for Neural Network 2-layers.png')
plt.show()

clf = MLPClassifier(hidden_layer_sizes=(20,5,2), solver='adam', activation='logistic', learning_rate_init=0.015, random_state=100)
score1 = []
score2 = []
size = []
for i in range(1, 95, 10):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i / 100.0)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for Neural Network 3-layers', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for Neural Network 3-layers.png')
plt.show()

###### 3. Boosting ######

score1 = []
score2 = []
estimator = []
for i in range(1, 100, 1):
    clf = AdaBoostClassifier(base_estimator=tree.DecisionTreeClassifier(max_depth=1),n_estimators=i)
    trainX, trainY, testX, testY, features, class_name = data_prep(data, 0.6)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    estimator = np.append(estimator, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'estimator': estimator, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='estimator', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for AdaBoost Decision Tree max-depth=1', fontsize=20)
plt.xlabel('numbers of estimators', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for AdaBoost Decision Tree max-depth=1.png')
plt.show()

score1 = []
score2 = []
estimator = []
for i in range(1, 100, 1):
    clf = AdaBoostClassifier(base_estimator=tree.DecisionTreeClassifier(max_depth=5),n_estimators=i)
    trainX, trainY, testX, testY, features, class_name = data_prep(data, 0.6)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    estimator = np.append(estimator, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'estimator': estimator, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='estimator', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for AdaBoost Decision Tree max-depth=5', fontsize=20)
plt.xlabel('numbers of estimators', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for AdaBoost Decision Tree max-depth=5.png')
plt.show()

clf = AdaBoostClassifier(base_estimator=tree.DecisionTreeClassifier(max_depth=2),n_estimators=50)
score1 = []
score2 = []
size = []
for i in range(1, 95, 1):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i / 100.0)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for AdaBoost Decision Tree', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for AdaBoost Decision Tree')
plt.show()

###### 4. Support Vector Machines ######

clf = svm.SVC(kernel="linear")
score1 = []
score2 = []
size = []
for i in range(1, 95, 1):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i / 100.0)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for SVM linear kernel', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for SVM linear kernel.png')
plt.show()

clf = svm.SVC(kernel="sigmoid")
score1 = []
score2 = []
size = []
for i in range(1, 95, 1):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i / 100.0)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for SVM sigmoid kernel', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for SVM sigmoid kernel.png')
plt.show()

clf = svm.SVC(kernel="rbf")
score1 = []
score2 = []
size = []
for i in range(1, 95, 1):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i / 100.0)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for SVM rbf kernel', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for SVM rbf kernel.png')
plt.show()

###### 5. k-Nearest Neighbors ######

score1 = []
score2 = []
neighbor_size = []
for k in range(1,50):
    knn = KNeighborsClassifier(n_neighbors=k)
    trainX, trainY, testX, testY, features, class_name = data_prep(data, 0.6)
    knn.fit(trainX, trainY)
    predY1 = knn.predict(trainX)
    predY2 = knn.predict(testX)
    neighbor_size= np.append(neighbor_size, k)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2.append(accuracy_score(testY, predY2))

df = pd.DataFrame({'Neighbor Size': neighbor_size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Neighbor Size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for KNN different Neighbor Size', fontsize=20)
plt.xlabel('Neighbor Size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for KNN different Neighbor Size.png')
plt.show()

knn = KNeighborsClassifier(n_neighbors=2)
score1 = []
score2 = []
size = []
for i in range(1, 95, 1):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    knn.fit(trainX, trainY)
    predY1 = knn.predict(trainX)
    predY2 = knn.predict(testX)
    size = np.append(size, i / 100.0)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 10))
plt.title('Learning curve for KNN k=2', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for KNN k=2.png')
plt.show()

###### 6. Accuracy scores comparision ######
score = []
trainX, trainY, testX, testY, features, class_name = data_prep(data, 0.6)

clf = tree.DecisionTreeClassifier(random_state=0, criterion='gini', max_depth=5)
clf.fit(trainX, trainY)
predY = clf.predict(testX)
score.append(accuracy_score(testY, predY))

clf = MLPClassifier(hidden_layer_sizes=(5,2), solver='adam', activation='logistic', learning_rate_init=0.015, random_state=100)
clf.fit(trainX, trainY)
predY = clf.predict(testX)
score.append(accuracy_score(testY, predY))

clf = AdaBoostClassifier(base_estimator=tree.DecisionTreeClassifier(max_depth=10),n_estimators=50)
clf.fit(trainX, trainY)
predY = clf.predict(testX)
score.append(accuracy_score(testY, predY))

clf = svm.SVC(kernel="rbf")
clf.fit(trainX, trainY)
predY = clf.predict(testX)
score.append(accuracy_score(testY, predY))

knn = KNeighborsClassifier(n_neighbors=2)
clf.fit(trainX, trainY)
predY = clf.predict(testX)
score.append(accuracy_score(testY, predY))

classifier = ['DT(max-depth=5)','NN(2-layers)','AdaBoost(DT10)', 'SVM(rbf)', 'KNN(k=2)']
plt.figure(figsize=(10,10))
plt.bar(classifier, score)
plt.suptitle('Accuracy score comparison', fontsize=20)
plt.ylim([0,1])
plt.savefig('Accuracy score comparison.png')
plt.show()

