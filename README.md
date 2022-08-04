# TASK 0: The ability to demo use the application without registration but with cookies data collection 

## Project Description
### This exercise inherits from the base of our [rewarding system](https://github.com/OfficialRuby/longevity-interview/tree/main/reward) which was part of [longevity-interview](https://github.com/OfficialRuby/longevity-interview).

Ulike the [previous version](https://github.com/OfficialRuby/longevity-interview/tree/main/reward) of this app, the current version allows user to interact with the system and then meanwhile keeping record of user interactions by means of cookies. For instance, if a user is not logged in when performing a task that rewards him/her, their progress will not be lost when they authenticate with the server.

## Dependencies
This project has been tested to work on the following environments
1. Python3.9 running on Debian 11 Linux (Bullseye)
2. Docker environment configured with python3.9 image

## Known Issue

1. This project only aims at showing how an unauthenticated user can interact with the system, it doesn't make any external API call in the process of rewarding user.
2. The project does not perform strict check on user rewarding, which means a user can be rewarded more than once for performing a particular task.

## Running the project 
With docker file alredy configured, this program can be lunched by running `docker-compose up --build` form the base directory of the downloaded or clonned repository.

### Cheers