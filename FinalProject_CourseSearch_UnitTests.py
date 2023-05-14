'''
Asongafac Asaha, Ali Khalid, Gabynelle Kwekam.
University of Maryland, INST326, Prof.Pauw

This file performs several unit test assertions for the class and functions
found within the FinalProject_CourseSearch.py file.
'''

import FinalProject_CourseSearch
from FinalProject_CourseSearch import (create_visual, parseCourseTags, getCourses,
                                       Course, getCourseGPA, checkKeywords, search)


#Test Cases --------------------------------------------------------
def test_Course_init():
    '''Unit Test for the Course object __init__() fucntion'''
    
    coursey = Course("INST326", "Title", 3, ["None"], "N/A", 3.50)

    #Asserting all the attributes were correctly applied.
    assert coursey.course_name == "INST326"
    assert coursey.title == "Title"
    assert coursey.course_credits == 3
    assert coursey.genEdSatisfactions[0] == "None"
    assert len(coursey.genEdSatisfactions) == 1
    assert coursey.description == "N/A"
    assert coursey.GPA == 3.5

def test_Course_repr():
    '''Unit Test for the Course object __repr__() fucntion'''
    
    coursey = Course("INST326", "Title", 3, ["None"], "N/A", 3.50)
    test_text = "INST326 Title\nCredits: 3\nGenEds: |None|\nAverage GPA: 3.5\nDesc:\nN/A"

    #Asserting that the string representation matches the way we intended.
    assert coursey.__repr__() == test_text
    
def test_Course_frame_form():
    '''Unit Test for the Course object frame_form() fucntion'''
    
    coursey = Course("INST326", "Title", 3, ["None"], "N/A", 3.50)
    courseDict = coursey.frame_form()

    #Testing that we can call the frame_form function and correclt use it returned
    #value as a dictionary, with the correct values being returned on request.
    assert courseDict["Course"] == "INST326"

def test_getCourseGPA():
    '''Unit Test for the getCourseGPA() fucntion'''
    
    coursey = Course("INST326", "Title", 3, ["None"], "N/A", 3.50)
    getCourseGPA([coursey])

    #Checking to see that the GPA was updated and matches that on PlanetTerp.
    assert coursey.GPA == 3.06

def test_checkKeywords():
    '''Unit Test for the checkKeywords() fucntion'''
    
    title_text = "Human-Centered Cybersecurity"
    keywords = ["cyber", "human", "Systems"]

    #A number of different test courses, some which fit keywords, some which dont.
    coursey = Course("INST326", "Title", 3, ["None"], "Ha", 3.50)
    coursey2 = Course("INST364", title_text, 3, ["None"], "Cybersecurity", 3.50)
    coursey3 = Course("INST399", "Nope", 3, ["None"], "Uh-uh", 3.50)
    coursey4 = Course("INST391", "Systems", 3, ["None"], "Made This Up", 3.50)

    #Checking to make sure the keyword finder correctly flagged each course title and
    #description. False means there were no matches, True means there was one or more.
    assert checkKeywords(coursey.title, keywords) == False
    assert checkKeywords(coursey.description, keywords) == False
    
    assert checkKeywords(coursey2.title, keywords) == True
    assert checkKeywords(coursey2.description, keywords) == True
    
    assert checkKeywords(coursey3.title, keywords) == False
    assert checkKeywords(coursey3.description, keywords) == False
    
    assert checkKeywords(coursey4.title, keywords) == True
    assert checkKeywords(coursey4.description, keywords) == False

def test_search():
    '''Unit Test for the search() fucntion'''
    
    page_text = search("Inst", "Summer 2023")
    page_text2 = search("", "Summer 2023")

    #A the search in page_text should yield only INST courses. The following find
    #statements check for terms found within the webpage of the INST courses.
    assert page_text.find("INST364") >= 0
    assert page_text.find("Project Management for Information Science") >= 0
    assert page_text.find("Must be in Technology and Information Design") >= 0
    assert page_text.find("Donkey kicker") < 0

    #A the search in page_text2 should yield a page with all the course tags present. 
    #The following find statements check for tags of several courses.
    assert page_text2.find("Donkey kicker") < 0
    assert page_text2.find("BMGT") >= 0
    assert page_text2.find("GEOL") >= 0

def test_parseCourseTags():
    '''Unit Test for the parseCourseTags() fucntion'''
    
    page_text = search("", "Summer 2023")

    #A search in page_text should yield courses and course information from all course
    #tags. The following find statements check for terms within the webpages and course
    #information of several tags and courses.
    assert page_text.find("INST364") >= 0
    assert page_text.find("Education") >= 0
    assert page_text.find("GVPT200") >= 0
    assert page_text.find("ENGL393") >= 0
    assert page_text.find("Subversive Cultures and Performance") >= 0

def test_getCourses():
    '''Unit Test for the getCourses() fucntion'''
    
    page_text = search("Inst", "Summer 2023")
    keywords = ["cyber", "human", "Systems"]
    keywords2 = []

    #One list shoudl produce a list with only Summer INST courses matching the keywords.
    test_list = getCourses(page_text, keywords)
    #Another lsit should produce a lsit with all Summer INST courses.
    test_list2 = getCourses(page_text, keywords2)

    #The first list should meet these parameters.
    assert len(test_list) == 4
    assert test_list[0].course_name == "INST311"
    assert test_list[3].course_name == "INST462"

    #The second list should meet these parameters.
    assert len(test_list2) == 35
    assert test_list2[0].course_name == "INST126"
    assert test_list2[16].course_name == "INST453"
    assert test_list2[34].course_name == "INST899"

#Running Tests -----------------------------------------------------
test_Course_init()
test_Course_repr()
test_Course_frame_form()
test_getCourseGPA()
test_checkKeywords()
test_search
test_parseCourseTags()
test_getCourses()
