# AbiVenkat_WanyueWang

## Title: 

Name of your application.

## Purpose: 
What is the application scenario? Who are the target users? What are the objectives?

## Demo: 

Give the link to your video demo. 

## Installation: 

How to install the application? You don’t need to include instructions on how to install and initially populate the databases if you only use the given dataset.

## Usage: 

How to use it? 

## Design: 

What is the design of the application? Overall architecture and components.



### Widget 1:

This widget is designed to accept a user-inputted keyword of interest. Based on the input, the widget will display a list of the top 5 universities that have the highest number of faculty members working on that particular keyword, along with the number of relevant faculty members. Additionally, the widget will also display the top 5 faculty members from each university who have the highest score for the given keyword along with the score. 

(We consider a faculty member working on a keyword if it is one of his/her keywords.)



### Widget 2:

For researchers seeking a faculty mentor or collaborator, it's essential to determine if the potential faculty member is open to collaboration. This widget can help identify their collaboration preferences by analyzing the number of co-authored papers they have with other faculty members. Users can apply a time filter to focus on recent collaborations, such as within the past five years.

To prevent confusion due to identical names, users should input both the faculty member's name and their affiliated institution.



### Widget 6:

Once the ideal faculty candidate is identified, how can you establish contact? By entering either the known faculty member's name and their affiliated institution, or simply a school name with strong connections, this widget will determine the links to the candidate faculty member.

We employ Neo4j's shortest path finding to reveal how the candidate and known faculty members are connected through a series of alternating "INTERESTED_IN" relationships, connected by "KEYWORD" and "FACULTY" nodes. Up to five paths will be displayed for the user's convenience.



## Implementation: 

How did you implement it? What frameworks and libraries or any tools have you used to realize the dashboard and functionalities?

## Database Techniques: 

What database techniques have you implemented? How?

## Extra-Credit Capabilities: 

What extra-credit capabilities have you developed if any?

## Contributions: 

How each member has contributed, in terms of 1) tasks done and 2) time spent?
