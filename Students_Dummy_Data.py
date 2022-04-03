#!/usr/bin/env python
# coding: utf-8

# # DAV 6100 Information Architectures Final Project

# ## Ramdonly generating student names

# In[1]:


import names
import pandas as pd
import numpy as np
import random
from functools import reduce


# In[2]:


nr_of_students = 100
students = []
for students_id in range(nr_of_students):
    lastname = names.get_last_name()
    firstname = names.get_first_name()
    students.append([lastname, firstname])
df = pd.DataFrame(students, columns=['First Name','Last Name', ])
df.head(5)


# In[ ]:


## Assign student's major in Katz school


# In[3]:


df['Katz School Major'] = np.random.choice(['Data Analytics and Visualization', 'Artificial Intelligence'], size = len(df), p = [0.7, 0.3])
df.head(5)


# ## Assign student's Graduation Semesters

# In[4]:


Graduation_Semesters = [
    'Spring-2017', 'Summer-2017', 'Fall-2017',
    'Spring-2018', 'Summer-2018', 'Fall-2018',
    'Spring-2019', 'Summer-2019', 'Fall-2019',
    'Spring-2020', 'Summer-2020', 'Fall-2020',
    'Spring-2021', 'Summer-2021', 'Fall-2021',
    'Spring-2022', 'Summer-2022', 'Fall-2022',
    'Spring-2023', 'Summer-2023', 'Fall-2023']

#Randomly select 100 elements from list with replacement and return a list
Graduation_Semester = random.choices(Graduation_Semesters, k=100)


# In[5]:


# Append new list into existing dataframe and assign a column name
df['Graduation Semester'] = Graduation_Semester
df.head(5)


# In[ ]:


## Assign student's Country of Origin


# In[6]:


df['Country of Origin'] = np.random.choice(['USA', 'China', 'India', 'Pakistan','Other'], size = len(df), p = [0.3, 0.4, 0.15, 0.10, 0.05])
df.head(5)


# ## Assign student's languages

# In[7]:


languages = []

usa_languages = ['English','Spanish']
china_languages = ['Mandarin','Cantonese','Wu']
pakistan_languages = ['Punjabi','Pashto','Sindhi']
india_languages = ['Hindi', 'Gujarati', 'Marathi', 'Bengali','Malayalam']
other_languages = ['French','Russian','Hebrew','Portuguese','Arabic','Other']

cor = df['Country of Origin']

for i in range(len(cor)):
    if cor[i] == 'USA':
        languages.append(np.random.choice(usa_languages,1,p=[.78,.22]).tolist()[0])
    if cor[i] == 'China':
        languages.append(np.random.choice(china_languages,1,p=[.80,.15,.05]).tolist()[0])
    if cor[i] == 'Pakistan':
        languages.append(np.random.choice(pakistan_languages,1,p=[.70,.10,.20]).tolist()[0])
    if cor[i] == 'India':
        languages.append(np.random.choice(india_languages,1,p=[.70,.08,.09,.05,.08]).tolist()[0])
    if cor[i] == 'Other':
        languages.append(np.random.choice(other_languages).tolist()[0])

df['Languages'] = languages
df.head(5)


# ## Assign student's Undergraduate Majors

# In[8]:


df['Undergraduate Major'] = np.random.choice(['Mathematics', 'Computer Science', 'Engineering', 'Health Sciences','Other'], 
                                  size = len(df), p = [0.25, 0.45, 0.15, 0.10, 0.05])
df.head(5)


# In[9]:


courses_AI = [
    'Data Acquisition and Management',
    'Computational Statistics and Probability',
    'Numerical Methods',
    'Predictive Models',
    'Machine Learning',
    'Artificial Intelligence',
    'Neural Networks and Deep Learning',
    'AI Capstone: R&D Experience']

courses_DAV = ['DAV 5000 Business Modeling and Data Analysis',
    'DAV 5100 Structured Data Management',
    'DAV 5200 Visual Design and Storytelling',
    'DAV 5300 Computational Math and Statistics',
    'DAV 5400 Analytics Programming',
    'MAN 5580 Project Management',
    'DAV 6500 Capstone']

