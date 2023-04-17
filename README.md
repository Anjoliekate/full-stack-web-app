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

## Schema

```sql
CREATE TABLE songs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
album TEXT,
genre TEXT,
artist TEXT,
year INTEGER);
```

## REST Endpoints

Name                           | Method | Path
-------------------------------|--------|------------------
Retrieve song collection | GET    | /songs
Retrieve song member     | GET    | /songs/*\<id\>*
Create song member       | POST   | /songs
Update song member       | PUT    | /songs/*\<id\>*
Delete song member       | DELETE | /songs/*\<id\>*
# s23-authentication-Anjoliekate
# s23-authentication-Anjoliekate
