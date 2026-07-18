# Ticket 25243 — Short description

- **Branch:** `ticket-25243`
- **Date:** 2026-07-12
- **URL:** https://code.djangoproject.com/ticket/25243

## Summary

inspectdb crashes if SQLite foreign key references sqlite_master.

- Home-built "code was doing to partially enforce a home-built generic foreign key constraint".
- The home-built part is the `REFERENCES sqlite_master`.
- sqlite_master is the table that sqlite uses to maintain meta data about the db. Similar to `information_schema` in postgres.
- Bug reporter's workaround was to dump schemas, modify `REFRENCES sqlite_master...` to be `REFERENCES sqlite_master (tbl_name) ON DELETE RESTRICT ON UPDATE CASCADE`, and then recreate the db.
- Bug reporter stated a better error message would help.

Vocabulary
- [inspectdb](https://docs.djangoproject.com/en/6.0/ref/django-admin/#django-admin-inspectdb)
	- A django feature that allows you to point to a table in the database, and it will output the Django model for that database.
	- I tried it out on my project, which had already declared the django models. It output models with `class Meta.managed = False`.
- sqlite_master
    - From Jacob Walls comment on the PR: "This was renamed to sqlite_schema in 3.33.0"

## PR Review

- Test is written with `connection.constraint_checkes_disabled():`.


### Questions
- Why is it necessary to run connection with constraint checks disabled? Does `connection.constraint_checks_disabled():` cause the foreignkey to no longer have the CASCADE? I'm seeing `models.DO_NOTHING`.

```python
with connection.constraint_checks_disabled():
    cursor_execute("""
        CREATE TABLE todos (
			id INTEGER PRIMARY KEY,
			row_id INTEGER,
			table_name VARCHAR(64) DEFAULT 'stories' REFERENCES sqlite_master (tbl_name) ON DELETE RESTRICT ON UPDATE CASCADE COLLATE NOCASE,            content TEXT NOT NULL CHECK(TRIM(content) <> '' AND TRIM(content) = content AND content NOT LIKE '%  %' AND content NOT GLOB '*[
        ]*')
        );
	""")
```

```python
class Todos(models.Model):
	row_id = models.IntegerField(blank=True, null=True)
	table_name = models.ForeignKey('SqliteMaster', models.DO_NOTHING, db_column='table_name', blank=True, null=True)
	content = models.TextField()

	class Meta:
		managed = False
		db_table = 'todos'
```

- Do we need to have a better error message? What is really needed for this ticket in its current state?

### Observations
- Removing the `connection.constraint_checks_disabled():`, we encounter `django.db.utils.OperationalError: foreign key mismatch - "inspectdb_sqlite_master_fk" referencing "sqlite_master"`
- Running the create table with `connection.constraint_checks_disabled()` is not part of the problem reported in the ticket. The ticket is reporting the inspectdb aspect.
- So let's try testing it with `connection.constraint_checks_disabled()`, but use the example provided by the bug reporter. We want to observe the same error that the bug reporter got when they ran inspectdb.

## Reproduction

Use schema from description, create the table in DBeaver. This will update the project's db.sqlite3 file.

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY,
    row_id INTEGER,
    table_name VARCHAR(64) DEFAULT 'stories' REFERENCES sqlite_master (tbl_name) ON DELETE RESTRICT ON UPDATE CASCADE COLLATE NOCASE,
    content TEXT NOT NULL CHECK(TRIM(content) <> '' AND TRIM(content) = content AND content NOT LIKE '%  %' AND content NOT GLOB '*[

]*')
);
```

Then run `python manage.py inspectdb todos`.

Observation: There was no error. The output gave the Django unmanaged model.

```python
class Todos(models.Model):
    row_id = models.IntegerField(blank=True, null=True)
    table_name = models.ForeignKey('SqliteMaster', models.DO_NOTHING, db_column='table_name', blank=True, null=True)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'todos'
```

## Findings

Use LLM to help identify that commit [483e30c3d5](https://github.com/django/django/commit/483e30c3d5) resolved the error. Before, `get_relations()` used regex to parse table and fk relations from schema. Now it queries the db with `PRAGMA foreign_key_list(<table_name>)`. It is now able to handle more complex ON DELETE statements too.

## Conclusion

### 2026-07-12
- Left a comment asking if this should be closed as "worksforme" or proceed with adding regressions test as provided in existing PR.

### 2026-07-13
- Jacob Walls: "we generally add meaningful regression tests when we find accidentally fixed tickets, so +1 for keeping the PR"
