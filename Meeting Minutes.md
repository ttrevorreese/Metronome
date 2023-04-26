# Meeting Minutes

The meeting minutes for all of our meetings, formal or informal, will be noted below.

## Sprint 01

*26 January 2023 - 16 February 2023*

### Meeting 01 - 26 January 2023

Initial meeting held after finalizing groups. Started brainstorming ideas for the project. Our initial idea was to create a service that analyzes Tweets on Twitter, such as meteorology or football statistics/scorelines. Our mock company would be called Filexchange.

### Meeting 02 - 27 January 2023

Another short brainstorming session regarding the artefacts we will have to use for the project. We sat down together to try and better understand what exactly data engineering is and how we are going to create something that fits within the guidelines.

### Meeting 03 - 01 February 2023

Short meeting reviewing and refreshing our memories on Docker and how it works. We ran through some examples, such as Nifi and Airflow to understand how we can use some pre-existing services in order to deliver our goal.

### Meeting 04 - 03 February 2023

We initialized our repository and began creating the basic parts of it, such as this Meeting Minutes file, our Code of Conduct, our README file, our licenses, etc.

### Meeting 05 - 05 February 2023

After individual and collective brainstorming, we decided to move away from our original idea of using Tweets because it could be too abstract, and we wanted something that could be easily presentable, as well as very straightforward to the user. Therefore, we decided to create a Spotify data pipeline that will analyze a user's listening history and present them with artist and genre recommendations based on their listening data. We changed our mock company's name to Metronome.

### Meeting 06 - 10 February 2023

We began finalizing the requirements for the Sprint 01 submission, including creating a Product Backlog, a Kanban and Sprint board, defining user stories, and creating relevant branches on GitHub. We also began working on our presentation for Sprint 01.

### Meeting 07 - 16 February 2023

We completed all of our tasks for the Sprint 01 submission and demonstrated our work thus far to our supervisor and lecturer, Dr. Kevin Chalmers. He approved of our work and gave us pointers on how to move forward. After this, we began discussing our next steps forward and what we want to accomplish by the next sprint.

## Sprint 02

*17 February 2023 - 9 March 2023*

### Meeting 08 - 19 February 2023

We began researching specifically how we can implement the Spotify listening data into a data pipeline structure. We did some research on the Spotify API and how we can use that to transfer the data automatically. We also began researching which data pipelines would work best for our use case, and we landed on Apache Airflow.

### Meeting 09 - 22 February 2023

After deciding on Airflow, we began testing the implementation of the Spotify API and how we can read and use that data. We found that it is really easy to actually get the data from Spotify, but an issue that we ran into was that the API tokens expire after roughly 30 minutes upon generation. To solve this, we researched DAG files within Airflow in order to automate this process without the need to continually generate API tokens, as this not only causes us difficulty and inconvenience during the development stage, but it would render the entire application virtually useless to the general end user.

### Meeting 10 - 27 February 2023

We continued development on the data pipeline in Python using Airflow. We tested different methods, such as having everything in one file, and also having the processes in separate files. The process of extracting, transforming, and loading the data is not very difficult, it is just a matter of doing it properly and having a strong foundation so that we have usable data for our end goal of giving users recommendations of artists and genres.

### Meeting 11 - 02 March 2023

We got together and reviewed our work and progress thus far. We are working on deciding which methodology will work best for us, but continuing testing in order to create a functional prototype.

### Meeting 12 - 05 March 2023

We continued the development of the data pipeline process and ended up connecting the data from the Spotify API to Airflow using SQLite and DAG files within Airflow. We are now working on this connection and ensuring we have a streamlined process for this connection in further testing.

## Sprint 03

*10 March 2023 - 30 March 2023*

### Meeting 13 - 12 March 2023

We begun implementing an integral part of the Spotify API for song recommendations in the future, the artist ID variable.

### Meeting 14 - 19 March 2023

To further develop our features, we began full development on the playlist creation tool.

### Meeting 15 - 26 March 2023

We continued development on the playlist creation tool with song recommendations.

### Meeting 16 - 30 March 2023

We gathered to present our work for our Sprint 3 submission.

## Sprint 04

*31 March 2023 - 27 April 2023*

### Meeting 17 - 19 April 2023

We revised our work thus far after Spring Break and laid out our goals for our final deliverables.

### Meeting 18 - 20 April 2023

We begun revising our pipeline structure, as it was not efficient enough for our final deliverable. We looked at the structure of what we had and worked on ways to more efficiently provide the service we need. We connected the recommendation tool to Airflow and began troubleshooting the dag process in order to finalize the playlist creation tool.

### Meeting 19 - 21 April 2023

We continued revising the final product for the submission deadline.

### Meeting 20 - 22 April 2023

We continued revising the final product for the submission deadline.

### Meeting 21 - 23 April 2023

We continued revising the final product for the submission deadline.

### Meeting 22 - 24 April 2023

We continued revising the final product for the submission deadline.

### Meeting 23 - 25 April 2023

We continued revising the final product for the submission deadline.

### Meeting 24 - 26 April 2023

We continued revising the final product for the submission deadline.
