# s23-resourceful-Anjoliekate
s23-resourceful-Anjoliekate created by GitHub Classroom

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
Create User              | POST   | /users/*\<id\>*
Login User               | POST   | /users/*\<id\>*

bcrypt.hash(password) to store encrypted password and bcrypt.verify(password) to compare encrypted passwords. 
# s23-authentication-Anjoliekate
# s23-authentication-Anjoliekate
