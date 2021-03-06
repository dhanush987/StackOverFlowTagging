#This program will Train 
"""
MultiNomial Naive Bayes
Random Forest
XGBoost
SVM
clustering K Means
"""
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
from time import time
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Image
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
import sqlite3
import re
import time
import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.learning_curve import learning_curve
from sklearn.model_selection import GridSearchCV
from matplotlib import pyplot as pl
from matplotlib.backends.backend_pdf import PdfPages
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_blobs
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import glob,os
from scipy.stats import mode
import seaborn as sns
import sqlite3
import re
import time
import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.learning_curve import learning_curve
from sklearn.model_selection import GridSearchCV
from matplotlib import pyplot as pl
from matplotlib.backends.backend_pdf import PdfPages
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_blobs
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import glob,os
#MultiNomial

def MyMultiNomialNB(X_train, y_train):
	clf = MultinomialNB()
	param_grid = {'alpha': [0.000000001,0.00000001,0.0000001,0.01,0.1,1,10,100,1000] }
	#param_grid = {'alpha': [0.000000001] }
	# Ten fold Cross Validation
	classifier= GridSearchCV(estimator=clf, cv=5 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyExtraTreeClassifier(X_train, y_train):
	clf = ExtraTreesClassifier(min_samples_split=2, random_state=0,max_depth = 10)
	param_grid = {'n_estimators': [10,20,30,50]}
	#param_grid = {'max_depth': [1,5,10,25,50,75,100,500,1000,2000]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid,n_jobs=3)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_


def MyRandomForest(X_train, y_train):
	clf = RandomForestClassifier()
	#param_grid = {'n_estimators': [10,20,30,50,70,100]}
	param_grid = {'n_estimators': [100,200,300,400]}#,100,150,200]}
	classifier= GridSearchCV(estimator=clf, cv=2 ,param_grid=param_grid,verbose=10)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def rbf_svm(X_train, y_train):
	rbf_svc = svm.SVC(kernel='rbf')#,max_iter = 10000,cache_size =1024,decision_function_shape ='ovo'/'ovo'
	param_grid = {'C': np.logspace(-3, 2, 6), 'gamma': np.logspace(-3, 2, 6)}
	classifier= GridSearchCV(estimator=rbf_svc, cv=5 ,param_grid=param_grid)
	y_train= np.array(y_train)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

"""
db_file='oldData.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
SQL = "Select  date,name from code25;"
cursor.execute(SQL)
"""
X=[]
y=[]
"""
for row in cursor:
	X.append(row[0])
	y.append(row[1])
"""

code_loc='/Users/Dhanush/Desktop/SODATAFINAL/CodeText25/'
name_file=['javascript','sql','java','c#','python','php','c++','c','typescript','ruby','swift','objective-c','vb.net','assembly','r','perl','vba','matlab','go','scala','groovy','coffeescript','lua','haskell']
for item in name_file:
	print item
	code_loc_current=code_loc+item+'/'
	file_list = glob.glob(os.path.join(code_loc_current, "*.txt"))
	for file_path in file_list:
		f=open(file_path,'r')
		data=f.read()
		label=item
		X.append(data)
		y.append(label)
	#Complete dataset loaded
#print(X)
#Change Y to categorical labels.
labels= list(set(y))
labels.sort()
print len(labels)
label_mapping ={}

for i in range(24):
	print i
	label_mapping[labels[i]] = i+1

print(label_mapping)
#Lets encode the training data with this labels

for i in range(len(y)):
	y[i] = label_mapping[y[i]]
#print(y)
a=time.time()
print ("Vectorization started")
cv = TfidfVectorizer(input ='X',stop_words = {'english'},lowercase=True,analyzer ='word',min_df=10,max_features =1000)#,non_negative=True)#,)
X = cv.fit_transform(X)
vocab = np.array(cv.get_feature_names())
print (len(vocab))
print ("Time taken to vectorize is %s seconds" %(time.time()-a))#print vocab


#[X,y,encode_label]=joblib.load('/Users/Dhanush/Desktop/SODATAFINAL/Doc2Vec/Doc2Vec_text25_vector.pkl')
#Lets split the data into train-test

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.40, random_state=453456)

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=24)
kmeans.fit(X_train)
y_kmeans = kmeans.predict(X_train)
y_train=np.array(y_train)
labels = np.zeros_like(y_kmeans)
for i in range(1,25,1):
    mask = (y_kmeans == i)
    print (mask)
    labels[mask] = mode(y_train[mask])[0]
X_train=np.array(X_train)

from sklearn.metrics import accuracy_score
print accuracy_score(y_train, labels)
centers = kmeans.cluster_centers_
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_kmeans, s=50, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
plt.savefig("soem.png", dpi=300)

