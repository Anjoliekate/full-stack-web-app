# Fullstack Web-App

## Resource

**Songs**

Attributes:

* name (string)
* album (string)
* genre (string)
* artist (string)
* year (integer)

**Users**

* firstName (string)
* lastName (string)
* email (string)
* password(string)

## Schema

```sql
CREATE TABLE songs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
album TEXT,
genre TEXT,
artist TEXT,
year INTEGER);

CREATE TABLE users (
userId INTEGER PRIMARY KEY AUTOINCREMENT,
firstName TEXT,
lastName TEXT,
email TEXT,
password TEXT);
```

## REST Endpoints

Name                           | Method | Path
-------------------------------|--------|------------------
Retrieve song collection | GET    | /songs
Retrieve song member     | GET    | /songs/*\<id\>*
Create song member       | POST   | /songs
Update song member       | PUT    | /songs/*\<id\>*
Delete song member       | DELETE | /songs/*\<id\>*
Create User              | POST   | /users/
Login User               | POST   | /users/*\<id\>*
Sessions                 | POST   | /sessions/*\<id\*

bcrypt.hash(password) to store encrypted password and bcrypt.verify(password) to compare encrypted passwords. 

## Overview

Full-stack web-app that utilizes javascript, HTML, and CSS to create a full interactive user-platform. This app allows for users to keep track of their favorite songs. It implements REST endpoints GET, POST, PUT, and DELETE to allow the user to take action with their song collection accordingly. Implements full user authentication, authorization, validation, and sessions to ensure a smooth user experience. 

The backend includes python for the server and sqlite for the database. The python server communicates with the sqlite database via a databse handler script that uses the sqlite3 library to handle queries. 
