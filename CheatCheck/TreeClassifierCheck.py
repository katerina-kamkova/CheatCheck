import pandas as pd
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier
from sklearn import metrics  # Import scikit-learn metrics module for accuracy calculation


bank_data = pd.read_csv("C:/CheatingCheck/Data_table.csv")

XX = (bank_data.drop(columns=['Usernames', 'Logs number', 'Link clicked', 'Total time', 'Study time',
                              'Sessions number', 'Average session time', 'Number tabs visited', 'Jump number',
                              'Average jump number', 'Number speed clicks', 'Average forward seek',
                              'Average backward seek', 'Average pause number', 'Result']))[:1000]
yy = (bank_data['Result'])[:1000]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(XX, yy, test_size=0.20)

# Create Decision Tree classifier object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifier
clf = clf.fit(X_train, y_train)

# Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
