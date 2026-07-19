# Ticket 37137 - Replace raw SQL suggestion in TIME_ZONE docs

- **Branch:** `ticket-37137`
- **Date:** 2026-07-11
- **URL:** https://code.djangoproject.com/ticket/37137

## Summary


### Notes

- Original docs says
> Consider converting to local time explicitly with `AT TIME ZONE` in raw SQL queries instead of setting the `TIME_ZONE` option

This is in the context of the DATABASE setting.
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydatabase",
        "USER": "mydatabaseuser",
        "PASSWORD": "mypassword",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "TIME_ZONE": "UTC"
    }
}
```

Setting it here tells the connection to use UTC for the database.
Docs notes that it is very rarely needed. It is needed when using raw sql and datetime arithmetic.
Problem is, arithmetic can become confusing.

Original doc suggested using AT TIME ZONE in raw sql rather than using the TIME_ZONE setting on the database connection.

New doc suggestion is to use Func()

# Questions

What's the difference between `template` field and `function` field of `Func`?

Example of a postgres function using template attribute:
```python
class RandomUUID(Func):
    template = "GEN_RANDOM_UUID()"
    output_field = UUIDField()
```

Example of a postgres function using function attribute:
```python
class TimeZone(Func):
	function = "timezone"
	output_field = DateTimeField()
```

# PR Review

- Would it read better to have the code example from the Query Expressions page be inline here? Then the cross-reference mentioned by Natalia would just point to the func docs for more information.
- Would it be useful to add a test for the code example? Similar to what is done in [`test_trunc_filter_non_utc_active`](tests/db_functions/datetime/test_extract_trunc.py)?
