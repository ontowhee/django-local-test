# Ticket 37140 - Document how to handle NULL when using filter()/exclude() with `__in subqueries`

- **Branch:** `ticket-37140`
- **Date:** 2026-07-19
- **URL:** https://code.djangoproject.com/ticket/37140

## Summary

No documentation on behavior of filter() and exclude() when using `in` lookup where the rhs value contains NULL. That is, the `in` expression evaluates to UNKNOWN, and the query ends up returning empty set, despite there being rows matching some of the values from the rhs.

## References

- Follows up on [ticket 20024](https://code.djangoproject.com/ticket/20024) and adds documentation.
- Discussion from year 2013: https://groups.google.com/g/django-developers/c/OG1unUV-MOU

## Vocabulary

- filter()
- exclude()
- Lookup
- `<field>__in`
- Subquery
- Exists
- OuterRef
- SQL tri-valued logic (TRUE / FALSE / UNKNOWN)

## Paraphrase Comments

- Bug reporter encountered a real world problem using Subquery that resulted in empty set when it should have returned data.
- Discussion from 2013 proposes updating ORM to use EXISTS instead of IN when working with subqueries.
- [Comment:2](https://code.djangoproject.com/ticket/37140#comment:2) links to several past tickets giving context on the `in` lookup and NULL problem, and Django's decisions for fixing/not fixing it.
- [Comment:3](https://code.djangoproject.com/ticket/37140#comment:3) mentions replacing IN for subqueries with EXISTS is highly unlikely, breaks backwards compatibility, and ORM looks different than the SQL it generates. It also suggests the possibility of introducing an `exists` lookup as an alternative.

## Questions

- Is it a common pattern to reference a ticket in the documentation?

  Answer: A quick grep shows several, with most being open tickets that "may be implemented in the future". Most render phrases that link to the ticket. Only one rendered the ticket number explicitly ("#25313").
- Should the warning section be worded more generically? It currently focuses on subqueries, but the right hand side could be a list as well.

## PR Review

Hello, @SnippyCodes! Thank you for working on this ticket.

The warning section is looking good so far. It addresses both filter() and exclude(). However, it places emphasis on the subquery, whereas the list is only mentioned towards the very end. What are your thoughts on rewording the section to be more generic?

...

## Conclusion

### 2026-07-19
- Left review and question rewording to be more generic for subqueries and lists.
