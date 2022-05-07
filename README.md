# ASR-Hacker

## Team Members
### Kritti Sharma (18010060)
### Shreyas Chandgothia (180260037)
### Parth Sangani (18D100014)


This work has been done as a part of the Hacker-Seminar-Presentations of the course CS753 : Automatic Speech Recognition taught by Prof Preethi Jyothi.

An implementation of the "Literal Determination" part of the paper : https://dl.acm.org/doi/pdf/10.1145/3318464.3389777. We have implemented this from scratch since no open source code was available.


## Instructions to run the code : 

1. python3 literalFinder.py : The dictionary which contains the table names, attribute names and attribute values is manually loaded inside the code.

2. python3 generatePickle.py : It generates 2 pickle files, data.pkl corresponding to databases in the "Database-CSV" directory. These are dummy databases handcrafted by us. The second file, data-large.pkl corresponds to databases in "Database-CSV-Large" directory, these are real databases.

3. python3 literalFinderWithCSV.py : It uses the "data.pkl" file generated from step 2 to read the table names, attribute names and attribute values.

4. python3 literalFinderWithCSVLarge.py : It uses the "data-large.pkl" file generate from step 2 to read the table names, attribute names and attribute values.

There are 8 example queries in literalFinder.py and literalFinderWithCSV.py, 6 example queries in literalFinderWithCSVLarge.py. The current output is as per expectations but since our implementation uses edit distance metric, it may so happen that you may get an output which deviates from expectation upon changing the query (especially when attribute values are involved)


The database structure assumed by literalFinder.py file is as follows - 
1. Employees.csv (ID,FirstName,LastName)
2. Salaries.csv (Employee_ID,Salary)


## Structure of the Database-CSV directory : 

1. Employees.csv (ID,FirstName,LastName)
2. Salaries.csv (Employee_ID,Salary)


## Structure of the Database-CSV directory : 

1. Employees.csv (EMPLOYEE_ID,FIRST_NAME,LAST_NAME,PHONE_NUMBER)
2. Salaries.csv (EMPLOYEE_ID,HIRE_DATE,JOB_ID,SALARY,MANAGER_ID,DEPARTMENT_ID)