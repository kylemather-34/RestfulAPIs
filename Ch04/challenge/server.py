"""Write a handler to query logs.
The handler accept the following query parameters:
- offset (default to 0)
- count (default to 100)

    GET /logs?offset=10&count=20

If should use db.query_logs to get the logs and return them as a JSON response in the
following format:
{
    "count": <count>,
    "offset": <offset>,
    "logs": [
        {"level": "INFO", "time": "2024-01-01T00:00:00", "message": "Log message #0000"},
        {"level": "WARNING", "time": "2024-01-01T00:00:12.345000", "message": "Log message #0001"},
        ...
    ]
}

If the HTTP header `Accept` is set to `text/csv`, the handler should return the logs in
CSV format:
    level,time,message
    INFO,2024-01-01T00:00:00,Log message #0000
    WARNING,2024-01-01T00:00:12.345000,Log message #0001
    ...

If now logs matches the query, return a 404 (NOT_FOUND) response.
Don't forget to validate everything.

"""