courses_electives = [ 'Bayesian Methods',
    'AI Product Studio',
    'Natural Language Processing',
    'Data Visualization',
    'Advanced Data Engineering',
    'Complex Systems: Financial Time Series Analysis',
    'Special Topics',
    'Independent Study',
    'Internship'
    'AI Product Studio',
    'DAV 6000 Talent Analytics',
    'DAV 6050 Data-Driven Organizations',
    'DAV 6100 Information Architectures',
    'DAV 6150 Data Science',
    'DAV 6200 Data Product Design',
    'DAV 6300 Special Topics',
    'DAV 6400 Internship',
    'DAV 6450 Independent Study']

ksm = df['Katz School Major'] 
df['Courses'] = df.apply(lambda _: '', axis=1)

for i in range(len(ksm)):
    
    dav_courses = []
    ai_courses = []
    dav_electives = list(np.random.choice(courses_electives, size = 5, replace=False))
    ai_electives = list(np.random.choice(courses_electives, size = 4, replace=False))
    
    if ksm[i] == 'Data Analytics and Visualization':
        list1 = courses_DAV+dav_electives
        random.shuffle(list1)
        dav_courses.append(list1)
        df.iat[i, df.columns.get_loc('Courses')] = reduce(lambda x, y: x+y, dav_courses) 
        
    if ksm[i] == 'Artificial Intelligence':
        list2 = courses_AI+ai_electives
        random.shuffle(list2)
        ai_courses.append(list2)
        df.iat[i, df.columns.get_loc('Courses')] = reduce(lambda x, y: x+y, ai_courses) 
        


# In[10]:


df.head(5)


# ## Course Semesters

# In[11]:


Starting_Semesters = ['Spring-2016','Summer-2016','Fall-2016']


# In[12]:


'''In this cell we ensure that each of the classes a student takes is acounted for with '''

df['Course Semesters'] = df.apply(lambda _: '', axis=1)

gs = df['Graduation Semester']

for i in range(len(df['Graduation Semester'])):
    course_dates = []
    if gs[i] == 'Spring-2017':
        courses_dates = Starting_Semesters + list([ 'Spring-2017'])
        courses_dates1 = [element for element in courses_dates for i in range(3)]
        df.iat[i, df.columns.get_loc('Course Semesters')] = courses_dates1
        
for i in range(len(df['Graduation Semester'])):
    course_dates = []
    if gs[i] == 'Summer-2017':
        courses_dates = list([Starting_Semesters[1], Starting_Semesters[2]]) + list(['Spring-2017'+'Summer-2017']) 
        courses_dates1 = [element for element in courses_dates for i in range(3)]
        df.iat[i, df.columns.get_loc('Course Semesters')] = courses_dates1

for i in range(len(df['Graduation Semester'])):
    course_dates = []
    if gs[i] == 'Fall-2017':
        courses_dates = list([Starting_Semesters[2]]) + list(['Spring-2017'+'Summer-2017'+'Fall-2017']) 
        courses_dates1 = [element for element in courses_dates for i in range(3)]
        df.iat[i, df.columns.get_loc('Course Semesters')] = courses_dates1

for i in range(len(Graduation_Semesters)-3):
    for j in range(len(gs)):
        course_dates = []
        if Graduation_Semesters[i+3] == gs[j] :
            courses_dates = list([Graduation_Semesters[i]]) + list([Graduation_Semesters[i+1]]) + list([Graduation_Semesters[i+2]]) + list([Graduation_Semesters[i+3]])

            courses_dates1 = [element for element in courses_dates for i in range(3)]
            df.iat[j, df.columns.get_loc('Course Semesters')] = courses_dates1   
      


# In[13]:


df.head(5)


# In[14]:


len(df['Course Semesters'][0])


# In[15]:


len(df['Courses'][0])


# ## Student ID

# In[16]:


#Unique Identifiers

# generte ids
ids = np.random.randint(low=1e9, high=1e10, size = len(df['First Name']))

# add new id column to first column
df.insert(0, "Student ID", list(ids))
df.head(5)


# ## GPA

# In[17]:


