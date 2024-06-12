# Trip Management System

<div align="center">
  <div align="center">
    <img src="coverage.svg" alt="coverage"> 
</div>
</div>

## About 


The project utilizes an SQLite database for storing trip-related data and retrieves travel agency information from
a text file. It connects these data sources, enabling comprehensive analysis of travel agency
operations and trip statistics.

## Key Features
- Active Record Approach: used for managing trip data in database allowing to retrieval and manipulation of trip records
within the application.
- Alembic: framework used in project for testing purposes of CRUD operations. Alembic automates setup and teardown 
processes for testing environments, ensuring consistent database structure across different scenarios.


## Test Coverage
This repository includes both pytest and unittest test cases to ensure code reliability and functionality. You can run
the tests using the test runners by executing running the command:
```
pipenv run pytest
```
It is also possible to get insights into test coverage report by running the command:
```
pipenv run coverage report -m
```