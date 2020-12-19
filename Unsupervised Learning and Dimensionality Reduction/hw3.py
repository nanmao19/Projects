import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, FastICA, randomized_svd, LatentDirichletAllocation
from sklearn.mixture import GaussianMixture as GMM
from sklearn.decomposition import TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import LabelEncoder
'''
### import Wine quality  data ###
df = pd.read_csv("data/wine-red.csv")
print(df.head())
y = df.iloc[:,-1]
df = df.drop('quality', axis=1)
#print(df.shape)
#features = df.columns.values
#print(features)
'''
### import Iris data ###
df = pd.read_csv("data/Iris.csv")
df = df.drop('Id', axis=1)
features = df.columns.values
#print(features)

# convert label
le = LabelEncoder()
le.fit(df.iloc[:,-1])
y = le.transform(df.iloc[:,-1])
#Y_train = le.fit_transform(df[4].values)
df = df.drop('Species', axis=1)
print(df.shape)

# Standardize the data to have a mean of ~0 and a variance of 1
X_std = StandardScaler().fit_transform(df)

### k-means ###
print("======== k-means Orginal ========")
# plot to find optimal k value
ssd = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X_std)
    ssd.append(kmeans.inertia_)

fig, ax = plt.subplots(figsize=(6, 6))
plt.plot(range(1, 11), ssd, '-o')
plt.xlabel('number of clusters, k')
plt.ylabel('Cluster SSE')
plt.xticks(range(1, 11))
plt.title('Cluster SSE vs K-Value', fontweight='bold')
plt.savefig('Find optimal k value.png')
plt.show()

# Plot the original clustered data (k-Means)
km = KMeans(n_clusters=3, max_iter=100)
km.fit(X_std)
centroids = km.cluster_centers_

fig, ax = plt.subplots(figsize=(6, 6))
plt.scatter(X_std[km.labels_ == 0, 0], X_std[km.labels_ == 0, 1])
plt.scatter(X_std[km.labels_ == 1, 0], X_std[km.labels_ == 1, 1])
plt.scatter(X_std[km.labels_ == 2, 0], X_std[km.labels_ == 2, 1])

plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=300, c='black', label='centroid')
ax.set_aspect('equal')
plt.xlim([-2, 4])
plt.ylim([-2, 4])
plt.title('Visualization of original data', fontweight='bold')
plt.savefig('KMeans.png')
print(km.inertia_)
print(km.n_iter_)
plt.show()

### EM ###
print(X_std.shape)
print("======== EM Original ========")
# plot Plot the original clustered data (EM)
gmm = GMM(n_components=3, covariance_type='tied')
labels = gmm.fit(X_std).predict(X_std)
print(labels.shape)
print(gmm.weights_)
print(gmm.n_iter_)
print("log likelihood:", gmm.lower_bound_)

fig, ax = plt.subplots(figsize=(6, 6))
plt.scatter(X_std[:, 0], X_std[:, 1], c = labels, s=50)
plt.xlim([-2, 4])
plt.ylim([-2, 4])
ax.set_aspect('equal')
plt.title('Visualization of original data', fontweight='bold')
plt.savefig('EM.png')
plt.show()

### PCA ###
model = PCA(n_components=4)
pca = model.fit_transform(X_std)
print("Eigenvalue:", model.explained_variance_)
df_pca = pd.DataFrame(pca)
print(df_pca.shape)
#npc= model.n_components_
#most_important = [np.abs(model.components_[i]).argmax() for i in range(npc)]
#most_important_names = [features[most_important[i]] for i in range(npc)]
#dic = {'PC{}'.format(i): most_important_names[i] for i in range(npc)}
#dffeature = pd.DataFrame(dic.items())
#important_features = dffeature.iloc[:,-1].to_numpy()

# Plot the explained variances
features = range(model.n_components_)
plt.bar(features, model.explained_variance_ratio_)
plt.xlabel('PCA features')
plt.ylabel('variance')
plt.xticks(features)
plt.title('Percentage of variance', fontweight='bold')
plt.savefig('Percentage of variance')
plt.show()
print(model.explained_variance_ratio_)

# reduced feature PCA data
df_pca = df_pca.iloc[:, :2]
print(df_pca.shape)
X_std_pca = StandardScaler().fit_transform(df_pca)

# plot to find optimal k value in PCA data
ssd = []
for k in range(1, 12):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X_std_pca)
    ssd.append(kmeans.inertia_)

