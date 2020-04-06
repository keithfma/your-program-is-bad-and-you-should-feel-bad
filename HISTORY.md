# Insult Error Change Log

## v0.3.1

+ Makes casting uncaught exceptions to `InsultError`s optional
+ Beautifies error messages by pretending `InsultError` is a builtin
+ Adds unit tests

## v0.3.0

+ Added option to cast all uncaught exceptions to `InsultError`s, thanks to
  to Jacob McDonald for contributing

## v0.2.1

+ Added insults from XKCD "code quality" series, with attribution
+ Some of these new insults are commented out until a future date
  when we have more non-XKCD insult to balance them out.

## v0.2.0

+ Overhauled implementation to make everything much simpler
+ Fixed "bug" that prevented showing different error classes when user called
  raise with Insult error class, not instance
+ Fixed crummy workaround where users had to use a special list in try-except clauses
+ Changed to a 1-10 rating system, which made it easier to assign ratings and
  easier to use them

## v0.1.1

+ New insults contributed by Nick Weir
+ Added InsultErrors tuple to support try-except clauses for all InsultError classes

## v0.1.0

First release
