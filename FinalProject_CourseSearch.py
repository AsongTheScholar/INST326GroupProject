'''
Asongafac Asaha, Ali Khalid, Gabynelle Kwekam.
University of Maryland, INST326, Prof.Pauw
Final Project: Course Search Tool

This file provides the Course object and supplementary functions. These will be used to create a program to allow a user
to search through UMD's Schedule Of Classes for specific tags as well as keywords. Users are also able to automatically
cross view the courses with their average GPA on PlanetTerp.
'''

import requests
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import sys
import numpy as np
import re
 

class Course():
    '''Object representaion of a course.'''
    
    def __init__(self, course_name, title, course_credits, genEdSatisfactions, description, GPA):
        '''Course object construction method.
        Args:
            self (Course) - Reference of the course object.
            course_name (str) - Course name in the form of tag (Ex.INST) and number (Ex.326)
            title (str) - official and descriptive title of the course
            course_credits (int) - Number of credits the course offers.
            genEdSatisfactions (list) - List of the GenEds the course satisfies.
            description (str) - Description of the course.
            GPA (float) - Average GPA of the course.
        Returns:
            None.'''
        
        self.course_name = course_name
        self.title = title
        self.course_credits = course_credits
        self.genEdSatisfactions = genEdSatisfactions
        self.description = description
        self.GPA = GPA

    def __repr__(self):
        '''Repr method of the course object. Creates a string representation of a course.
        Args:
            self (Course) - Reference of the course object.
        Returns:
            courseBreakdown (str) - Formatted string showing the details of the course.'''
        
        courseBreakdown = ""
        courseBreakdown += self.course_name + " " + self.title + "\nCredits: " + str(self.course_credits) + "\nGenEds: |"
        for genEd in self.genEdSatisfactions:
            courseBreakdown += genEd + "|"
        courseBreakdown += "\nAverage GPA: " + str(self.GPA) + "\nDesc:\n" + self.description
        return courseBreakdown

    def frame_form(self):
        '''Returns a dictionary representation of the course. necessary for dataframe usage.
        Args:
            self (Course) - Reference of the course object.
        Returns:
            course_dict (dict) - Dictionary representation of the course.'''
        
        gens = "|"
        for genEd in self.genEdSatisfactions:
            gens += genEd + "|"
        course_dict = {"Course": self.course_name, "Title": self.title, "Credits": self.course_credits, "GenEds": gens,
                        "Average GPA": self.GPA}

        return course_dict
    
def search(courseTag, term):
    '''Starts a parse query for free courses.
        Args:
            courseTag (str) - Course tag(INST, ENGL, AREC, etc.) to refine query.
            term (str) - Case-sensitive smester term of which the user wants to register.
        Returns:
            pageText (str/html) - Html text of the page we will extract courses from.'''

    #Creating the selenium driver and opening SoC. Similar structures will be seen further in the code.
    driver = webdriver.Chrome()
    driver.get("https://app.testudo.umd.edu/soc/")
    #Finding the course name/tag search box and entering the given tag.
    courses = driver.find_element("id","course-id-input")
    courses.send_keys(courseTag)
    #Finding the term/semester dropdown menu and selecting the given term.
    termSelect = Select(driver.find_element("id","term-id-input"))
    termSelect.select_by_visible_text(term)
    #Finding the search button and clicking it.
    search = driver.find_element("id","search-button")
    search.click()

    page = driver.current_url
    pageText = ""

    driver.close()

    #If no course tag was specified, a different function is called to get all offered courses (VERY COSTLY)
    try: 
        pageText = requests.get(page).text
        sleep(0.01)
    except:
        print("too fast!")
    if courseTag == "":
        pageText = parseCourseTags(pageText)

    return pageText

def parseCourseTags(startPage):
    '''Function in case of a query without a course tag (INST, ENGL, AREC, etc.). Must go through the SoC search for every
        tag avaiable for the specified semester. Searching like this will take substantially longer than specifying a single tag.
        Args:
            startPage (str/html) - Html text of the page holding links to all the tag sections for a particular semester.
        Returns:
            coursesText (str/html) - Html of ALL the courses offered during the sepcified semester.'''
    
    soup = BeautifulSoup(startPage, "html.parser")
    columns = soup.find(id="course-prefixes-page")
    links = columns.find_all("a")

    i=0
    coursesText = ""
    while i < len(links):
        currentLink = links[i]["href"]
        try: 
            coursesText += (requests.get("https://app.testudo.umd.edu/soc/" + currentLink).text) + "\n"
            sleep(0.01)
        except:
            print("too fast!")
        i=i+1
        
    return coursesText