fig, ax = plt.subplots(figsize=(6, 6))
plt.plot(range(1, 12), ssd, '-o')
plt.xlabel('number of clusters, k')
plt.ylabel('Cluster SSE')
plt.xticks(range(1, 12))
plt.title('Cluster SSE vs K-Value', fontweight='bold')
plt.savefig('Find optimal k value.png')
plt.show()

# plot PCA clustered data
km = KMeans(n_clusters=3, max_iter=100)
km.fit(X_std_pca)
centroids = km.cluster_centers_
fig, ax = plt.subplots(figsize=(6, 6))
plt.scatter(X_std_pca[km.labels_ == 0, 0], X_std_pca[km.labels_ == 0, 1])
plt.scatter(X_std_pca[km.labels_ == 1, 0], X_std_pca[km.labels_ == 1, 1])
plt.scatter(X_std_pca[km.labels_ == 2, 0], X_std_pca[km.labels_ == 2, 1])
plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=300, c='black', label='centroid')
plt.xlim([-2, 4])
plt.ylim([-2, 4])
plt.title('Visualization of PCA data', fontweight='bold')
ax.set_aspect('equal')
plt.savefig('Visualization of PCA clustered data.png')
print(km.inertia_)
print(km.n_iter_)
plt.show()

### ICA ###
# calculate kurtosis for ICA data
model = FastICA(n_components=2, whiten=True)
ica = model.fit_transform(df)
df_ica = pd.DataFrame(data=ica)
mean = np.mean(df_ica, axis=0)
n = df_ica.shape[1]
var = np.sum((df_ica-mean)**2)/n
kurt = np.sum((df_ica-mean)**4)/n
kurt = kurt/(var**2)
kurt = kurt[~np.isnan(kurt)]
print(kurt)

# plot kurtosis
features = ["IC0", "IC1"]
#features = ["IC0", "IC1", "IC2"]
plt.bar(features, kurt, width=0.2)
plt.xlabel('ICA features')
plt.ylabel('Kurtosis')
plt.ylim([0,0.5])
plt.xticks(features)
plt.title('Kurtosis for ICA feature space', fontweight='bold')
plt.savefig('Kurtosis of ICA feature')
plt.show()

# # reduced feature ICA data
X_std_ica = StandardScaler().fit_transform(df_ica)

# plot to find optimal k value in ICA data
ssd = []
for k in range(1, 12):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X_std_ica)
    ssd.append(kmeans.inertia_)

fig, ax = plt.subplots(figsize=(6, 6))
plt.plot(range(1, 12), ssd, '-o')
plt.xlabel('number of clusters, k')
plt.ylabel('Cluster SSE')
plt.xticks(range(1, 12))
plt.title('Cluster SSE vs K-Value', fontweight='bold')
plt.savefig('Find optimal k value.png')
plt.show()

# plot ICA clustered data
km = KMeans(n_clusters=3, max_iter=100)
km.fit(X_std_ica)
centroids = km.cluster_centers_
fig, ax = plt.subplots(figsize=(6, 6))
plt.scatter(X_std_ica[km.labels_ == 0, 0], X_std_ica[km.labels_ == 0, 1])
plt.scatter(X_std_ica[km.labels_ == 1, 0], X_std_ica[km.labels_ == 1, 1])
plt.scatter(X_std_ica[km.labels_ == 2, 0], X_std_ica[km.labels_ == 2, 1])
plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=300, c='black', label='centroid')
plt.xlim([-4, 2])
plt.ylim([-4, 2])
plt.title('Visualization of ICA data', fontweight='bold')
ax.set_aspect('equal')
plt.savefig('Visualization of ICA clustered data.png')
print(km.inertia_)
print(km.n_iter_)
plt.show()

### RP ###
model = TruncatedSVD(n_components=3, algorithm='randomized')
rca = model.fit_transform(df)
df_rca = pd.DataFrame(data=rca)
print(model.components_.shape)
print(model.explained_variance_ratio_)
print(model.explained_variance_)

# reduced feature RP data
X_std_pca = StandardScaler().fit_transform(df_rca)
X_std_pca = df_rca

# plot dimension vs SEE in RP
ssd = []
seed = 9
for i in range(1, 4):
    model = TruncatedSVD(n_components=i, algorithm='randomized', random_state=0)
    rca = model.fit_transform(df)
    df_rca = pd.DataFrame(data=rca)
    X_std_pca = StandardScaler().fit_transform(df_rca)
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X_std_pca)
    ssd.append(kmeans.inertia_)

