import mlrose
import numpy as np
import pandas as pd
import math
import time
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier

# data processing for Neural Network
# data = pd.read_csv("data/bankdata.csv")
data = pd.read_csv("data/titanic_train.csv")
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

###### Neural Networks ######
clf = MLPClassifier(hidden_layer_sizes=(5,2), solver='adam', activation='logistic', learning_rate_init=0.015, random_state=100)
score1 = []
score2 = []
size = []
start = time.time()
for i in range(1, 95, 10):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i / 100.0)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))
    if i == 1:
        print(i)
        print(clf.coefs_)
        print(clf.intercepts_)
end = time.time()
runtime = end-start

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy', 'testing accuracy'], figsize=(10, 5))
plt.title('Learning curve for Neural Network', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for Neural Network.png')
plt.show()

print(clf.coefs_)
print(clf.intercepts_)
print(clf.n_iter_)
print(clf.n_layers_)
print(runtime)
print(max(score2))


###### RHC #######
###### by number od iteration ######
trainX, trainY, testX, testY, features, class_name = data_prep(data, 0.6)
score1 = []
score2 = []
size = []
for i in range(1, 1002, 50):
    clf = mlrose.NeuralNetwork(hidden_nodes=[2], activation='relu', algorithm='random_hill_climb', max_iters=i, \
                               bias=True, is_classifier=True, learning_rate=0.015, early_stopping=True, clip_max=5,
                               max_attempts=10)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy','testing accuracy'], figsize=(10, 5))
plt.title('Model Complexity Curve for RHC', fontsize=20)
plt.xlabel('Max Iterations', fontsize=20)
plt.ylabel('Accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Model Complexity Curve for RHC - Number of iterations.png')
plt.show()

###### by number od restarts ######
score1 = []
score2 = []
size = []
for i in range(1, 11, 1):
    clf = mlrose.NeuralNetwork(hidden_nodes=[2], activation='relu', algorithm='random_hill_climb', max_iters=750, \
                               bias=True, is_classifier=True, learning_rate=0.015, early_stopping=True, clip_max=5,
                               restarts=i, max_attempts=10)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy','testing accuracy'], figsize=(10, 5))
plt.title('Model Complexity Curve for RHC', fontsize=20)
plt.xlabel('Number of Restarts', fontsize=20)
plt.ylabel('Accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Model Complexity Curve for RHC - Number of restarts.png')
plt.show()

###### RHC with optimal parameters ######
score1 = []
score2 = []
size = []
start = time.time()
for i in range(1, 95, 10):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i / 100.0)
    clf = mlrose.NeuralNetwork(hidden_nodes=[2], activation='relu', algorithm='random_hill_climb', max_iters=750, \
                               bias=True, is_classifier=True, learning_rate=0.015, early_stopping=True, clip_max=5,
                               restarts=5, max_attempts=10)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

end = time.time()
runtime = end-start
df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy','testing accuracy'], figsize=(10, 5))
plt.title('Learning curve for RHC', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('Accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for RHC.png')
plt.show()

print(clf.fitted_weights.shape[0])
print(clf.predicted_probs.shape[0])
print(max(clf.predicted_probs))
print(runtime)

##### SA #######
### Cololing rate ###
trainX, trainY, testX, testY, features, class_name = data_prep(data, 0.6)
score1 = []
score2 = []
size = []
for i in np.arange(0.01, 1, 0.1):
    clf = mlrose.NeuralNetwork(hidden_nodes=[2], activation='relu', algorithm='simulated_annealing', max_iters=750,
                               schedule=mlrose.GeomDecay(init_temp=1.0, decay=i, min_temp=0.001), bias=True,
                                 is_classifier=True, learning_rate=0.015, early_stopping=True, clip_max=5, max_attempts=100)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy','testing accuracy'], figsize=(10, 5))
plt.title('Model Complexity Curve for SA - cooling rate', fontsize=20)
plt.xlabel('Cooling rate', fontsize=20)
plt.ylabel('Accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Model Complexity Curve for SA - cooling rate.png')
plt.show()

### Initial Temperature ###
trainX, trainY, testX, testY, features, class_name = data_prep(data, 0.6)
score1 = []
score2 = []
size = []
for i in np.arange(0.01, 1, 0.1):
    clf = mlrose.NeuralNetwork(hidden_nodes=[2], activation='relu', algorithm='simulated_annealing', max_iters=750,
                               schedule=mlrose.GeomDecay(init_temp=i, decay=0.99, min_temp=0.001), bias=True,
                                 is_classifier=True, learning_rate=0.015, early_stopping=True, clip_max=5, max_attempts=100)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy','testing accuracy'], figsize=(10, 5))
plt.title('Model Complexity curve for SA - initial temp', fontsize=20)
plt.xlabel('Initial Temperature', fontsize=20)
plt.ylabel('Accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Model Complexity curve for SA - initial temp.png')
plt.show()

### SA with optimal parameter ###
score1 = []
score2 = []
size = []
start = time.time()
for i in range(1, 95, 10):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i / 100.0)
    clf = mlrose.NeuralNetwork(hidden_nodes=[2], activation='relu', algorithm='simulated_annealing', max_iters=750,
                               schedule=mlrose.GeomDecay(init_temp=1, decay=0.4, min_temp=0.001), bias=True,
                               is_classifier=True, learning_rate=0.015, early_stopping=True, clip_max=5,
                               max_attempts=100)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))
