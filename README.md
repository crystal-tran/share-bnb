<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">

<h1 align="center"> 🏡🏖🗺ShareBnB 🌄🛫🚣‍♂️ </h1>

  <p align="center">
    Explore your next backyard destination.
    <br />
    <br />
    <a href="https://sharebnb.crystaltran.dev/">View Demo</a>
    <br />
    <br />
     <p>username: <b>guest</b> | demo password: <b>password</b></p>
    <img src="https://github.com/crystal-tran/share-bnb/blob/main/static/images/sharebnb-demo-gif.gif" alt="sharebnb-demo">

   
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#learnings">Learnings</a></li>
        <li><a href="#database-design">Database Design</a></li>
      </ul>
    </li>
    <li>
      <a href="#built-with">Built With</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#authors">Authors</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

  <h1 align="left">About the Project</h1>
<!--   <p align="left">
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
  </p> -->
ShareBnB is a full-stack application that enables users to login, manage their profile, browse and search for property rentals, book/reserve listings, post listings, and upload images securely in AWS. This project was built in January 2024 during a 4-day sprint at <a href="https://github.com/rithmschool">Rithm School</a>. 
<br />
<br/ >
This project offered the opportunity to build an entire full-stack application from scratch with the technologies of our choosing. We chose to build the backend with Flask for server-side routing and its integration with Jinja for accelerated development and library support with SQLAlchemy. 
<br />
<br />
Frontend and backend hosted on <a href="https://render.com/">Render</a> and database hosted on <a href="https://www.elephantsql.com/">ElephantSQL</a>.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Learnings
- Project management and prioritizing key features under a deadline
- Delivering technical concepts with a lightning talk presentation
- Incorporating AWS S3 for secure cloud storage
- Documentation of bugs and resolution process
- Designing RESTful API routing
- Implementation of SQLAlchemy ORMs to manage database schemas and relationships
- Form validation and error handling with WTForms
<br />
<br />

## Database Design
<img src="https://github.com/crystal-tran/share-bnb/blob/main/static/images/sharebnb-database-schema.PNG" alt="sharebnb-db-schema">


## Built With

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
* ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)
* ![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)
* ![SQLAlchemy Badge](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=fff&style=for-the-badge)
* ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
* ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
* ![ElephantSQL](https://img.shields.io/badge/-ElephantSQL-336791?logo=elephantsql&logoColor=white&style=flat)
* ![Render](https://img.shields.io/badge/-Render-333333?logo=render&logoColor=white&style=flat)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED  -->

## Getting Started

To get a local copy up and running follow these steps.

1. Clone repository.
   ```sh
   git clone https://github.com/crystal-tran/share-bnb.git

   ```
2. Create a virtual environment and install dependencies.
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Create and seed database.
   ```sh
   createdb sharebnb
   python seed.py
   ```
4. Run app
   ```sh
   flask run
   ```
5. View on <a href="http://localhost:5000/">http://localhost:5000/</a>.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Authors
* [Brandie Lucano](https://github.com/BMLucano) : Frontend and backend co-author

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Rithm School](https://github.com/rithmschool)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Markdown-Badges](https://github.com/Ileriayo/markdown-badges)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

