# MONITORING SYSTEMS

- monitoring systems can be split into 2 categories
    - pull (metric-driven)
        => dont own the app
        => system health & trends; continuous incidents
    - push (event-driven)
        => used for discrete incidents
        => every event matters (logs)

---------------------------------------------------------------------------------------------------
## Metrics monitoring (CPU, MEM, Disk, API latency etc.) [PULL]
- metric scraper (when to use?) - only `PULL` when u dont control the app emitting events
- then why when we own the app that produces the metrics, we still pull the metrics rather than have it push
    => dont want app to decide when & where to send metrics
    => dont want fault in metric apps to block your app
        Bad reasons:
        => affects performance
        => monitoring failure affects prod traffic; back pressure into prod
        => de-centralized => now each app decides whether it sends traffic or not rather than 1 monitoring app deciding

i.e.
* __METRICS PIPELINE == GRAFANA + PROMETHEUS__

    [app] `/metrics` endpoint -> [prometheus] -> [grafana]

- app exposes `/metrics` endpoint
- prometheus __scrapes__ (pulls) metric data every 10-15s
- prometheus stores data in its own built-in time-series DB
- grafana __queries__ prometheus => grafana then renders the data on the UI
    why query?
    - grafana is a stateless visualization client
    - doesnt want to store data; doesnt want to manage backpressure; doesnt want to manage reconnections

---------------------------------------------------------------------------------------------------
## Event driven alerting (logs, bad login attempts, credit card fraud, unauthorized access, etc.) [PUSH]

i.e.
* __LOGS PIPELINE == ELASTIC STACK (ECK)__

    verbose:    [app] (file/ stdout) -PUSH-> [`tail -f /var/log`] -PUSH-> `log tailer/agent` -PUSH-> [logstash] (filter/parse/enrich) -PUSH-> log backend [Elasticsearch] -> [Kibana] UI
    with kafka: [app] (file/ stdout) -PUSH-> [`tail -f /var/log`] -PUSH-> `log tailer/agent` -PUSH-> [Kafka] (buffer/broker) [logstash] (filter/parse/enrich) -PUSH-> log backend [Elasticsearch] -> [Kibana] UI
    overall:    [app] -PUSH-> [tailer] -PUSH-> [kafka] -PUSH-> ([logstash] -PUSH-> [Elasticsearch] -> [Kibana])
                                                                <------------------ECK stack------------------>
- ECK => elastic cloud on kubernetes, official kubernetes operator that manages:
    1. logstash      - Parser => parses logs
    2. Elasticsearch - DB => stores logs & indexed data
    3. kibana        - UI => dashboard to display & query data
    4. kafka         - MSG Broker => buffers & distribute to multiple consumers; sits infront of the ECK stack
- kafka can be used too (i included this in the above architecture)
- use cases: app logs, error traces, audit logs, security logs
- if logs is continuous, why does it follow a push model?
    - it is distinct events that are submitted and used for auditing => cant be pulled at different snapshots
- kafka acts as a broker which accepts messages from producers, store them temp, and deliver to consumers when needed
    - kafka is a distributed message broker
    - producer -> broker -> consumer
    - good use cases:
        1. allows multiple logstash instances to process the same logs independently => single logstash instance cant handle all traffic in a large app => can spin up 3-5 logstash instances
        2. different types of logs => #1 stores in elastic search & used for dashboard, #2 security rules for alerting sus activities, #3 transform & send to s3 for archive

* __both logs & metrics pipelines run inside kubernetes__

* __BAD LOGIN DETECTOR__

    Bad login [event] -> [stream processor] -> [alert]