# Database-Framework Branch

Branch goal
-----------

The Database-Framework branch contains design work and the initial
implementation plan for the project's database layer and related backend
integration. The primary goal is to define and establish a stable, normalized
SQLite schema, migration scaffolding, and backend plumbing so the scraper and
API can reliably insert, query, and serve recipe data.

Milestones (mapped from Database Roadmap steps)
-----------------------------------------------

1. Identify entities — COMPLETE
   - Recipe, Ingredient, Instruction (Step), User, Collection, and join tables
     have been identified and documented.

2. Define relationships — COMPLETE
   - Establishing one-to-many and many-to-many relationships (Recipe ↔
     Ingredient via RecipeIngredient, Recipe → Instruction, User → Collection,
     Collection → Recipe).
   - Drafting foreign-key constraints and cascade rules.

3. Draft ERD and initial schema — COMPLETE
   - ERD sketch and a starter SQLite schema are being refined. Working through
     types, uniqueness constraints, and normalization choices.

4. Normalize tables and finalize constraints — COMPLETE
   - Remove duplication, finalize the Ingredient master list strategy, add
     indexes, and lock down uniqueness and FK constraints.

5. Implement schema, migrations, and tests — PENDING
   - Add migrations (Alembic / Flask-Migrate), seed scripts, and unit tests
     for insertion and retrieval. Add transactional insertion from scraper.

Progress notes
--------------

- Step 1 (Identify entities) is complete and documented in
  Database Roadmap.md on this branch.
- Steps 2 and 3 are actively being worked on: relationship definitions,
  ERD refinement, and the starter schema are under iteration and review.

Next actions
------------

- Complete relationship documentation and finalize join-table column
  definitions and constraints.
- Convert the starter SQL into migration scripts and add a migration stub.
- Add tests covering scraped-data validation and transactional inserts.

How to review
-------------

1. Open Database Roadmap.md for detailed context and the starter schema.
2. Review new SQL or migration files when they appear in PRs.
3. Run the test suite and local migrations to validate schema changes.

Suggested commit message
------------------------

Add README for Database-Framework branch describing goals and milestones

Contact
-------

If you want to pair on any of the items above, tag me (@EoUReDIt) in a PR
review or open an issue in the repository.
