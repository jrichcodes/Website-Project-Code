# Product Requirements Document
Name: Josephine Rich

Product Name: TripPlanner

## Background
For any trip to go smoothly, there is planning invovled. We created a website to help users organize their outdoor trips and be inspired to go outdoors. Currently, there are regular trip planners and hiking planners. We saw a gap in the market for any type of outdoor activity trip planning all in one. There is also a social media aspect that allows users to become friends each other and share trips. Our easy to use interface is welcoming to any person whether a newbie or a senior to the outdoors. All of your current and past trips are in one place so that people can see where you have gone and where you are headed. 

## Project Overview
Trip Planner is an online outdoor trip planning service that allows users to prepare for trips easily. Users must create a profile to begin planning. From there, users can log in and utilize the Events page to create a trip. After a trip is created, users have the option to delete the trip or modify it through the Trip Summary page. The Trip Summary page can be accessed by clicking on the trip on the Events page. Users can use the Trip Summary page to create trip view general information about the trip, add gear items, create a menu for the trip, or view the trip's location on a map.

One of the most convenient features of trip planner is how efficient it allows the trip planning process to become. For example, if a user wants to create a trip but is not sure where they would like to go, they can use the Trip Suggestions page to view a list of possible trips, which can be filtered by location. Additionally, if the user clicks the "Create Trip" button on one of these suggestions, the Events page will be autofilled with information such as the name, description, and location.

Some other convenient features of trip planner include:
- Scheduling tools
- Mapping tools
- Meal planning
- Grocery shopping list
- Ability to friend other users

## Features
1. **Create an Account** As a new user, I want to register by creating a username and password so that I can store my data.
2. **Suggested Recipes** As a registered user planning a trip, I want possible recipe ideas so that I can add them to my trip menu.
3. **Create Trip** As a registered user, I want to save information about a trip I am planning so I can access the information later.
4. **See Friends** As a registered user, I want to see my friends so I can see what trips they are planning.
5. **Home Page** As user, I want to see what features the website has to offer so I can decide if I will use it or not.
6. **Logout** As a logged in user, I want to logout so that my information is protected and can on longer be seen.
7. **Delete Trip** As a registered user, I want to delete a trip so that I no longer see it under my trips. 
8. **Add gear item** As a registered user, I want to add a gear item to my gear list so I know what to bring on my trip.
9. **Map** As a registered user, I want to see where my trip is on a map so I can see where I am going to.
10. **Recipe Card** As a registered user, I want to see how to make a suggested recipe so I know the steps to make the recipe. 


## Technologies to be used
**Frontend** 
- HTML : creat basic web pages
- Boostrap : used to make website pretty
- CSS : used to make website pretty

**Backend**
- SQLAlchemy : database
- Flask : web framework
- Python : glue that holds everything together
- Javascript : does the backend work for reactive buttons on the frontend
- Json : used for suggestion pages data so that we would not have to store in database
- Flask-Login : used to restrict viewing of certain pages based on login status

**Python Libraries**
- Folium : visualize data
- Geopy : create the trip maps
- Datetime : create the trip countdown
- werkzeug.security : used for generating hashes