end = time.time()
print(clf.fitted_weights.shape[0])
print(clf.predicted_probs.shape[0])
print(max(clf.predicted_probs))
runtime = end-start
print(runtime)

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy','testing accuracy'], figsize=(10, 5))
plt.title('Learning curve for SA', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('Accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for SA.png')
plt.show()

##### GA #######
trainX, trainY, testX, testY, features, class_name = data_prep(data, 0.6)
score1 = []
score2 = []
size = []
for i in range(1, 200, 10):
    clf = mlrose.NeuralNetwork(hidden_nodes=[2], activation='relu', algorithm='genetic_alg', pop_size=i, max_iters=100, \
                               bias=True, is_classifier=True, early_stopping=True)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy','testing accuracy'], figsize=(10, 5))
plt.title('Model Complexity for GA - population size', fontsize=20)
plt.xlabel('Population size', fontsize=20)
plt.ylabel('Accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Model Complexity for GA - population size.png')
plt.show()

### GA with optimal parameter ###
score1 = []
score2 = []
size = []
start = time.time()
for i in range(1, 95, 10):
    trainX, trainY, testX, testY, features, class_name = data_prep(data, i/100.0)
    clf = mlrose.NeuralNetwork(hidden_nodes=[2], activation='relu', algorithm='genetic_alg', pop_size=100, max_iters=750,
                               bias=True, is_classifier=True, learning_rate=0.015, early_stopping=True, clip_max=5,
                               max_attempts=100)
    clf.fit(trainX, trainY)
    predY1 = clf.predict(trainX)
    predY2 = clf.predict(testX)
    size = np.append(size, i)
    score1 = np.append(score1, accuracy_score(trainY, predY1))
    score2 = np.append(score2, accuracy_score(testY, predY2))
end = time.time()
runtime = end-start

df = pd.DataFrame({'Data size': size, 'training accuracy':score1, 'testing accuracy':score2})
axes = df.plot(x='Data size', y=['training accuracy','testing accuracy'], figsize=(10, 5))
plt.title('Learning curve for GA', fontsize=20)
plt.xlabel('sampling training size', fontsize=20)
plt.ylabel('Accuracy score', fontsize=20)
axes.set_ylim([0,1])
plt.savefig('Learning curve for GA.png')
plt.show()

print(clf.fitted_weights.shape[0])
print(clf.predicted_probs.shape[0])
print(max(clf.predicted_probs))
print(runtime)

# fit into algorithms #
def fitalgs(problem):
    algs = ["Random Hill Climb", "Simulated Annealing", "Genetic Algorithm", "MIMIC"]
    bestFitness = []
    runtime = []
    iterations = []

    start = time.time()
    best_state, best_fitness, fitness_curve = mlrose.random_hill_climb(problem, max_attempts=10, max_iters=100, curve=True)
    end = time.time()
    iterations = np.append(iterations, fitness_curve.shape[0])
    bestFitness = np.append(bestFitness, best_fitness)
    rhc_fitness = -fitness_curve
    runtime = np.append(runtime, end - start)

    start = time.time()
    best_state, best_fitness, fitness_curve = mlrose.simulated_annealing(problem, schedule = mlrose.GeomDecay(), max_attempts = 10, max_iters = 100, curve=True)
    end = time.time()
    iterations = np.append(iterations, fitness_curve.shape[0])
    bestFitness = np.append(bestFitness,best_fitness)
    sa_fitness = -fitness_curve
    runtime = np.append(runtime,end-start)

    start = time.time()
    best_state, best_fitness,fitness_curve = mlrose.genetic_alg(problem, pop_size=100, max_attempts = 10, max_iters=100, curve=True)
    end = time.time()
    iterations = np.append(iterations, fitness_curve.shape[0])
    bestFitness = np.append(bestFitness,best_fitness)
    ga_fitness = -fitness_curve
    runtime = np.append(runtime,end-start)

    start = time.time()
    best_state, best_fitness, fitness_curve = mlrose.mimic(problem,pop_size=100, max_attempts=10, max_iters=100, curve=True)
    end = time.time()
    iterations = np.append(iterations, fitness_curve.shape[0])
    bestFitness = np.append(bestFitness,best_fitness)
    print(fitness_curve)
    runtime = np.append(runtime,end-start)

    # get results #
    df = pd.DataFrame({'Algorithms': algs, 'Best Fitness Value':bestFitness, 'Runtime':runtime, 'Num of Iterations':iterations.astype(int)})
    print(df)


## TravellingSales fitness function ##
# define fitness problem #
coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3)]
fitness = mlrose.TravellingSales(coords = coords_list)
problem = mlrose.TSPOpt(length = 8, fitness_fn = fitness, maximize = False)
fitalgs(problem)

## 8-Queens problem ##
# define fitness problem #
fitness = mlrose.Queens()
problem = mlrose.DiscreteOpt(length = 8, fitness_fn = fitness, maximize = False, max_val = 8)
fitalgs(problem)

## Knapsack fitness function ##
# define fitness problem #
weights = [10, 5, 2, 8, 15, 1, 20, 50]
values = [1, 2, 3, 4, 5, 6, 7, 8]
fitness = mlrose.Knapsack(weights, values)
problem = mlrose.DiscreteOpt(length = 8, fitness_fn = fitness, maximize = True)
fitalgs(problem)

