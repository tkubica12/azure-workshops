# GraphRAG with Azure Database for PostgreSQL
Level 1 notebooks showcase basic capabilities using PostgreSQL
- Full-text search
- Vector search
- Query rewriting
- Hybrid search
- Semantic ranking

Level 2 notebooks showcase advanced capabilities using PostgreSQL
- GraphRAG-like solution with extraction of traits (communities) and use AGE extension to build graph in PostgreSQL
- Generating summaries of the traits/communities
- Combining graph solution with vector search
- Different query strategies using global and local context
- Ad-hoc graph traversal queries

Level 3 notebooks showcase active multi-step AI search with planning using Azure SQL (aka Deep Research)
- GraphRAG-like solution using Azure SQL to implement 3 types of search in single query language - full-text, vector and graph
- Generating summaries of the traits/communities
- AI creating query strategies and generating SQL queries
- If database returns error during execution of specific query, AI attempts to fix the query
- After all queries are executed, AI evaluates quality of responses, selects the best one and scales it further (get more results from that strategy)
- AI compiles final answer

Note: you can skip data preparation for level 2 and level 3 by importing all precalculated data I backed up from the database into `./db_data_backup` folder.
