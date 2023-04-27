# Metronome

<!--- ![Logo](https://github.com/ttrevorreese/Metronome/blob/8bc31be3fe74fc77f94a45a025143cd0a7c7e2c1/Assets/Metronome%20Logo.png) --->

<img src="https://github.com/ttrevorreese/Metronome/blob/8bc31be3fe74fc77f94a45a025143cd0a7c7e2c1/Assets/Metronome%20Logo.png" alt="Metronome Logo" width="500" height="500">

This is the repository for the Boolean Hooligans group for the Data Engineering Module at the University of Roehampton in Year 3 of the Computer Science BSc program.

## Company

The mock company we have created to work with this data is called Metronome, where we provide music recommendations based on a user's Spotify listening history.

## Project Scope

This project is aimed at creating a data engineering system (data pipeline) for a business' smooth and efficient data delivery.

We will work on the project as a Scrum team, adopting design and project management methods, such as Agile and Kanban. Familiarity and knowledge of a typical software development team, such as Visual Studio, Git, and Docker, is essential. We will also need to familiarize ourselves with some of the difficult human and technical issues around collaborating on and continuous improvement of a data delivery system.

### Requirements

- Identifying the requirements (functional and non-functional)
- Prioritizing the requirements (if applicable)
- Task allocation
- Identifying the scope of your project
- Identifying the stakeholders
- Risk management

## Key Features

- Extracts user's Spotify listening history (most recent 50 songs played)
- Generates 50 recommendations based on the listening history
- Creates a playlist on the user's account with the recommendations

## Build Structure

- Apache Airflow within a Docker container
- Python scripts being ran in the background using the Airflow DAG file
- Spotify API implementation

## Installation and Use

1. Clone this repository into Visual Studio Code using this link: https://github.com/ttrevorreese/Metronome/
2. Retrieve your Spotify API token from this link: https://developer.spotify.com/
3. In the `extract.py` file and the `playlist_generator.py` file, replace the `user_id` variable with your Spotify username and the `TOKEN` variable with your API token taken from the line above. Make sure to save both files.
4. Download Docker Desktop and in the `docker-compose.yml` file, create a new terminal and run the commands `airflow db init` followed by `docker compose up` to create the docker container. Go to http://localhost:8080 to access Airflow, with the username and password being airflow.
5. Once the Docker container is ran, run the `spotify_dag.py` file to initialize the DAG within Airflow.
6. In your Spotify account, you should see a new playlist generated. The DAG file will update the playlist with new songs periodically as you listen when the DAG is active.
7. Alternatively, you can run the `extract.py` and `playlist_generator.py` files to create one playlist.

## Bug Reporting

If there are any bugs or issues with the program or installation, please use the issues tab located within this GitHub repository. This will make it easy for user communication with us developers, as we will be able to locate the bug(s) and try to create a solution as fast as possible.

## Programming Languages and Tools

<img align="left" alt="Python" width="26px" src=https://github.com/devicons/devicon/blob/2ae2a900d2f041da66e950e4d48052658d850630/icons/python/python-original.svg style="padding-right:10px;"/>
<img align="left" alt="NumPy" width="26px" src=https://github.com/devicons/devicon/blob/2ae2a900d2f041da66e950e4d48052658d850630/icons/numpy/numpy-original.svg style="padding-right:10px;"/>
<img align="left" alt="Pandas" width="26px" src=https://github.com/devicons/devicon/blob/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg style="padding-right:10px;"/>
<img align="left" alt="Docker" width="26px" src=https://github.com/devicons/devicon/blob/2ae2a900d2f041da66e950e4d48052658d850630/icons/docker/docker-original.svg style="padding-right:10px;"/>
<img align="left" alt="PostgreSQL" width="26px" src=https://github.com/devicons/devicon/blob/2ae2a900d2f041da66e950e4d48052658d850630/icons/postgresql/postgresql-original.svg style="padding-right:10px;"/>
<img align="left" alt="Git" width="26px" src=https://github.com/devicons/devicon/blob/2ae2a900d2f041da66e950e4d48052658d850630/icons/git/git-original.svg style="padding-right:10px;"/>
<img align="left" alt="Visual Studio Code" width="26px" src="https://github.com/devicons/devicon/blob/2ae2a900d2f041da66e950e4d48052658d850630/icons/vscode/vscode-original.svg" style="padding-right:10px;"/>
<img align="left" alt="GitHub" width="26px" src=https://github.com/devicons/devicon/blob/2ae2a900d2f041da66e950e4d48052658d850630/icons/github/github-original.svg style="padding-right:10px;"/>
<img align="left" alt="Spotify" width="26px" src=https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg style="padding-right:10px;"/>

<br />

## Contributors

- [Trevor Reese](https://github.com/ttrevorreese)
- [Matthew Lowrie](https://github.com/MatthewLowrie)
- [Mandev Seahra](https://github.com/mseahra)
- [Sayeed Bin Yahya](https://github.com/Sparx4life7xxx)

## Credits

This project was done in honor and loving memory of Mandev's father. ♥
