import pandas as pd
from sklearn import metrics  # Import scikit-learn metrics module for accuracy calculation


bank_data = pd.read_csv("C:/CheatingCheck/Data_table.csv")

XX = (bank_data.drop(columns=['Usernames', 'Logs number', 'Link clicked',
                              'Total time', 'Study time', 'Sessions number', 'Average session time',
                              'Go back number', 'In tab visited', 'Number tabs visited', 'Jump number',
                              'Average jump number', 'Average video watched time', 'Number speed clicks',
                              'Average forward seek', 'Average backward seek',
                              'Average pause number', 'Average rewatch video',
                              'Result']))[:1000]
yy = (bank_data['Result'])[:1000]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(XX, yy, test_size=0.20)

from sklearn.svm import SVC
svclassifier = SVC(kernel='rbf', gamma='auto')
svclassifier.fit(X_train, y_train)

y_pred = svclassifier.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
