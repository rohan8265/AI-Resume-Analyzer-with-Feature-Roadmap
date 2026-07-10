# Log Report

Analyze the Apache-style access log located at `/app/access.log` and produce a JSON report.

Write the report to:

```
/app/report.json
```

The report must be a JSON object containing **exactly** these three fields:

```json
{
  "total_requests": <integer>,
  "unique_ips": <integer>,
  "top_path": "<string>"
}
```

Field definitions:

- **total_requests** — the total number of valid HTTP request lines in the log.
- **unique_ips** — the number of distinct client IP addresses that appear in the log.
- **top_path** — the request path (e.g. `/index.html`) that appears most frequently. If there is a tie, return any one of the tied paths.

## Success Criteria

1. Read every valid request line from `/app/access.log`.
2. Count the total number of requests and store it in `total_requests`.
3. Count the number of unique client IP addresses and store it in `unique_ips`.
4. Determine the most frequently requested path and store it in `top_path`.
5. Write the JSON report to `/app/report.json` with exactly the three field names shown above (`total_requests`, `unique_ips`, `top_path`).
