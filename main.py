import pandas as pd
import numpy as np

#Quiz Totals

Quiz1 = pd.read_csv("D:\Code\Python\Data Science\Grader\data\quiz_1_grades.csv").set_index("Email")
Quiz2 = pd.read_csv("data\quiz_2_grades.csv").set_index("Email")
Quiz3 =pd.read_csv("data/quiz_3_grades.csv").set_index("Email")
Quiz4 = pd.read_csv("data\quiz_4_grades.csv").set_index("Email")
Quiz5 = pd.read_csv("data\quiz_5_grades.csv").set_index("Email")
Quiz1 = Quiz1.assign(GradeQ2=Quiz2["Grade"],GradeQ3=Quiz3["Grade"],GradeQ4=Quiz4["Grade"],GradeQ5=Quiz5["Grade"])
Quiz1["Total"] = Quiz1["GradeQ2"] + Quiz1["GradeQ3"]+ Quiz1["GradeQ4"] + Quiz1["GradeQ5"] + Quiz1["Grade"]
dfQuiz = Quiz1
dfQuiz["OutOf"]= 100




ExamMain = pd.read_csv("data/hw_exam_grades.csv").set_index("SID")
sec1 = pd.read_csv("data/Section 1 Grades.csv")
sec2 = pd.read_csv("data/Section 2 Grades.csv")
sec3  =pd.read_csv("data/Section 3 Grades.csv")
allSec = pd.concat([sec1,sec2,sec3])






studentDetails = pd.DataFrame(allSec.loc[:,["SID","Section","Email","First Name","Last Name"]]).set_index("Email")
# sID = pd.Series(data=allSec.index,index=studentDetails.index)
# studentDetails["SID"] =sID
# studentDetails= studentDetails.set_index("SID").merge(allSec["Email"],how="left",on="SID").set_index("Email")

# studentDetails["Quiz Total"] = dfQuiz["Total"]

ID_Mail = allSec.loc[:,["SID","Email"]].set_index("SID")

 
dfHomework = ExamMain.filter(regex="Homework \d{1,2}$",axis=1).copy(deep=True)
dfHomework= dfHomework.merge(ID_Mail["Email"],how="left",on="SID")


dfHomework = dfHomework.iloc[:,0:10].copy(deep=True)
dfHomework["Total"] = dfHomework.sum(axis=1)
dfHomework["OutOf"] = 740

dfExam = ExamMain.filter(regex="Exam \d$",axis=1).copy(deep=True)
dfExam['Total']= dfExam.sum(axis=1)
dfExam["OutOf"] = 300

dfQuiz["SID"] = studentDetails["SID"]
dfQuiz =dfQuiz.set_index("SID")
studentDetails = studentDetails.set_index("SID")

studentDetails["QuizTotal"] =dfQuiz["Total"]
studentDetails["Exam Total"]= dfExam["Total"]
studentDetails["HomeWork Total"] = dfHomework["Total"]
studentDetails["Score"] = round(studentDetails.loc[:,["QuizTotal","Exam Total","HomeWork Total"]].sum(axis=1).div(1140).mul(100))

gradingSystem = [0,39,54,69,84,100]
gradess = ["E","D","C","B","A"]

studentDetails["Scores"] = pd.cut(studentDetails["Score"],bins=gradingSystem,labels=gradess,right=True)


studentDetails.to_excel("Graded.xlsx", sheet_name='Results', index=False)

print(studentDetails)







   
    



