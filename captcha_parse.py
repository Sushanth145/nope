import datetime, requests
from bs4 import BeautifulSoup
VTOP_BASE_URL = r"https://vtop2.vitap.ac.in/vtop/"
VTOP_LOGIN = r"https://vtop2.vitap.ac.in/vtop/vtopLogin"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}
VTOP_DO_LOGIN = r"https://vtop2.vitap.ac.in/vtop/doLogin"
PROFILE = r"https://vtop2.vitap.ac.in/vtop/studentsRecord/StudentProfileAllView"
MARKS = r"https://vtop2.vitap.ac.in/vtop/examinations/doStudentMarkView"
TIMETABLE = r"https://vtop2.vitap.ac.in/vtop/processViewTimeTable"
ACADHISTORY = r"https://vtop2.vitap.ac.in/vtop/examinations/examGradeView/StudentGradeHistory"

from collections import namedtuple

from utility import solve_captcha
# from crypto import magichash
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from constants import *

from insert import insert_marks ,insert_timetable ,insert_acadhistory
from vtop_parser import parse_attendance, parse_timetable, parse_acadhistory, parse_profile, parse_marks
# from crypto import magichash

def get_timetable(sess, username):
    """
    Returns Timetable 
    Format of timetable : {
        "Monday": [
            {
                "slot" : "A1",
                "courseName" : "Computer Communication",
                "code" : "ECE4008",
                "class" : "AB1 408",
                startTime: "8:00",
                endTime:"8:50"
            }
        ]
    }
    """
    payload = {
        "semesterSubId" : "AP2023242",        # Filled for Winsem
        "authorizedID" : username,
        "x" : datetime.datetime.now(datetime.timezone.utc).strftime("%c GMT")   # GMT time
    }
    status = True
    days = {}
    final_dict = {}
    try:
        timetable_sess = sess.post(TIMETABLE, data=payload, headers=HEADERS, verify=False)
        # Check for 200 CODE
        if timetable_sess.status_code !=200:
            status = False
    except:
        status = False
    finally:
        timetable_html = timetable_sess.text
        # try:
        #     days, final_dict = parse_timetable(timetable_html)
        # except Exception as e:
        #     print(e)
        #     status = False
        # finally:
            # if(insert_timetable(id, days, final_dict)):
            #     status = True
            # else:
            #     status = False
    
            # return (days, final_dict, True)
        return(timetable_html)

def generate_session(username, password):
    """
    This function generates a session with VTOP. Solves captcha and returns Session object
    """
    
    sess = requests.Session()
    # VTOP also not secure
    sess.get(VTOP_BASE_URL,headers = HEADERS, verify= False)
    login_html = sess.post(VTOP_LOGIN,headers = HEADERS, verify= False).text
    alt_index = login_html.find('src="data:image/png;base64,')
    alt_text = login_html[alt_index+5:] 
    end_index = alt_text.find('"')
    captcha_src = alt_text[:end_index]
    captcha = solve_captcha(captcha_src,username)
    payload = {
        "uname" : username,
        "passwd" : password,
        "captchaCheck" : captcha
    }
    post_login_html = sess.post(VTOP_DO_LOGIN, data=payload, headers=HEADERS, verify=False).text
    
    valid = True
    
    try:
        soup = BeautifulSoup(post_login_html, 'lxml')
        code_soup = soup.find_all('div', {"id": "captchaRefresh"})
    except Exception as e:
        print(e)
        valid = False
    finally:
        if(len(code_soup)!=0):
            valid = False
        # lala = get_timetable
        # print(lala)
        return (sess,valid)

def get_acadhistory(sess,username):
    """
    Returns Academic History of Student or Grade History
    Format is {
        subjects : {
            subjectName : grade
            ...
        },
        summary:{
            "CreditsRegistered" : Num,
            "CreditsEarned" : Num,
            "CGPA" : str,
            "S" : Num
            "A" : Num,
            ...
        }
    }
    """

    # Payload for Academic History.
    payload = {
        "verifyMenu" : "true",        
        "winImage" : "undefined",
        "authorizedID": username,
        "nocache" : "@(new Date().getTime())"   
    }
    status = True
    grades = {}
    try:
        acad_sess = sess.post(ACADHISTORY, data=payload, headers=HEADERS, verify=False)
        # Check for 200 CODE
        if acad_sess.status_code !=200:
            status = False
    except:
        status = False
    finally:
        acad_html = acad_sess.text
        try:
            grades = parse_acadhistory(acad_html)
        except Exception as e:
            print(e)
            status = False
        finally:
            # if(insert_acadhistory(id, grades["subjects"], grades["summary"])):
            #     status = True
            # else:
            #     status = False
            status = True    
            return (grades, status)

def get_acadhistory(sess,username):
    """
    Returns Academic History of Student or Grade History
    Format is {
        subjects : {
            subjectName : grade
            ...
        },
        summary:{
            "CreditsRegistered" : Num,
            "CreditsEarned" : Num,
            "CGPA" : str,
            "S" : Num
            "A" : Num,
            ...
        }
    }
    """

    # Payload for Academic History.
    payload = {
        "verifyMenu" : "true",        
        "winImage" : "undefined",
        "authorizedID": username,
        "nocache" : "@(new Date().getTime())"   
    }
    status = True
    grades = {}
    try:
        acad_sess = sess.post(ACADHISTORY, data=payload, headers=HEADERS, verify=False)
        # Check for 200 CODE
        if acad_sess.status_code !=200:
            status = False
    except:
        status = False
    finally:
        acad_html = acad_sess.text
        try:
            grades = parse_acadhistory(acad_html)
        except Exception as e:
            print(e)
            status = False
        finally:
            # if(insert_acadhistory(id, grades["subjects"], grades["summary"])):
            #     status = True
            # else:
            #     status = False
            status = True

    
            return (grades, status)
