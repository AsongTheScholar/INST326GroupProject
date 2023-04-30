import requests
from time import sleep
import pandas as pd
from selenium import webdriver

class Course():
    def __init__(self, course_name, title, course_credits, genEdSatisfactions):
        self.course_name = course_name
        self.title = title
        self.course_credits = course_credits
        self.genEdSatisfactions = genEdSatisfactions

def search(courseTag):
    '''Starts a parse query for free courses.
        Args:
            frame (str) - Dataframe to write to.
            tags (list) - Tags to apply to refine the search.
        Returns:
            TBD; likely the dataframe or none.'''

    driver = webdriver.Chrome()
    driver.get("https://app.testudo.umd.edu/soc/")
    courses = driver.find_element("id","course-id-input")
    courses.send_keys(courseTag)
    search = driver.find_element("id","search-button")
    search.click()

    page = driver.current_url

    try: 
        pageText = requests.get(page).text
        sleep(2)
    except:
        print("too fast!")

    return pageText
    
def formatTable(frame, maxRows, sort):
    '''Takes a data frame and returns it in a more deliverable form.
        Args:
            frame (str) - Dataframe to write to.
            maxRows (int) - mx number of rows to display.
            sort (str) - Variable/factor to sort table by.
        Returns:
            courseTable (dataframe/2dlist) - Tabular representation of the formatted dataframe.'''

def main():
    '''Not fully thought through yet. Will likely have a series of inputs.'''