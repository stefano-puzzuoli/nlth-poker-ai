## NLTHP 

This NLTHP project consists of an easy to use web application that allows users to test their Texas Hold'em Poker skills against 5 Artificial Intelligence Agents in a game of No-Limit Texas Hold'em Poker. Users are able to select from 4 different levels of difficulty and train and assess their skills according to their desired challenge magnitude. 
The user interface consists of a user-friendly web UI which users can access through their web browsers. This UI allows the users of the application to visualise the Poker game, with the table, opponents, cards and all the possible accepted commands when playing each hand. The application also includes a sign up/log in functionality which allows users to keep track of their game statistics (e.g. winning percentage). Users which do not want to avail of this functionality have the option to play games as guests, which will not involve any statistics recording. The web application makes use of a personally implemented poker hand evaluation library, which is lightweight and fast. This evaluation library handles 5, 6 and 7 card hand lookups and all lookups are done with bit arithmetic and dictionary accesses. 
The models (different models for different difficulties) consist of Reinforcement Machine learning models with Gradient Boosting Regressors that allow each Artificial Intelligence Agent to try to predict the maximum expected return value on each different game state throughout a game. These AI Agents are trained repeatedly with the final objective of generating interesting and viable poker winning strategies, allowing users to test and improve their Texas Hold'em Poker skills.

### Recommended Browsers

NLTHP is compatible with the numerous diverse Operating Systems, devices, and Internet browsers that are available. While we want every user to have the best possible experience, we recognize that it is impossible to develop applications that work identically, efficiently, and effectively with all browsers and versions. We also recognize that testing on every browser version and device combination is no longer possible as many new browser versions are deployed on aggressive weekly or bi-weekly schedules. NLTHP has been tested on and supports the following Web Browsers: 
* Chrome
* Microsoft Edge 
* Firefox 
* Safari
* Internet Explorer 
* Opera


##### Note
------------------------------------------------
Before using the NLTHP App it is recommended to read the User Manual located in the 'docs/documentation' directory. 