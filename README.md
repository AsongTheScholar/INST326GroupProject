# INST326GroupProject

REQUIREMENTS:
- Program designed to run on Python3.10 or newer, though backwards compatability is potentially possible.
- The program requires the downloading of requests into the user's python library.
- The program requires the downloading of BeautifulSoup into the user's python library.
- The program requires the downloading of Selenium into the user's python library.
- The program requires the downloading of pandas into the user's python library.

USAGE:
To run the program, either run the file direclty or through command bar. User will be met with a sequence of prompts that
allow the program to refine their course search. Follow the prompts according to your scheduling wishes, and after
completion you will be delivered a tabular dataframe of all the courses matching your query, GPA included. The program
runs within an exitable loop, s users can run successive queries from the same program call until they wish to stop.

WARNINGS:
- GPA data is only available from those whom chose to report to PlanetTerp. As such, it is taken with a grain of salt and
  is not a 100% accurate depiction of the diffciulty or true average experience of the course.
  Some courses also do not have any reports of GPA data on PlanetTerp, so those courses will be reported as a 0.0 and
  unfortunately miss this key insight.

- The program makes use of live browser simualtion. As such, program speeds may vary and may be greatly reduced by large
  and broad search queries. If a user chooses to search every possible course tag, without any filtering keywords, previous
  tests have given it a response time of up to 30 minutes. Perform large searches at your own expense.