fig, ax = plt.subplots(figsize=(6, 6))
plt.plot(range(1, 4), ssd, '-o')
plt.xlabel('number of dimension')
plt.ylabel('Cluster SSE')
plt.xticks(range(1, 4))
plt.title('Cluster SSE vs Number of dimension', fontweight='bold')
plt.savefig('RP.png')
plt.show()

# feature reduction from RCA
model = TruncatedSVD(n_components=2, algorithm='randomized', random_state=seed)
rca = model.fit_transform(df)
df_rca = pd.DataFrame(data=rca)
X_std_pca = StandardScaler().fit_transform(df_rca)

# plot RCA clustered data
km = KMeans(n_clusters=3, max_iter=100)
km.fit(X_std_pca)
centroids = km.cluster_centers_
fig, ax = plt.subplots(figsize=(6, 6))
plt.scatter(X_std_pca[km.labels_ == 0, 0], X_std_pca[km.labels_ == 0, 1])
plt.scatter(X_std_pca[km.labels_ == 1, 0], X_std_pca[km.labels_ == 1, 1])
plt.scatter(X_std_pca[km.labels_ == 2, 0], X_std_pca[km.labels_ == 2, 1])
plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=300, c='black', label='centroid')
plt.xlim([-2, 4])
plt.ylim([-2, 4])
plt.title('Visualization of RCA data', fontweight='bold')
ax.set_aspect('equal')
plt.savefig('Visualization of RCA clustered data.png')
print(km.inertia_)
print(km.n_iter_)
plt.show()

### LDA ###
# Construct within-class covariant scatter matrix S_W
X_train_std = X_std

S_W = np.zeros((4,4))
for i in range(3):
    S_W += np.cov(X_train_std[y==i].T)

# Construct between-class scatter matrix S_B
N = np.bincount(y)  # number of samples for given class
vecs = []
[vecs.append(np.mean(X_train_std[y == i], axis=0)) for i in range(3)]  # class means
mean_overall = np.mean(X_train_std, axis=0)  # overall mean
S_B = np.zeros((4, 4))
for i in range(3):
    S_B += N[i] * (((vecs[i] - mean_overall).reshape(4, 1)).dot(((vecs[i] - mean_overall).reshape(1, 4))))

# Calculate sorted eigenvalues and eigenvectors of inverse(S_W)dot(S_B)
eigen_vals, eigen_vecs = np.linalg.eig(np.linalg.inv(S_W).dot(S_B))
print(eigen_vals)
eigen_pairs = [(np.abs(eigen_vals[i]), eigen_vecs[:, i]) for i in range(len(eigen_vals))]
eigen_pairs = sorted(eigen_pairs, key=lambda k: k[0], reverse=True)
print('Eigenvalues in decreasing order:\n')
for eigen_val in eigen_pairs:
    print(eigen_val[0])

# Plot main LDA components
tot = sum(eigen_vals.real)
discr = [(i / tot) for i in sorted(eigen_vals.real, reverse=True)]
print(discr)
cum_discr = np.cumsum(discr)
print(cum_discr)

# Project original features onto the new feature space
W = np.hstack((eigen_pairs[0][1][:, ].reshape(4, 1), eigen_pairs[1][1][:, ].reshape(4, 1))).real
X_train_lda = X_train_std.dot(W)

# Plot transformed features in LDA subspace
data = pd.DataFrame(X_train_lda)
data['class'] = y
data.columns = ["LD1", "LD2", "class"]

fig, ax = plt.subplots(figsize=(6, 6))
plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=data.iloc[:,-1], s=50)
plt.title('Visualization of LDA data', fontweight='bold')
plt.ylabel('LD2')
plt.xlabel('LD1')
plt.savefig('Visualization of LDA clustered data.png')
plt.show()

# LDA implementation using scikit-learn
lda = LinearDiscriminantAnalysis(n_components=2)
X_train_lda = lda.fit_transform(X_train_std, y)

data = pd.DataFrame(X_train_lda)
data['class'] = y
data.columns = ["LD1", "LD2", "class"]

fig, ax = plt.subplots(figsize=(6, 6))
plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=data.iloc[:,-1], s=50)
plt.title('Visualization of LDA data', fontweight='bold')
plt.ylabel('LD2')
plt.xlabel('LD1')
plt.savefig('Visualization of LDA clustered data.png')
plt.show()
