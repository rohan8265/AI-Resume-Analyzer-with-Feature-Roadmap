#!/usr/bin/env bash
set -euo pipefail

# Parse access.log and produce report.json
python3 -c "
import json
from collections import Counter

requests = []
ips = set()
paths = []

with open('/app/access.log') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        ip = parts[0]
        # Extract the request path from the quoted request string
        # Format: \"METHOD /path HTTP/version\"
        request_field = line.split('\"')[1]
        path = request_field.split()[1]

        requests.append(line)
        ips.add(ip)
        paths.append(path)

path_counts = Counter(paths)
top_path = path_counts.most_common(1)[0][0]

report = {
    'total_requests': len(requests),
    'unique_ips': len(ips),
    'top_path': top_path
}

with open('/app/report.json', 'w') as f:
    json.dump(report, f, indent=2)
"
