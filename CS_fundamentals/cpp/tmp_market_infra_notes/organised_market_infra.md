# Market Infra

market data infrastructure system includes these components:
- market data handler/ feed handler - connect to upstream exchange server, normalize feed, persist/ distribute data
- orderbook engines - stateful component that owns an orderbook instance to maintain the live book (orderbook is just a data structure)
    - book reconstruction engine (client side) - core system that builds & maintains a replica of the exchange's order book
    - matching engine (exchange side) - core system of an electronic exchange that accepts incoming orders, runs priority logic & pairs buy & sell orders
- time series store - DB storing timeseries data

* It seems that the industry has different definitions for each component and I have laid out my understanding of each component

## Project research

### Orderbook

L1 BBO [best-bid-offer] - best ask & best bid; 1 number for each
L2 MBP [market-by-price] - includes quanty for each price level available in the orderbook (all price available & quantity)
L3 MBO [market-by-order] - focuses on queue priority (i.e. time-price priority); can actaully eval which orders get filled

explanation: https://youtu.be/C24m5WEYWxE?si=UGaGBp3_XpxJL89I

### Matching engine

Matching engines accepts *raw incoming orders* and processes them to create an output (i.e. L3 orderbook events, fill/ no fill events etc.)

3 contexts where a matching engine lives:
1. exchange (coinbase, NYSE etc.) - every exchange runs this, & its the output observed by my client side ingestor
2. HFT/ broker as a dark pool/ alternative trading system (ATS) - some large firms run their own external matching engines that other clients can route orders to.
    its technically a private exchange.
3. HFT (internally) cross network use case, purely internal

* "toy matching engine" refers to simulating what the exchange does => accept orders, run price-time priority, emit fills

### live & backtest mode

live:
     Coinbase server ->   feed handler  -> parse JSON/ FIX  -> normalize -> update orderbook (in-MEM)   [SPSC queue 1]
                          receive bytes
                                                            -> store JSON/ FIX on Disk                       [SPSC queue 2]

- Feed handler - connects, pull, parse
- Orderbook engine - maintain book state
- Time series store - stores events

backtest:
    Disk -> replay engine -> orderbook (in-MEM) -> publish state
                                                        |
     ---------------------------------------------------
    |
     -> strategy -(submits order) -> matching engine -(send fill / no fill result)
            ^                                                |
            |                                                |
             ------------------------------------------------

- Replay engine - pulls events from disk, preserves timing
- Orderbook engine - maintains book state
- Matching engine - determines if strategy's orders will fill / no fill
- Strategy - program that receives orderbook state & decides an action (i.e. send order to matching engine)

during live:
- store raw events from the API as ~~JSON~~ binary structs on disk; store raw bytes to avoid expensive re-parse & wasting disk space
- feed handler is thread 1 (parse, convert, drop data into both queues); orderbook engine is thread 2; disk write is thread 3
- SPSC queues prevents block on disk I/O or on book update
- now() = wall clock (~~std::chrono~~ or RDTSC)

during backtest:
- assumption is that market moves independent of the strategy's action, hence we dont update orderbook with orders filled by matching engine
- we send results of whether order was filled or not filled back to the strategy, so that it knows its current position
- now() = event's recorded timestamp; not the actual current time (logical time vs physical time)

test orderbook engine:
- verify: run in matching engine mode & verify results of stored L3 events => should return the same results
- benchmark: parsing latency (both JSON, FIX formats)

### Orderbook engine: Book reconstruction engine vs Matching engine

(client side)
published L3 orders
    +               -> Book reconstruction -> update orderbook state
orderbook state               engine

(backtest)
raw orders
    +               -> Matching engine ->   publish L3 orders (fill / no fill) -> fill / no fill result
orderbook state

(exchange side)
raw orders                                  publish L3 orders (fill / no fill)
    +               -> Matching engine ->           +
orderbook state                             update orderbook state

* The orderbook engine is designed to operate in two modes
    - as a book reconstruction engine consuming processed L3 events on the client side
    - as a matching engine consuming raw orders on the exchange side.
        The core price-time priority logic is identical in both cases.

### venues & their protocols

| Venue         | Protocol      | Transport
| ----------------------------------------------
| NYSE, NASDAQ  | ITCH/ OUCH    | UDP multicast
| CME           | MDP 3.0       | UDP multicast
| FIX engines   | FIX protocol  | TCP (co-located)
| Coinbase      | Websocket     | TCP
| Internal HFT  | custom binary | UDP or shared MEM

* FIX runs on top of TCP
    - TCP natively supports long-lived, persistent connections (socket can stay open indefinitely)
    - raw TCP socket is a reliable 2 way pipe between 2 IP address, only closes when FIN or RST packet received
    - firewalls & routers will eventually forget about idle connections to save MEM => sockets kept open via FIX's heartbeat protocol

* Websocket runs on top of TCP
    - while TCP is fully duplex & persistent, web browsers do not allow raw TCP sockets for security reasons
    - WS connection starts as a standard HTTP req over port 80 or 443 (firewall allows) then uses HTTP Upgrade header to
        switch existing TCP connection from HTTP mode into WS mode
    - Raw TCP is a continuous stream of bytes; WS allows send/ receive of complete structured text strings like JSON or binary blobs

* FIX vs Websocket
    | Feature           | FIX connection                     | Coinbase websockets
    | ----------------------------------------------------------------------------------------
    | Transport layer   | raw TCP sockets (via SSL)          | TCP socket (via HTTP Upgrade)
    | APP layer         | FIX session protocol (i.e FIX 5.0) | Websocket protocol (wss://)
    | Data format       | custom TAG=VALUE(ASCII)            | JSON
    | Browser compatible| No                                 | Yes
    | Primary use case  | institutional order entry          | retail real time monitoring
    |                   | & market data                      | & streaming
    * this comparison helps me to visualize how to handle coinbase's messages as i have experience working with FIX messages (provides familiarity)

* 1 socket =/= 1 port
    - multiple sockets can use the same port (i.e. web server running on port 443 handles thousands of different client connections, each connection has unique socket)
    - a port is just a number allocated by the OS, it does not strictly need a socket
    - for tcp, u need a listening socket to accept new connections, which then spawns separate "connection socket" for each client
    - for udp, it uses 1 soket to handle ALL incoming & outgoing data for that port, clients are differentiated via src IP & src port

* Why UDP for multicast (production)
    - no connection overhead
    - no ACK RTT
    - 1 packet fans out to all subscribers simultaneously
    - easier to implement *kernel bypass* over UDP


## Coinbase exchange API

coinbase home page > developers > developer platform > trading > view docs 

**Coinbase Developer Platform Exchange** offers a websocket feed which provides real-time market data updates for order & trades

### Channels
- heartbeat
- status
- ticker
- ticker batch
- level2
- level2 batch
- user
- matches
- full
- auction

### APIs
- REST API - for lower-frequency trading and general requests.
- FIX Order Entry API - for higher-frequency trading.
- WebSocket Feed - for market data.
- FIX Market Data API - for latency sensitive market data feeds.

* why FIX over WebSocket(JSON)
    while both maintain persistent & duplex TCP connections:
    - JSON
        - must string-parse the incoming text, allocate MEM for strings & convert them into floats or doubles -- induces parsing overhead (string manipulation)
        - coinbase's L2 or ticker websockets broadcasts high volumes of aggregated data over a single stream, client has to do heavy lifting of sorting through
    - FIX
        - doesnt need to look for closing brackets; iterates through bytes sequentially, maps IDs to MEM offsets, utilize fixed width arrays
        - coinbase's FIX market data API allows precise subscriptions via explicit MarketDataRequest (MsgType=V)

### Connect

tcp+ssl://fix-ord.sandbox.exchange.coinbase.com:6121

### References

Coinbase:
- help page: https://help.coinbase.com/en/developer-platform/websocket-feeds/exchange (documents channels)
- institutional APIs: https://docs.cdp.coinbase.com/exchange/introduction/welcome

Helpful articles:
- Market data feed handler + matching engine: https://github.com/omerhalid/Real-Time-Market-Data-Feed-Handler-and-Order-Matching-Engine
- 
    - https://github.com/amor71/LiuAlgoTrader
    - https://liualgotrader.readthedocs.io/en/latest/Concepts.html


## Project goals / implementations

### Optimizations
- SPSC(single producer single consumer) queue
- cache aware design

### Benchmarks

coinbase server <-(1)-> websocket feed handler <-(2)-> SPSC queue <-(3)-> orderbook engine <-(4)-> book update

(1) ~~network RTT~~ - geographical latency  => CANNOT bechmark
(2) paring + normalization - latency to decode raw message to struct => CAN benchmark
(3) SPSC queue round trip time -  => CAN benchmark
(4) orderbook latency - latency to process order (add, cancel, modify) => CAN benchmark

