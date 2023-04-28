# AbiVenkat_WanyueWang

## Title: 

FacultyFinder+

## Purpose: 
This application's purpose is to help connect students to faculty members that best align with their goals and research pursuits.

## Demo: 

Give the link to your video demo. 

## Installation: 

The application is based on python so python will be necessary and so will accompanying packages such as dash. Additionally mysql, neo4j, and mongodb local instances need to be running and the proper local credentials needs to be passed into the relevant utility files to run the application. To run the application use `python app.py` and click the generated local host link presented in the terminal to access the application in your web browser.

## Usage: 

Simply fill out the forms in the widgets to use the application. There are many different things you can do and instructions are located in each widget. 

## Design: 

The overall application is written in python utilizing dash. The application uses a specific flavor of dash called bootstrap for the styling and also uses the respective mysql, mongodb, and neo4j python libraries to communicated with the local databases that are running, so the app can read and write data to the databases. 



### Widget 1:

This widget is designed to accept a user-inputted keyword of interest. Based on the input, the widget will display a list of the top 5 universities that have the highest number of faculty members working on that particular keyword, along with the number of relevant faculty members. Additionally, the widget will also display the top 5 faculty members from each university who have the highest score for the given keyword along with the score. 

(We consider a faculty member working on a keyword if it is one of his/her keywords.)



### Widget 2:

For researchers seeking a faculty mentor or collaborator, it's essential to determine if the potential faculty member is open to collaboration. This widget can help identify their collaboration preferences by analyzing the number of co-authored papers they have with other faculty members. Users can apply a time filter to focus on recent collaborations, such as within the past five years.

To prevent confusion due to identical names, users should input both the faculty member's name and their affiliated institution.

### Widget 3:

It's important to know for a student what areas of research a faculty member is most relevant with. Often something like a keyword relevant citation score could be proven to be a useful metric to see how many citations a faculty member is cited for regarding a particular relevant keyword.

The user can input a faculty name to retirieve a faculty member's keyword relevant citation score for the specific keywords the faculty is relevant with. This result is then displays as a graph in descending order to give the user a more holistic look about the faculty member's works.


### Widget 4:

Keeping track of all the faculty members a user may be interested in can be cumbersome if there is no way on the application to keep track. Therefore to help users keep track of what faculty members they are interested in, we created a form where a user can input the faculty's name along with an optional note to save it to a favorites table. This table is there present at all times so a user can keep track. This table contains additional information about the faculty member as well pulled from the information we have about them and also can contain a note the user makes about the faculty member. 

### Widget 5:

This widget allows a user to delete a faculty member from their favorites table if they no longer are interested in considering that faculty member.

### Widget 6:

Once the ideal faculty candidate is identified, how can you establish contact? By entering either the known faculty member's name and their affiliated institution, or simply a school name with strong connections, this widget will determine the links to the candidate faculty member.

We employ Neo4j's shortest path finding to reveal how the candidate and known faculty members are connected through a series of alternating "INTERESTED_IN" relationships, connected by "KEYWORD" and "FACULTY" nodes. Up to five paths will be displayed for the user's convenience.



## Implementation: 

We implemented our project by using python and more specifically configuring the frontend and backend code using dash. Utilizing pymongo, pymysql, and neo4j libraries we were able to connect inputs from the frontend and integrate those into queries that we submitted on the backend to our databases. The results we got from the databases were mostly fed into pandas dataframes and then those dataframes were manipulated into different dash components to preset grahps, networks, and tables. 

For the frotend styling we mostly used dash bootstrap for theming our components and also for pre-configured CSS styles on certain layout configurations mostly made up table-esque structure consisting of rows and columns.

## Database Techniques: 

  - To speed up the processing on the favorites table, we created a compound index structure on the faculty name and note column for the favorites table. We     liked this approach as we could have a single index structure that hold references to multiple fields
    `db.favorites.createIndex({"faculty_name":1, "note": 1})`
  - Later we realized that we want to create a constraint on this favorites table in that since there could be multiple faculty members that have the same       name, we wanted to make sure at least the combination of a faculty member's name and note would be distinct and this combination is what we could use to     differentiate different faculty members that have the same name. We added a unique attribute constraint to our index and this is applied to the whole         table, so no new data can be added unless the combination of faculty member name and note is unique.
    `db.favorites.createIndex({"faculty_name":1, "note": 1}, {unique : true})`
  - To have a fast lookup of the KRC scores for a professor for all their related keywords we created a view in mysql. This way in our actual query code coming from python we could quickly access the KRC scores for the professor we want.
  ``` 
    CREATE VIEW faculty_krc AS 
    SELECT faculty.name as faculty_name, keyword.name as keyword_name, SUM(publication_keyword.score * publication.num_citations) as KRC
    FROM faculty, keyword, publication, publication_keyword, faculty_publication
    WHERE faculty.id = faculty_publication.faculty_id AND publication.id = faculty_publication.publication_id
    AND publication.id = publication_keyword.publication_id AND keyword.id = publication_keyword.keyword_id
    GROUP BY faculty_name, keyword_name
    ORDER BY KRC DESC;
  ```
## Extra-Credit Capabilities: 

N/A

## Contributions: 

Both team members spent equal amounts of time and effort working on the application and the documentation. Widgets 1,2,6 were implmented by Wanyue and widgets 3,4,5 were implemented by Abi. Afterwards both spent time on styling and other areas related to the project such as documentation and the video demo equally.