#List of GPA values for the DataFrame 
gpa = np.random.normal(3.5, .4, size=(1, len(df['First Name'])))

#Ensure the maximum is 4.0 GPA
gpa[gpa > 4] = 4.0

#Shorten each value to 2 decimal places
gpa1 = np.around(gpa,2)

#Add this array to the dataframe
df.insert(4, "GPA", gpa1.tolist()[0])
df.head(5)


# ## Age

# In[18]:


#Age at Graduation

ages = [i for i in range(23,35)]
probs_ages = [.2,.215,.15,.1,.1,.05,.05,.035,.035,.025, .025, .015]
df['Age at Graduation'] = np.random.choice(ages, size = len(df), p = probs_ages)
df.head(5)


# In[19]:


#Years of Experience

yearsofexperience = []

for i in df['Age at Graduation']:
    step = [0,.5,1,1.5]
    j = i - 22 + random.choice(step)
    yearsofexperience.append(j)
    
df['Years of Experience'] = yearsofexperience
df.head(5)


# In[20]:


#Location

locations = ['New York, NY','Chicago, IL','Woodbridge, NJ','San Francisco, CA','Los Angeles, CA','Bridgeport, CT']


probs_loc = [.7,.05,.15,.04,.03,.03]
df['Location'] = np.random.choice(locations, size = len(df), p = probs_loc)
df.head(5)


# In[21]:


jobdesc = ['Entry Data Analyst',
 'Data Scientist I',
 'Machine Learning Engineer',
 'Business Intelligence (BI) Developer',
 'Entry Level Python Developer',
 'UX Design Intern',
 'Data Architect I',
 'Big Data Architect',
 'Database Administrator - Entry',
 'Entry Business Systems Analyst']

jobs = []
for i in range(len(df)):
    jobs.append(np.random.choice(jobdesc))
    jobs

df['Job Decription'] = jobs
df.head(5)


# In[22]:


'''We can apply this function to any row to get the merged list of Courses and Semester of that course, which we 
will eventually use for connections with other students in the graph database.'''

def merged_course_semester(i):
    courses = df.loc[i]['Courses']
    semesters = df.loc[i]['Course Semesters']
    merged = []
    for i in range(len(courses)):
        merged.append([semesters[i],courses[i]])
    return merged

def merged_semester_list(i):
#Index of the dataframe row is i
    list1 = []
    for j in range(12):
        h = merged_course_semester(i)[j][0]+' '+merged_course_semester(i)[j][1]
        list1.append(h)
    return list1

merged_semester_list(3)


# In[23]:


transcripts = []
for i in range(len(df)):
    transcripts.append(merged_semester_list(1))
    
transcripts
df['Transcript'] = transcripts


# In[24]:


df = df.drop(['Courses', 'Course Semesters'], axis=1)
df.head(5)


# ## Export dataframe into a csv file

# In[27]:


import csv

# Create student info csv
fields = [
    'Student ID',
    'First Name',
    'Last Name',
    'Katz School Major',
    'GPA',
    'Graduation Semester',
    'Country of Origin',
    'Languages',
    'Undergraduate Major',
    'Age at Graduation',
    'Years of Experience',
    'Location',
    'Job Decription',
    'Transcript'
] 
rows = df.values.tolist()
with open('students.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(rows)


# ## Import csv file into S3 bucket

# In[33]:


import s3fs
###LOAD THE FILE INTO S3####
# prepare csv file name   
pathname = 'ia-final-project/'#specify location of s3:/{my-bucket}/
filenames = f"{pathname}students_data.csv" #name of the filepath and csv file

#encoding must be adjusted to accommodate abnormal characters. Use s3fs to write to S3 bucket
print("Start adding salary data to csv")
byte_encoded_df = df.to_csv(None, index=False).encode() #encodes file as binary
s3 = s3fs.S3FileSystem(anon=False)
with s3.open(filenames, 'wb') as file:
    file.write(byte_encoded_df) #writes byte-encoded file to s3 location

#print success message
print("Successfull uploaded file to location:"+str(filenames))
print("Complete running StudentsDummyData")


# In[ ]:




