# School of Computing &mdash; Year 4 Project Proposal Form


## SECTION A

|                     |                   |
|---------------------|-------------------|
|Project Title:       | No-Limit Texas Hold'em Poker AI            |
|Student 1 Name:      | Stefano Puzzuoli            |
|Student 1 ID:        | 17744421            |
|Student 2 Name:      | Immanuel Idelegbagbon            |
|Student 2 ID:        | 17393433            |
|Project Supervisor:  | Dr Mark Roantree            |

## SECTION B

### Introduction

This project consists of an easy to use web application that allows users to test their Texas Hold'em Poker skills against one or more Artificial Intelligence Agents in a game of No-Limit Texas Hold'em Poker.  

No-Limit Texas Hold'em Poker contains an enormous strategy space, imperfect information and stochastic events, all elements that characterize most of the highest level challenging problems in multi-agent artificial intelligence systems.  

Our project will tackle such challenges with Reinforcement Machine Learning, with a Gradient Boosting Regressor which will result in an additive model in a forward stage-wise fashion, allowing for the optimization of arbitrary differentiable loss functions.  

### Outline

The Texas Hold'em Poker application will be based on Artificial Intelligence Agents which learn from their opponents’ behaviours and implement strategies to counteract their actions in order to maximise their own winnings.  

Throughout a game, after each iteration, each Agent is trained using a set number of selected features and labels while the remaining features and labels from the beginning of the Agent's “career” are discarded. The motivation for this discarding is that the expected return of an Agent’s action is a function of the Agent's future actions in any hand, so older hands become inaccurate as an Agent improves.  

A machine learning Gradient Boosting Regressor is used to estimate a function from the set of saved features to the set of saved labels. In order to predict the best action, the Agent executes this function according to the state of the game and the entire set of possible actions. The one that is estimated to be the maximum expected return value is picked. The Artificial Intelligence Agents are this way trained repeatedly with the final objective of generating interesting and viable poker winning strategies.  

Since with No Limit Texas Hold’em Poker there are 10<sup>71</sup> possible game states, we will also be implementing a poker hand evaluation library, which will have to be lightweight and fast. This evaluation library will handle 5, 6 and 7 card hand lookups. All lookups will be done with bit arithmetic and dictionary accesses.  

Python 3 will be the programming language used to deal with all the calculations involving the machine learning algorithm and data manipulation.  

Regarding the front-end of the project, it will consist of a user-friendly web application which users will be able to access through their web browsers. This UI will allow the users of the application to visualise the poker game, with the table, opponents, cards and all the possible accepted commands when playing each hand.  

TypeScript will be the programming language used to develop the front-end of the web application and more specifically Angular, a TypeScript framework.  

The web application will also include a sign up/login functionality which will allow users to keep track of their game statistics (e.g. winning percentage). Users which do not want avail of this functionality will have the option to play games as guests, which will not involve any statistics recording.  

MariaDB will be the RDBMS used to store the data.  



### Background

After successfully creating a Fantasy Football Point Predictor in our Third Year Project, we were curious to find out how Machine Learning and Artificial Intelligence could be applied to a completely different game which requires strategy, intuition, and mainly reasoning based on hidden information.  

After some profound research and discovering that AI had repeatedly had success at beating humans in past years in games like Chess and Go (games that follow predefined rules and are not affected by random factors), we became aware that much more rare were the Artificial Intelligence Agents/Bots that had obtained the same success in games like No-Limit Texas Hold'em Poker. From this we decided to take on this challenge and try to create AI Agents that can give human poker players a real challenge.  


### Achievements

The main function of this web application is to provide Machine Learning AI Agents that will be able to play No-Limit Texas Hold'em Poker against each other and a user, learning from their opponents’ behaviours and implementing strategies to counteract their actions in order to maximise their own winnings.  

The users of the web application will be individuals who want to test or improve their No-Limit Texas Hold'em Poker skills against competent opponents, have fun or even simply learn how to play said game.  

### Justification

The main purpose of this web application is to provide users with Artificial Intelligence Agents against which they can play No-Limit Texas Hold'em Poker and not only test their skills, but also improve them.  

Users will be able to adopt different game strategies against skilled players (the AI Agents) and verify which ones are most effective and successful.  

This web application will be very useful for players who want to challenge their No-Limit Texas Hold'em Poker skills.  


### Programming language(s)

* **Python 3**

Python 3 will be the programming language used to deal with all the calculations involving the machine learning algorithm and data manipulation. More specifically we intend to make use of a Gradient Boosting Regressor which will result in an additive model in a forward stage-wise fashion, with the objective to create “smart” and “skilled” AI Agents to challenge users.  
This will also be the language in which we will write our poker hand evaluation library.  

* **TypeScript**

We intend to use Typescript (through the framework Angular) a the programming language to build a web facing user interface which will allow the user to play No-Limit Texas Hold'em Poker against the AI Agents with visuals of the table, opponents, cards and all the possible accepted commands when playing each hand. The front-end of the application is responsible for giving users a direct visual of all they will need to play the game.

* **SQL**

SQL (Structured Query Language) will be the language utilised to manage the user data in the database.


### Programming tools / Tech stack

* **Angular**

As previously mentioned, Angular will be the framework used for the front-end of the web application.

* **Node.js**

Node.js will be used to develop the back-end of the web interface.

* **MariaDB**

MariaDB will be the RDBMS utilized for storing user login credentials and statistics.

* **ExpressJS** 

ExpressJS will be the web server used to allow users to access the web application.

* **Jenkins**

Jenkins will be the automation server which will allow continuous integration and facilitate technical aspects of continuous delivery whenever necessary.


### Hardware

No non-standard hardware components which will be required for this project.

### Learning Challenges

* **Machine learning in games with imperfect information and non-determinism**

Undoubtedly, one of the most challenging aspects of this project will be tackling the machine learning features of the AI Agents against which users will be playing. As a No-Limit Texas Hold'em Poker game can be in one out of 10<sup>71</sup> possible game states, creating a model which allows our AI Agents to both perform within certain time restrictions and in a competent manner, while adapting their style of play to the opponents’ will not be a simple task. It will be our first time tackling machine learning in games with imperfect information and non-determinism. It will be our first time tackling Reinforcement Machine Learning.

* **TypeScript/Angular**

It will also be our first time to make use of the programming language TypeScript and the framework Angular so learning this new language and tool necessary for the front-end will require some time.

* **Node.js**

An additional challenge regarding the web interface will be making use of Node.js for its backend and combining it with Angular which is also something we will be tackling for the first time.

* **User Credentials Authentication and Authorization**

As our web application will allow users to sign up/login to record their game statistics, we will be required to securely store sensitive information in a database, to then authenticate and authorize users to play under a certain registered player username. This will be the first time that either of us store and retrieve sensitive data in a database.


### Breakdown of work

#### Student 1 - Stefano Puzzuoli

* User Interface – Interactivity/background tasks
* Machine learning (Gradient Boosting Regression algorithm) – initial predictions, pseudo-residuals computation, training and testing
* Database management
* Continuous integration and Continuous delivery


#### Student 2 - Immanuel Idelegbagbon

* Initial Dataset retrieval
* User Interface –  Frontend
* Machine learning (Gradient Boosting Regression algorithm) – subsequent predictions, new pseudo-residuals computation and final predictions
* Accessibility features
* Testing

