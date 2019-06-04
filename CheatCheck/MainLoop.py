import pandas as pd
import LogFilter
import json
from pandas import DataFrame
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier


# Convert logs into input data table
# Returns list of users and info matrix
def get_users_matrix():
    print("Enter the path to the file that contains logs: ")
    log_file_path = input()

    # Open file with logs
    try:
        data_file = open(log_file_path, 'r')
    except IOError:
        print("The log file isn`t found, check the path")
        return

    # Extract logs from the file and convert them in tne filter
    fail_json = list()
    filt = LogFilter.LogFilter()
    counter = 0
    for line in data_file:
        counter += 1
        print(counter)
        try:
            filt.extract_info(json.loads(line))
        except json.decoder.JSONDecodeError:
            fail_json.append(counter)

    data_file.close()
    users = filt.get_users()

    # Make proper data set
    # Make a table from data about users
    X = [[0] * 23 for i in range(len(users))]
    names_list = list(users.keys())
    names_list.sort()
    for i in range(len(users)):
        data_list = users[names_list[i]]
        for j in range(23):
            X[i][j] = data_list[j]

    return users, X


# Convert logs into input data table, save it in .csv file if save_filter_path != "" and return input table
def get_and_convert_training_logs():
    users, X = get_users_matrix()

    print("Enter the path to the .txt file with output values by one in the string")
    classific_path = input()

    names_list = list(users.keys())
    names_list.sort()

    # Get the output values from given file
    y = list()
    if classific_path != "":
        try:
            f = open(classific_path, 'r')
        except IOError:
            print("The output table file isn`t found, check the path")
            return

        for line in f:
            y.append(int(line))
        f.close()
    else:
        for i in range(len(users)):
            y.append(0)

    # Create data frame
    XT = [*zip(*X)]
    users_data = {'Usernames': names_list,
                  'Logs number': XT[0],
                  'Forum actions': XT[1],
                  'Show answer': XT[2],
                  'Link clicked': XT[3],
                  'Total time': XT[4],
                  'Study time': XT[5],
                  'Sessions number': XT[6],
                  'Average session time': XT[7],
                  'Go back number': XT[8],
                  'In tab visited': XT[9],
                  'Number tabs visited': XT[10],
                  'Jump number': XT[11],
                  'Average jump number': XT[12],
                  'Average video watched time': XT[13],
                  'Number speed clicks': XT[14],
                  'Average forward seek': XT[15],
                  'Average backward seek': XT[16],
                  'Videos watched': XT[17],
                  'Average pause number': XT[18],
                  'Average rewatch video': XT[19],
                  'Average attempts number': XT[20],
                  'Success number': XT[21],
                  'Tasks number': XT[22],
                  'Result': y}

    data_frame = DataFrame(users_data,
                           columns=['Usernames', 'Logs number', 'Forum actions', 'Show answer', 'Link clicked',
                                    'Total time', 'Study time', 'Sessions number', 'Average session time',
                                    'Go back number', 'In tab visited', 'Number tabs visited', 'Jump number',
                                    'Average jump number', 'Average video watched time', 'Number speed clicks',
                                    'Average forward seek', 'Average backward seek', 'Videos watched',
                                    'Average pause number', 'Average rewatch video', 'Average attempts number',
                                    'Success number', 'Tasks number', 'Result'])

    print("To save input table to csv file, enter wanted path, otherwise just press enter: ")
    save_file_path = input()

    # Save data to the wanted file
    if save_file_path != "":
        try:
            data_frame.to_csv(save_file_path)
        except IOError:
            print("The path for saving is incorrect, table wasn`t saved")

    return data_frame


# Convert logs into input data table, save it in .csv file if save_filter_path != "" and return input table
def get_and_convert_checking_logs():
    users, X = get_users_matrix()

    names_list = list(users.keys())
    names_list.sort()

    # Create data frame
    XT = [*zip(*X)]
    users_data = {'Usernames': names_list,
                  'Logs number': XT[0],
                  'Forum actions': XT[1],
                  'Show answer': XT[2],
                  'Link clicked': XT[3],
                  'Total time': XT[4],
                  'Study time': XT[5],
                  'Sessions number': XT[6],
                  'Average session time': XT[7],
                  'Go back number': XT[8],
                  'In tab visited': XT[9],
                  'Number tabs visited': XT[10],
                  'Jump number': XT[11],
                  'Average jump number': XT[12],
                  'Average video watched time': XT[13],
                  'Number speed clicks': XT[14],
                  'Average forward seek': XT[15],
                  'Average backward seek': XT[16],
                  'Videos watched': XT[17],
                  'Average pause number': XT[18],
                  'Average rewatch video': XT[19],
                  'Average attempts number': XT[20],
                  'Success number': XT[21],
                  'Tasks number': XT[22]}

    data_frame = DataFrame(users_data,
                           columns=['Usernames', 'Logs number', 'Forum actions', 'Show answer', 'Link clicked',
                                    'Total time', 'Study time', 'Sessions number', 'Average session time',
                                    'Go back number', 'In tab visited', 'Number tabs visited', 'Jump number',
                                    'Average jump number', 'Average video watched time', 'Number speed clicks',
                                    'Average forward seek', 'Average backward seek', 'Videos watched',
                                    'Average pause number', 'Average rewatch video', 'Average attempts number',
                                    'Success number', 'Tasks number'])

    print("If you want to save checking table to csv file, enter wanted path, otherwise just press enter: ")
    save_file_path = input()

    # Save data to the wanted file
    if save_file_path != "":
        try:
            data_frame.to_csv(save_file_path)
        except IOError:
            print("The path for saving is incorrect, table wasn`t saved")

    return data_frame


