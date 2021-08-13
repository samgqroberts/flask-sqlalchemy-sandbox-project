# Flask-SQLAlchemy sandbox project

In order to create the proper MySQL database process, use the newdb script to create and run
a Docker container for MySQL.

```bash
$ ./newdb
```

In order to populate that process with the proper database and tables, use the python shell:

```python
>>> from myapp import create_app, db
>>> db.drop_database("myapp")
>>> db.create_database("myapp")
>>> db.create_all_tables(create_app())
```
