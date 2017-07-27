# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


from clean_data import *
from sklearn.externals import joblib
import numpy as np
import csv
from nltk.corpus import stopwords
import os, re, nltk
import glob
import codecs



# importing Visualization module
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# importing csv module
import csv

import pygal


filename = './save/topic_classifier.joblib.pkl'
text_clf = joblib.load(filename)

count_category = {}


# csv file name
#csvfilename = "final.csv"

csvfilename = "likesInfo/"+sys.argv[1]


# initializing the titles and rows list
fields = []
rows = []

# reading csv file
with open(csvfilename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = csvreader.next()

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    # get total number of rows
    print("Total no. of rows: %d"%(csvreader.line_num))

# printing the field names
print('Field names are:' + ', '.join(field for field in fields))

#  printing first 5 rows
print('\nAll rows are:\n')
for row in rows[:]:
    # parsing each column of a row
    # print row[1:]
    current_row = ''.join(row[1:])
    print 'prediction for row : '
    cleaned = clean_data_from_text(current_row, remove_stopwords=True, stemming=True, extract_noun=False)
    print cleaned.encode("utf-8")
    predicted = text_clf.predict([cleaned])

    for prediction in predicted:

        print prediction.encode("utf-8")

        if not prediction in count_category:
            count_category[prediction] = 1
        else:
            count_category[prediction] += 1
    # for col in row:
    #     print(col),
    # print('\n')


print 'counts'
print count_category


labels = []
sizes = []
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'pink', 'green', 'red']
# explode = (0.1, 0, 0, 0, 0,0,0)  # explode 1st slice

for category, count in count_category.items():
    labels.append(category)
    sizes.append(count)

centre_circle = plt.Circle((0,0),0.0,color='black', fc='white',linewidth=1.25)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Data to plot
# labels = 'Business', 'Entertainment', 'US', 'Health', 'Sci_Tech', 'World', 'Sport'
# sizes = [215, 130, 245, 210, 200, 210, 230]

# Plot
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.savefig("chartimg.png")
#plt.show()


#test = "Sean Hannity hosts 'Hannity' on the Fox News Channel and 'The Sean Hannity Show,' the second most listened to radio talk show in America."

#cleaned = clean_data_from_text(test, remove_stopwords=True, stemming=True, extract_noun=False)
#print cleaned
#predicted = text_clf.predict([cleaned])
#print predicted

# cleaned = clean_data(df=raw, remove_stopwords=True, stemming=True, extract_noun=False)
# predicted = text_clf.predict(cleaned.text)
# print np.mean(predicted == cleaned.category)