# Gets data from .csv file by given path, returns input table
def upload_ready_table():
    print("Enter the path to the file that contains wanted table; it must be .csv " +
          "with top row of features names and the first column of names")
    path = input()

    try:
        bank_data = pd.read_csv(path)
    except IOError:
        print("The input table file isn`t found, check the path")
        return
    return bank_data.drop(columns=['Unnamed: 0'])


# Get the results for current students
def check_current_users(training_table, tested_table):
    # Get proper input table
    XX = training_table.drop(columns=['Usernames', 'Logs number', 'Link clicked', 'Total time', 'Study time',
                                      'Sessions number', 'Average session time', 'Number tabs visited', 'Jump number',
                                      'Average jump number', 'Number speed clicks', 'Average forward seek',
                                      'Average backward seek', 'Average pause number', 'Result'])

    # Get proper tested table
    usernames = tested_table['Usernames']
    tested_table = tested_table.drop(columns=['Usernames', 'Logs number', 'Link clicked', 'Total time', 'Study time',
                                              'Sessions number', 'Average session time', 'Number tabs visited',
                                              'Jump number', 'Average jump number', 'Number speed clicks',
                                              'Average forward seek', 'Average backward seek', 'Average pause number'])

    # Get proper output table
    yy = (training_table['Result'])

    # Create classifier and train it
    clf = DecisionTreeClassifier()
    clf = clf.fit(XX, yy)

    # Get the result of new data classified
    prediction_table = clf.predict(tested_table)

    answer_table = tested_table
    answer_table['Result'] = prediction_table
    answer_table['Usernames'] = usernames
    return answer_table


# Add an example to the table
def add_example(new_username, new_table):
    # Find in new table wanted data by username and add it to the old table by file path
    if new_username in new_table['Usernames'].values:
        old_table = upload_ready_table()
        new_row = new_table.loc[new_table['Usernames'] == new_username]
        united_table = pd.concat([old_table, new_row], sort=False)

        print("Enter the path, where to download table with new row")
        new_path = input()
        try:
            united_table.to_csv(new_path)
        except IOError:
            print("The path for saving is incorrect, table wasn`t saved")
    else:
        print("There is no user with such username in the table")


# User menu
print("This is CheatCheck")
print("Choose the way to import training set:")
print("1 - From set of unsorted logs and answer table")
print("2 - Upload ready table .csv")
print("Enter your choice:")
choice = input()

training_set = DataFrame()
if choice == "1":
    training_set = get_and_convert_training_logs()
elif choice == "2":
    training_set = upload_ready_table()
else:
    print("You wrote the wrong number")

print("Choose the way to import info about new users:")
print("1 - From set of unsorted logs")
print("2 - Upload ready table without results .csv")
print("Enter your choice:")
choice = input()

checking_set = DataFrame()
if choice == "1":
    checking_set = get_and_convert_checking_logs()
elif choice == "2":
    checking_set = upload_ready_table()
else:
    print("You wrote the wrong number")

current_results = check_current_users(training_set, checking_set)

import pandas as pd
pd.set_option('display.max_rows', 10000)
print("To print the result, enter 'print', otherwise press enter")
if input() == 'print':
    print(current_results[['Usernames', 'Result']])

print("To add some new results to the training set, enter true, otherwise press enter")
answer = input()
while answer == "true":
    print("Enter username of the user you`d like to add to the training set")
    username = input()
    checking_set['Result'] = current_results['Result']
    add_example(username, checking_set)

    print("To add some new results to the training set, enter true, otherwise press enter")
    answer = input()

print("To save table with results, enter the path, otherwise press enter")
save_path = input()
# Save data to the wanted file
if save_path != "":
    try:
        checking_set['Result'] = current_results['Result']
        checking_set.to_csv(save_path)
    except IOError:
        print("The path for saving is incorrect, table wasn`t saved")
