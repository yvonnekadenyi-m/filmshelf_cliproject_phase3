# FilmShelf CLI Project
A simple Command Line Interface (CLI) application to manage your personal movie watchlist. Built with Python and SQLAlchemy ORM for Phase 3 project requirements.

## Problem Statement
In today's world, people watch movies and TV shows across many platforms, often losing track of what they have watched or want to watch next. Most existing watchlist tools are tied to specific streaming services, require internet access, or contain ads. FilmShelf provides a simple, offline and personalized solution for managing your movie watchlist.

### Features

User Management
- Create multiple users
- List all users
- Delete users
- Switch between users

Wachlist Management
- Add movies to your personal watchlist
- View all movies in your watchlist
- Mark movies as watched
- Remove movies from watchlist

Reviews and Ratings
- Write reviews for movies
- Rate movies (1-5 stars)
- View all your reviews

Database Persistence

- All data stored in SQLite database
- SQLAlchemy ORM for database operations
- Proper relationships between models


- SQLite database with Alembic migrations

- Clean tabular CLI output with [tabulate]

- Input validation and beginner-friendly design


#### Technology Stack

Python 3.12+
SQLAlchemy - ORM for database operations
Tabulate - Clean table display in CLI
SQLite - Lightweight database
Alembic

##### Database Design
The application uses **SQLAlchemy ORM** with 4 related tables:

- **User** → can add reviews  
- **Movie** → belongs to a genre, can have reviews  
- **Review** → links users to movies  
- **Genre** → categorizes movies  

###### Installation & Setup

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd Project
   ```
2. Install dependencies:
   ```
   pipenv install
   ```
3. Initialize the database:
   ```
   python cli.py
   ```

## Usage

Run the CLI:
```
python cli.py
```

Menu options:
- 1: Add movie
- 2: List movies
- 3: Delete movie
- 4: List genres
- 5: Add user
- 6: List users
- 7: Delete user
- 8: Add review
- 9: List reviews
- 0: Exit

 ## Learning Goals Demonstrated

Python fundamentals → CLI logic, user input/output

Data structures → lists, dicts, tuples in CLI functions

OOP & Inheritance → SQLAlchemy models

SQL & ORM → CRUD operations, relationships

Application structure → modular code
 
## Author

Yvonne Kadenyi 

## License

MIT License