def getCourses(coursesPage, keywords):
    '''Parses through a course result set to put courses in more usable objects.
        Args:
            coursesPage (str/html) - Html text of the page we want to extract courses from.
        Returns:
            courseList (list) - List of all the new course objects created from the resultset.'''
    
    soup = BeautifulSoup(coursesPage, "html.parser")
    courses = soup.find_all(class_="course")
    courseList =[]

    #Getting data from all courses in the result set
    for course in courses:
        courseName = course.find(class_="course-id").contents[0]
        courseTitle = course.find(class_="course-title").contents[0]
        
        #Series of try/catches to account for differences in description placement per course.
        try:
            courseDesc = course.find_all(class_="approved-course-text")[1].contents[0]
        except:
            try:
                courseDesc = course.find_all(class_="approved-course-text")[0].contents[0]
                if(courseDesc.find("<div>") >= 0):
                    courseDesc = "N/A"
            except:
                courseDesc = "N/A"

        #Checks if the course name or title has a keyword, should keywords be provided. If they do not, course is not added at all
        #to preserve efficiency.
        if len(keywords) > 0: 
            if (checkKeywords(courseTitle, keywords) == False and checkKeywords(courseDesc, keywords) == False):
                continue
        
        courseCredits = course.find(class_="course-min-credits").contents[0]
        courseGenEds =[]

        #For genEds, we make a list and comb through each course to fidn them. In cases of multiple, we use further iteration.
        genEdsList = course.find_all(class_="course-subcategory")
        if len(genEdsList) < 1:
            courseGenEds.append("None")
        else:
            for genEd in genEdsList:
                courseGenEds.append(genEd.text[1:5])

        courseGPA = 0.0   

        newCourse = Course(courseName, courseTitle, courseCredits, courseGenEds, courseDesc, courseGPA)
        courseList.append(newCourse)

    return courseList

def getCourseGPA(courses):
    '''Cross references Planet Terp to find the average GPA for the course.
        Args:
            courses (list) - List of the courses we wish to populate the GPAs of.
        Returns:
            None.'''

    #Similar process to what we did in the search function.    
    driver = webdriver.Chrome()  
    
    for course in courses:
        courseName = course.course_name
        driver.get("https://planetterp.com/")
        searchBox = driver.find_element("id","main-search")
        searchBox.send_keys(courseName)
    
        searchButton = driver.find_element("class name","input-group-append")
        searchButton.click()

        page = driver.current_url
        pageText = ""
        GPA =0.0

        #Try-catch accounts for instances where a course is not on Planet Terp (perhaps because it is new). GPA is set to 0.
        try:
            sleep(0.3)
            GPA = float(driver.find_element("id", "average-gpa-text").text[15:19])
            sleep(0.3)
        except:
            print("empty")
 
        course.GPA = GPA

def checkKeywords(check_text, keywords):
    '''Goes through provided string and returns a boolean specifying whether or
        not any of the kwywords could be found in that string.
        Args:
            check_text (str) - Text we wish to compare/search the keyword for.
            keywords (list) - List keywords the user specified.
        Returns:
            Boolean - Boolean of wheter or not any of the keywords were found.'''

    #In case any previous errors/try catches failed and an incompatible type is
    #passed, this accounts for that and returns False.
    if check_text is None or (not (isinstance(check_text, str))):
        return False
    for keyword in keywords:
        if(check_text.upper().find(keyword.upper()) >= 0):
            return True
    return False

def create_visual(courses):
    '''Creates the dataframe of our courses.
        Args:
            courses (list) - List of the courses we wish to make a dataframe from.
        Returns:
            df (dataframe) - Dataframe made from our courses list.'''
    
    df = pd.DataFrame.from_records([course.frame_form() for course in courses])
    return df


if __name__ == "__main__":
    '''Main method that runs the prompt for the user'''
    run = "d"
    while run.upper() != "DONE":
        
        print("List the course tag (Ex. INST, ENGL, AREC) you wish to search and press enter, or press enter with nothing to search all tags (SLOW)")
        tag = input()
        print("\nEnter the semester you wish to search (case sensitve; Ex. Summer 2023).")
        term = input()
        print("\nEnter any keywords you wish to filter by, press enter after each keyword. Enter \"DONE\" when finished or to not filter.")
        keys = []
        key = input()

        while key.upper() != "DONE":
            keys.append(key)
            key = input()

        page = search(tag, term)
        course_list = getCourses(page, keys)
        getCourseGPA(course_list)
        final_frame = create_visual(course_list)
        print(final_frame.to_string())

        print("Enter any key to run another search, or enter \"DONE\" to end program")
        run = input()
