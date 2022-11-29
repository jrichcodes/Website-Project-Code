# Product Requirements Document
Name: Julia Steed

Product Name: Trip Planner

## Background
The University of Tennessee at Knoxville has an outdoor center from which students and faculty can rent equipment such as mountain bikes, bouldering crash pads, sleeping bags, and many more essentials for trips. Additionally, University of Tennessee Outdoor Pursuits (UTOP) leads a variety of trips each semester. Some examples are whitewater kayaking, mountain biking, and backpacking. Currently, the system UTOP uses to manage these trips is fairly limited in terms of functionality, and requires a large amount of manual processes. If UTOP had more capable and dynamic software, their trip preparation process would go more smoothly and likely allow them to run more trips.

## Project Overview
Trip Planner is an online outdoor trip planning service that allows users to prepare for trips easily. Users must create a profile to begin planning. From there, users can log in and utilize the Events page to create a trip. After a trip is created, users have the option to delete the trip or modify it through the Trip Summary page. The Trip Summary page can be accessed by clicking on the trip on the Events page. Users can use the Trip Summary page to create trip view general information about the trip, add gear items, create a menu for the trip, or view the trip's location on a map.

One of the most convenient features of trip planner is how efficient it allows the trip planning process to become. For example, if a user wants to create a trip but is not sure where they would like to go, they can use the Trip Suggestions page to view a list of possible trips, which can be filtered by location. Additionally, if the user clicks the "Create Trip" button on one of these suggestions, the Events page will be autofilled with information such as the name, description, and location.

Some other convenient features of trip planner include:
- Scheduling tools
- Mapping tools
- Meal planning
- Grocery shopping aid
- Ability to friend other users

## Features
1. **Custom trip type** As a user planning a trip, I want to be able to create a custom trip type, so that I am not restricted to the list of options in the dropdown for trip type.
2. **Change email** As a user, I want to be able to edit the email address that is associated with my account, so that I can still access my trips if I want to use a different email address for any reason.
3. **Suggested trips** As a user planning a trip, I want to be able to view trip suggestions, so that if I am unsure what trip I want to go on I can easily access some ideas.
4. **Auto-fill trip data from trip suggestions** As a user planning a trip on the suggestion page, when I choose to create a trip from a provided suggestion, I want the data on the trip page that can be autofilled to do so, so that I can save time only having to enter in what is necessary.
5. **Maps** As a user who has planned a trip, I want to be able to view my trip on a map, so that I can see the location I will be going to.
6. **Trip countdown** As a user who has planned a trip, I want to be able to view how many days are left until my trip, so that I know when I am taking the trip and how soon it is.
7. **Filter suggestions page** As a user planning a trip using the suggestions page, I want to be able to filter by location, so that it will be easier to find a trip that's right for me. 
8. **Menus** As a user planning a trip, I want to be able to add a menu to my trip, so that I can plan my nutrition.

## Technologies to be used
- Flask
- Flask-Login
- Flask-SQLAlchemy
- werkzeug.security
- Python
- SQLAlchemy
- Folium
- Geopy
- Django
- Bootstrap
- CSS
- Javascript