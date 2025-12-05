# selenium

# understanding of selenium
# - python program spawns server process(driver process), which communicates with python program via TCP connection (hence u can see TCP connections opened between localhost's ports via lsof -p <pid>)
# - the protocol for python code <-> driver is WebDriverProtocol
# - driver process spawns browser process
# - driver sends commands to the browser process => browser execs commands -> sends back to driver -> propagated to python program
# - this server process receives the communicated instruction then propagates it to the browser process

# Visualization
'''
Python program
    │
    ▼  HTTP/WebDriver protocol (TCP)
Driver process (chromedriver / geckodriver)
    │
    ▼  Browser automation protocol (DevTools Protocol for Chrome)
Browser process (Chrome/Firefox)
'''

# Why have a separate driver process?
# - to not need an implementation for every single browser for python (or any other language that selenium supports)
    # => python only needs to implement 1 standard WebDriver API => then the python program can communicate with the driver via WebDriver protocol
    # => any other languages also just need to interact with selenium driver via WebDriver protocol
    # => theoretically can skip the driver & implement a direct client for each browser's protocol BUT u'd need separate implementation for each browser PLUS each language also needs its own implementation now
        # => (n) # of langs * (m) # of browsers = O(nm)
        # => vs (n) # of langs * 1 WebDriver protocol client = O(n)
# - cross language compatability => covered above
# - separate driver language agnostic program => Encapsulation of browser-specific protocol complexity