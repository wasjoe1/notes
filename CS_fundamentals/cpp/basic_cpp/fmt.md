
```cpp
#include <iostream>
#include <fmt/core.h>

int main() {
    int old_price = 5;
    int new_price = 5;
  
    // old std:: method
    std::cout << "Old Price: "<< old_price << ", New Price: " << new_price << "\n";

    // new fmt method
    fmt::print("Old Price: {}, New Price: {}\n", old_price, new_price);
}
```

- fmt
    - can think of it like `std::cout << std::format("Price: {}\n", price);`
    - faster than iostream
    - type safe
    - easier formatting
    - thread safe BUT if multiple threads print simultaneously , outputs can interleave
    i.e.
    Hello from thrHello from thread 2
    ead 1
    * thus production systems usually log through a logger
- spdlog
    - adds timestamp, log level, formatting
    ```cpp
    // i.e. emthods => let u cotntrl verbostiy
    spdlog::debug("Orderbook update {}", seq);
    spdlog::warn("Reconnect triggered");
    spdlog::error("Websocket disconnected");
    ```
    - can have sync logging in dev first
    - then in production systems, instead of blocking threads when trying to log => use async logging
        - print tolog queue instead of console
        - can even consider turning off logging if latency really matters (though might not be the best coz then u lose logs of what happened)
    