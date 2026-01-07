# Cloudflare outage

This outage occured on 18 nov 2025
Blog by the ceo, matthew prince: https://blog.cloudflare.com/18-november-2025-outage/
GPT prompts to help understanding: https://chatgpt.com/c/692e9371-1504-832b-b423-bb1a37cd3a83

## Context
- not by malicious atacks
- a staff wanted to change the permissions/ priveleges on the DB so that distributed 
- a staff updated their DB system's(clickhouse cluster) permissions for the DB queries, where the perms for distributed DB queries changed from shared system account -to-> 'initial user' accounts
    - this DB is used to store metadata which supports the bot management service that cloudflare provides
- b4 change, devs which asked for table metadata could only see system.tables or system.columns; only able to view the 'default' DB tables
- with the increase in perms, they are now able to see the undelying tables in the 'r0' storage DB -- shard level tables where data is physically stored
- aim was to improve transparency & reliability for distributed queries; query engine would have explicit correct access to all relavant underlying data

## Cause
- an existing internal job that built 'feature file' for the bot managemet system by querying clickhouse's col metadata for a table named 'http_requests_features'
- the 'default' DB and underlying storage tables both had the same table names & thus duplicate rows were returned; SQL query did not specify a specific DB name to return this from
- a larger than expected feature file was generated & propagated to all the server machines that make up cloudflare's network
- SW running on these machines to route traffic, reads this feature file BUT this SW sets a limit on the size of the feature file
- this size limit is below double the size => causing the SW to fail

Why fluctuations before consistent system failure?
- file is generated from a clickhouse query ran on the DB cluster every 5 mins
- the generation of the file could come from a 'bad' or 'good' replica shard of the DB cluster
- hence sometimes a 'good' file is generated, & sometimes 'bad'

## Solution
- generate an old good file
- manually insert into the feature file distribution queue
- force restart of core proxy => the proxy server which users make requests for cloudflare bot services
