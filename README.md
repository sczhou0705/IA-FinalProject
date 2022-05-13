# IA-FinalProject

Motivation:
The need for communicating and maintaining a secure exclusive, and private social network with alumni exists for Yeshiva University’s Katz School of Science and Health. Since this is a relatively small yet prestigious school, we can create a system where students keep in contact with each other via a medium that only they can access. Their Linkedin accounts and current job title can be edited at any time, and we can infer their salary. It allows the students to maintain all the data related to their courses, groups they may be associated with, career interests, skill sets, and potential internship opportunities with alumni. Students can manage a profile and see their relationships using a connected collection of information from the Registrar, admissions, alumni, and LinkedIn datasets. It can also help build a network between the current students and the alumni. By signaling their interests and identifying alumni with a trajectory that appeals to the student, they can model their experience as alumni. 

In the final project, we utilize AWS lambda, s3 bucket, Glue, RDS, Neptune services, etc. 

### Step 1 : Design AWS infrastructure

![image](https://github.com/sczhou0705/IA-FinalProject-YUconnect/blob/main/image/diagram_updated.png)

### Step 2: Create student dummy dataset and web scrapping linkedIn and Salary

### Step 3: Construct Neptune graph databases.
Gremlin csv Example: ![image](https://github.com/sczhou0705/IA-FinalProject-YUconnect/blob/main/image/csvGremlin.png)

Network graph Example : 
![image](https://github.com/sczhou0705/IA-FinalProject-YUconnect/blob/main/image/network%20graph%20sample.png)

### Step 4: Upload datasets into MYSQL through AWS RDS and glue services.
!! Neptune can not directly be connected with Tableau, so we use RDS as a bridge to connect Tableau.
![image](https://github.com/sczhou0705/IA-FinalProject-YUconnect/blob/main/image/schema.png)

### Step 5: Connect to Tableau and do visualization analysis.

### Challenge and Solution:
![image](https://github.com/sczhou0705/IA-FinalProject-YUconnect/blob/main/image/Challenge.png)

