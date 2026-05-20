# Databases-Python-Demo

Adapted from the original [Databases-Python-Demo](https://github.com/DimK19/Databases-Python-Demo).

This repository contains a **Python / Flask** web application demo for the Databases laboratory course, extended with:

- Dockerized execution
- MariaDB 11.8
- additional player review data
- stored vector embeddings
- similarity search functionality on reviews

---

## Dependencies

To run the project, you need:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

The application uses the following Python libraries:

- Flask
- Flask-MySQLdb
- Flask-WTF
- faker
- email-validator
- mysqlclient
- numpy
- sentence-transformers

All required Python packages are listed in `requirements.txt`.

---

## What does Flask do?

Flask is a Python web framework used to create web applications.

In this project, Flask is responsible for:

- defining routes / endpoints
- receiving HTTP requests
- executing Python logic
- communicating with the MariaDB database
- rendering HTML templates with dynamic data

This project uses **raw SQL queries** through Python and Flask.

---

## Project Structure

Main files and folders:

- `dbdemo/`  
  Main Flask package.

- `dbdemo/__init__.py`  
  Initializes the Flask application, database connection, and Blueprints.

- `dbdemo/routes.py`  
  Contains the main routes, including review and similarity search routes.

- `dbdemo/student/`  
  Student-related Blueprint, forms, and routes.

- `dbdemo/grade/`  
  Grade-related Blueprint, forms, and routes.

- `dbdemo/templates/`  
  HTML templates rendered by Flask.

- `run.py`  
  Starts the Flask application.

- `db-project-demo.sql`  
  SQL file used to create and initialize the database.

- `seed_reviews.py`  
  Generates additional students and player-style review data.

- `populate_embeddings.py`  
  Populates vector embeddings for the reviews.

- `Dockerfile`  
  Defines the Flask application container.

- `docker-compose.yml`  
  Defines the Flask and MariaDB services.

- `zzz-grants.sql`  
  Grants privileges to the configured MariaDB user.

---

## Database Schema

The original demo contains two main tables:

- `students`
- `grades`

The relation is:

- each student has a unique `id`
- each grade belongs to a student through `student_id`
- one student can have many grades

The extended version also includes:

- `player_reviews`

The `player_reviews` table stores:

- the related student
- the manager name
- the player archetype
- the review text
- the review vector embedding

This allows the application to combine relational data, text data, and vector similarity search.

---

## Dockerized Execution

The project runs with Docker Compose.

The `docker-compose.yml` file defines two services:

- `app`  
  Runs the Flask application.

- `db`  
  Runs the MariaDB 11.8 database.

The application is available at:

```text
http://localhost:3000
```

---

## How to Run the Project

Follow these steps from a terminal.

### Step 1: Clone the repository

```bash
git clone https://github.com/KostasBitsakos/Databases_6th_semester.git
cd Databases_6th_semester
```

### Step 2: Build and start the containers

```bash
docker compose down -v
docker compose up -d --build
```

This will:

- build the Flask application container
- start the MariaDB database container
- initialize the database
- start the web application

### Step 3: Wait for the database to initialize

Wait a few seconds after starting the containers.

The database is initialized automatically using:

- `db-project-demo.sql`
- `zzz-grants.sql`

These files are executed automatically by MariaDB when the database volume is created for the first time.

### Step 4: Populate the review data

```bash
docker compose exec app python seed_reviews.py
```

This script creates:

- additional dummy students
- player review texts
- manager names
- player archetypes

### Step 5: Populate the vector embeddings

```bash
docker compose exec app python populate_embeddings.py
```

This script fills the `embedding` column of the `player_reviews` table.

The embeddings are used for similarity search.

### Step 6: Open the application

Open your browser at:

```text
http://localhost:3000
```

---

## Available Pages

After running the project, you can visit:

```text
/
```

```text
/students
```

```text
/grades
```

```text
/reviews
```

```text
/similarity
```

The application includes:

- a landing page
- a students page
- a grades page
- a reviews page
- a similarity search page

---

## Similarity Search

The extended version supports similarity search on player reviews.

Each review is stored:

- as normal text
- as a vector embedding

The text is used for reading and display.

The vector is used for comparing reviews.

Similarity search is computed inside **MariaDB**, using vector functions such as:

```sql
VEC_FromText(...)
```

```sql
VEC_ToText(...)
```

```sql
VEC_DISTANCE_COSINE(...)
```

General flow:

1. The user selects a query from the web page.
2. Flask receives the request.
3. Flask sends a SQL query to MariaDB.
4. MariaDB compares the vectors.
5. The closest reviews are returned.
6. Flask displays the results.

---

## Types of Similarity Search

### 1. Fixed-query similarity search

The user selects a predefined player profile, such as:

- pacey winger
- creative playmaker
- target striker
- ball-winning midfielder
- ball-playing centre-back
- sweeper keeper

The selected profile is converted into a vector and compared with the stored review embeddings.

### 2. Review-to-review similarity search

The user selects an existing review.

The application returns the most similar reviews based on the stored embeddings.

This demonstrates how vector similarity can be used to find related database records.

---

## Reset and Rebuild from Scratch

To completely reset the project, run:

```bash
docker compose down -v
docker compose up -d --build
docker compose exec app python seed_reviews.py
docker compose exec app python populate_embeddings.py
```

This will:

- stop the containers
- delete the old database volume
- rebuild the application
- recreate the database
- insert the review data again
- populate the embeddings again

Use this when you want a clean start.

---

## Useful Docker Commands

Start the project:

```bash
docker compose up -d
```

Stop the project:

```bash
docker compose down
```

Stop the project and delete the database volume:

```bash
docker compose down -v
```

Rebuild the project:

```bash
docker compose up -d --build
```

View all logs:

```bash
docker compose logs -f
```

View only Flask app logs:

```bash
docker compose logs -f app
```

View only database logs:

```bash
docker compose logs -f db
```

Check running containers:

```bash
docker compose ps
```

---

## Basic Troubleshooting

### The application does not open

Check that the containers are running:

```bash
docker compose ps
```

If needed, restart the project:

```bash
docker compose up -d --build
```

### The database seems empty

Run again:

```bash
docker compose exec app python seed_reviews.py
docker compose exec app python populate_embeddings.py
```

Then refresh the browser.

### Changes in the SQL file do not appear

MariaDB runs the initialization SQL files only when the database volume is empty.

To force re-initialization, run:

```bash
docker compose down -v
docker compose up -d --build
docker compose exec app python seed_reviews.py
docker compose exec app python populate_embeddings.py
```

### Similarity search returns no results

Make sure the review data and embeddings have been created:

```bash
docker compose exec app python seed_reviews.py
docker compose exec app python populate_embeddings.py
```

---


## Acknowledgment

This project started from the original [Databases-Python-Demo](https://github.com/DimK19/Databases-Python-Demo).

It was extended with:

- Docker support
- MariaDB 11.8
- additional review generation
- stored vector embeddings
- similarity search functionality

The project is intended for educational use in the Databases laboratory course.
