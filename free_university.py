from selenium import webdriver
import pandas as pd

catalogs = {"Harvard":"https://pll.harvard.edu/catalog/free?page=0", "MIT":"https://ocw.mit.edu/search/", "UMD":"https://umd.catalog.instructure.com/?filters%5B%5D=free", "Open":"https://www.open.edu/openlearn/free-courses/full-catalogue"}

def searchUni(frame, university, tags):
    '''Starts a parse query for free courses.
        Args:
            frame (str) - Dataframe to write to.
            university (str) - Catalog to parse through.
            tags (list) - Tags to apply to refine the search.
        Returns:
            TBD; likely the dataframe or none.'''

#The follwoign are functions to search particular catalogs, in case the html formatting is too distinct to handle all in one function
def parseHarvard(frame, tags):
    '''Starts a parse query for free courses.
        Args:
            frame (str) - Dataframe to write to.
            tags (list) - Tags to apply to refine the search.
        Returns:
            TBD; likely the dataframe or none.'''

def parseMIT(frame, tags):
    '''Starts a parse query for free courses.
        Args:
            frame (str) - Dataframe to write to.
            tags (list) - Tags to apply to refine the search.
        Returns:
            TBD; likely the dataframe or none.'''

def parseUMD(frame, tags):
    '''Starts a parse query for free courses.
        Args:
            frame (str) - Dataframe to write to.
            tags (list) - Tags to apply to refine the search.
        Returns:
            TBD; likely the dataframe or none.'''

def parseOpen(frame, tags):
    '''Starts a parse query for free courses.
        Args:
            frame (str) - Dataframe to write to.
            tags (list) - Tags to apply to refine the search.
        Returns:
            TBD; likely the dataframe or none.'''

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