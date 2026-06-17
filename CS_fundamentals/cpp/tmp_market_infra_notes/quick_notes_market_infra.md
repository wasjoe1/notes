# Market infra (quick notes)

# -------------------------------------------------------------------------------------------------
# asio::co_spawn

asio::co_spawn(boost::asio::io_context ioc, net::awaitable<void> awaitable, boost::asio::detached_t net::detached/token)

boost::asio::io_context ioc - event loop driver; engine that will execute the allocated coroutines upon run()
boost::asio::awaitable<void> awaitable - cou=routine to be allocated on to the event loop
boost::asio::detached_t net::detached/token - token that defines the lifecycle & error handling strategy

what it does:
- allocates coroutine frame => reserves MEM for coroutine state, local variables, & execution points?
- attaches the coroutine to the io_context (event loop driver)
- schedules execution => queues coroutine's initial entry step into io_context's queue

# -------------------------------------------------------------------------------------------------
# Boost::asio & Boost::beast

- Boost::asio - library for async tasks in C++
- Boost::beast - lib for web-based networking (hTTP & websocket protocols)

# -------------------------------------------------------------------------------------------------
# async & coroutines in c++ 20

- creating async function: async def do_something() == net::awaitable<T> do_something()
- await a coroutine's execution: await == co_wait
- execute a coroutine with a specified executor (ioc being the executor in this case): asyncio.run(main()) == net::co_spawn(ioc, run(), net::detached) + ioc.run()

* execution only starts when you call `ioc.run`, `net::co_spawn(...)` schedules the coroutines

# -------------------------------------------------------------------------------------------------
# system design (feedhandler & websocket)

- want to keep `FeedHandler` class decoupled from `WebsocketClient` class
    => create 2 different classes
- should i instantiate WebsocketClient separately from FeedHandler? (dependency injection [Aggregation]) OR [Composition]
    [Aggregation] - has-A relationship i.e. Department has a professor, but when the department is "deleted" the professor could still exist
    [Composition] - part-of relationship; sub object cant exist without the parent i.e. a room is part of the house
    => in the current scenario, the feedhandler should be a 1:1 r/s
    => feedhandler uses a websocket but doesnt control its life time [aggregation]
- generally,
    - we instantiate `WebsocketClient` separate from the feedhandler class & pass it in as an argument
    - better decoupling
    - allows the websockClient maintain its own state: maintain its own pool of connections, retries etc.
    - feedhandler doesnt need to know the socket's configs
    - easier testing
- lifetime
    - feedhandler only holds a reference/ pointer to a websoekt, it didnt create & doesnt destroy
    - websocket can outlive the feed handler

    inject by?
    - reference - websocket must outlive feed handler   => because someone else holds the true reference
    - shared_ptr - ownership is shared which adds atomics overhead? => everyone holds a a ptr; u may or may not be the last one (need to increase / decrease counter)
    - unique_ptr - feed handler takes ownership => ownership passed directly to you (no difference from just instantiating it within the feedhandler class)

# -------------------------------------------------------------------------------------------------
# vcpkg git baseline

- acts as the strict ceiling
- when operating in manifest mode, vcpkg requires a strict defined baseline commit => else it will throw a fatal compilation error
- generally for small projects where all the packages are lined up, we just use a `builtin-baseline` in `vcpkg.json` without needing a separate `vcpkg-configuration.json`
```json
{
  "name": "my-json-project",
  "version-string": "1.0.0",
  "builtin-baseline": "3df3411b0e9f69742a78fa8cb27db4ff3c9cb597",
  "dependencies": [
    "nlohmann-json"
  ]
}
```

- the reason we have `vcpkg-configuration.json` is to accomodate larger projects where we have older versions for specific packages
```json
{
  "registries": [
    {
      "kind": "git",
      "repository": "https://github.com",
      "baseline": "deadbeef1234567890abcdef...",
      "packages": [ "internal-logger", "proprietary-crypto" ]
    }
  ]
}
```

* to get the latest commit of the vcpkg:
    - in terminal cli, use: `git ls-remote https://github.com/microsoft/vcpkg.git refs/heads/master`
    - or when in directory with `vcpkg.json` or `vcpkg-configuration.json` use: `vcpkg x-update-baseline --add-initial-baseline`

* `vcpkg x-update-baseline --add-initial-baseline`
    - works by checking ur local git clone vcpk repo (the one pointed to in my `VCPKG_ROOT`)
    - "builtin-baseline": "58950f88544e4637524dbd6a01d0317cf4cb77fc" // this is for a 2024 commit

# -------------------------------------------------------------------------------------------------
# json manipulation & json dump

```cpp
#include <nlohmann/json.hpp>

// method 1:
// Create the JSON message
nlohmann::json msg;
msg["type"] = message_type;
msg["channel"] = channel_name;
msg["product_ids"] = product_ids;
msg["jwt"] = m_token;

// json.dumps (convert json object into flat string)
return msg.dump();

// method 2:
using json = nlohmann::json;
// Create a JSON object (similar to a Python dict)
json my_dict = {
    {"name", "Alice"},
    {"age", 28},
    {"active", true}
};

// Serialize to string (equivalent to json.dumps)
std::string json_string = my_dict.dump(); // dump as a string

std::cout << json_string << std::endl;
```

# -------------------------------------------------------------------------------------------------
# websocket protocol

```python
message = {
    "type": "subscribe",
    "channel": channel_name,
    "product_ids": products
}
# mainly sets message["jwt"] = token, returns message
signed_message = sign_with_jwt(message, channel_name, products)
# parses entire message dict into JSON string & send JSON string
ws.send(json.dumps(signed_message))
```

- websockets dont use HTTP request body & headers once connection is established (HTTP only used in the HTTP handshake)
    - HTTP handshake
    initial _GET_ request sent to `wss://://coinbase.com` => contains HTTP header & body
    CB replies with _status 101_ => protocol change
    (upon success) connection stays open as a raw bi-directional TCP pipe
    - no more headers, status code, req bodies etc. (not HTTP protocol anymore)
- ws protocol wraps JSON string in a frame
- frame only has a few bytes of overhead (`bit` indicating text or binary, `few bytes` indicate length of string, `masking key`)

# -------------------------------------------------------------------------------------------------
# generating intermediate file

intermediate file - file that has substituted code from the preprocessor, but not yet been compiled

```bash
cd build
ninja src/main.cpp.i // processes the file & generate a raw file called main.cpp.i
```

when running the normal build command:
- compiler never produce this intermediate file
- because it goes straight from src code (.cpp) to to binary object files (.o) & links them into the target executable

## use compilation database to generate intermediary file

{
    "directory": "/Users/joechua/Desktop/DEV/projects_production/market_infra/build_debug",
    "command": "/usr/bin/c++ -DBOOST_CONTAINER_NO_LIB -DBOOST_CONTAINER_STATIC_LINK -DBOOST_CONTEXT_EXPORT=\"\" -DBOOST_CONTEXT_NO_LIB=\"\" -DBOOST_CONTEXT_STATIC_LINK=\"\" -DBOOST_DATE_TIME_NO_LIB -DBOOST_DATE_TIME_STATIC_LINK -DPROJECT_SOURCE_DIR=\\\"/Users/joechua/Desktop/DEV/projects_production/market_infra\\\" -isystem /Users/joechua/Desktop/DEV/projects_production/market_infra/build_debug/vcpkg_installed/arm64-osx/include -g -std=gnu++20 -arch arm64 -o CMakeFiles/market_infra.dir/src/main.cpp.o -c /Users/joechua/Desktop/DEV/projects_production/market_infra/src/main.cpp",
    ...
}
- the command here is literally used to create (compilation & linking) the executable
- change -c to -E to only run the preprocessor phase
- change `CMakeFiles/market_infra.dir/src/main.cpp.o` to `-o main.i`
* as such: `-E /Users/joechua/Desktop/DEV/projects_production/market_infra/src/main.cpp -o main.i`

# -------------------------------------------------------------------------------------------------
# compile code (quickly)

`clang++ -g -std=c++17 main.cpp -o prog`

quick ez way to compile code

# -------------------------------------------------------------------------------------------------
# kill process

kill <PID>          defaults to signal 15
kill -15 <PID>      signal 15, kill with clean up (polite request)
kill -9 <PID>       signal 9, force kill

# -------------------------------------------------------------------------------------------------
# authenticate requests to the advanced trade WS API

- create secret API key (API key ID + private key)
- CDP kept the public key on their end
- python script sends subscribe

# -------------------------------------------------------------------------------------------------
# API authentication

okay so i have seen 4 ways that API authentication have been implemented so far.
1. calude: single string (single token system)
2. mongodb: public key (username) + private key (password)
3. coinbase CDP: API keyname (stirng with org & key ids) + private key (real private key)
4. coinbase exchange API: API key (username) + passphrase (password) + API secret (string used to compute hmac)

1. claude: single bearer token
    - include this token directly in the `Authorization: Bearer <token>` header
    - the server then looks it up in its DB, finds associated account & grants access
    - only sent over a secure network (TLS), where a packet sniffer cant theoretically decrypt the message
2. mongoDB: username + password
    - public key & private key are really just username & password
    - also relies on network to be secure => no asymmetric cryptography occurs
3. coinbase CDP: (key name + EC private key), placed in jwt [asymmetric]
    - sign a JWT using the EC private key
    - key name (API keyname) goes in the JWT header as the kID (key id)
    - coinbase server looks up corresponding public key by key name, verifies the signature, & grants access
    * private key is on client, while public key is with server; server decrypts signature using public key
4. coinbase exchange API: API key + passphrase + secret [symmetric]
    - no private key in this; API key (username) + passphrase (password) + secret is just some string that only you and coinbase knows
    - secret is used during the signing of the HMAC signature
    - body: to create HMAC signature, (timestamp + method + path + body) is _hashed_ using the _secret_
    - headers: _API key_ & _passphrase_ are sent as separate headers
    - but everything, your message API key + passphrase are all in there
    - will need a secure connection

# -------------------------------------------------------------------------------------------------
# dependency management (vcpkg.json & vcpkg-configurations.json)

_manifest mode_ - reads json manifest
- vcpkg.json - tells vcpkg what dependencies is required
- vcpk-congfigurations.json - tells vcpkg what registry to use & the baseline git commit we should look at
    * rather than looking at specific library versions, vcpkg's repository is maintained by microsoft where they ensure every lib then at that git hash commit is compatible with 1 another

boost website version of getting started guide (getting started with boost libs): https://www.boost.org/doc/user-guide/getting-started.html

```bash
# OLD
# according to the guide, the syntax below is used to include header only libs:
target_include_directories(my_app PRIVATE ${Boost_INCLUDE_DIRS}) # this is considered 
# and for libs that require compiled binaries, this is used:
target_link_libraries(my_app PRIVATE Boost::filesystem)

# NEW
# however, according to chat, modern CMake just use this for both cases(header-only & compiled-binaries lib) for external libs:
target_link_libraries(my_app PRIVATE Boost::filesystem)
# then this is used to include header files in my project directory
target_include_directories(market_infra PRIVATE include/)
```

- verbose explanation for market_infra project
```bash
cmake_minimum_required(VERSION 3.20)

project(market_infra)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# create compile_commands.json(compilation database) in build folder
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# find the package
# FAILS
# find_package(Boost REQUIRED CONFIG beast) # required config causes cmake to load the master BoostConfig.cmake file & imports all available boost modules & headers that vcpkg installed
    # however, because im in manifest mode, i should just use `find_package(Boost REQUIRED CONFIG)` since "all" refers to the dependecies of the project, not of all the dependencies on my mac previoulsy installed
    # however boost doesnt have individual .cmake configs for each of their components
# this also fails
# find_package(Boost REQUIRED CONFIG) # fails because cmake loads the master configuration file & bundles all header-only tools into the single targe Boost::headers
# which then you should just use 
# target_link_libraries(market_infra PRIVATE Boost::headers) # covers both asio & beast

# # so either do 1:
find_package(boost_asio REQUIRED CONFIG)
find_package(boost_beast REQUIRED CONFIG)
# # or 2:
# find_package(Boost REQUIRED COMPONENTS beast asio)

find_package(OpenSSL REQUIRED)

# create executable => always do so before you try to link libs to it
add_executable(market_infra src/main.cpp)

# now you may link it
target_link_libraries(market_infra PRIVATE Boost::asio)
target_link_libraries(market_infra PRIVATE Boost::beast)
target_link_libraries(market_infra PRIVATE OpenSSL::SSL)
target_link_libraries(market_infra PRIVATE OpenSSL::Crypto)
```

## CMake configure / cmake --preset

during configure stage:
1. vcpkg reads vcpkg.json
2. vcpkg downloads & installs boost & openssl
3. CMake processes CMakeLists.txt
4. find_package() locates the newly installed libs
5. CMake genereates the build rules (ninja/ makefile)
* whenever you edit CMakeLists.txt, you will need to re-run cmake --presets again (i.e. changing the way you compile the binaries)

* build stage is where:
    - pre-processor
    - compilation of individual .cpp files
    - linking

## cmake version

- on my ubuntu OS:
    - my cmake version is 3.28.3.
    - i thought this was old since (iirc) the cmake version on my mac was 4.X.X+
    - apparently cmake (3.28.3) is not considered old for standard linux dev
    - its the default package shipped with ubuntu 24.04 LTS
    - use the command `lsb_release -a` to check Ubuntu OS version
        No LSB modules are available.
        Distributor ID: Ubuntu
        Description:    Ubuntu 24.04.3 LTS
        Release:        24.04
        Codename:       noble
    * note that when building projects, you will see that vcpkg might install newer versions of CMake into its own cache dir to use strictly for building project's libs
        => doesnt replace system's global Cmake
        => project libs are downloaded in to vcpkg_installed in the build folder

## vcpkg repo out of sync

* error due to vcpkg git repo is out-of-sync
```bash
error: while checking out baseline from commit 'b216ddff25a1f432870e6c340ce79357049ef86e', failed to `git show` versions/baseline.json. This may be fixed by fetching commits with `git fetch`.
```
* resolve is to pull commits as vcpkg refers to your local repo's commits and uses baseline commit for reference
    => no commit, no ability to install packages accordingly

# -------------------------------------------------------------------------------------------------
# Boost (Asio & Beast)

Boost.Asio - TCP + TLS
Boost.Beast - builds on Asio, adds HTTP + websocket
* beast handles websocket handshake & framing (App layer), Asio handles TCP + TLS (transport layer)

Asio provides SSL stream wrapper but doesnt implement SSL itself
thus, requirebeast/ssl.hpp for ssl integration (handles all the wrapping & fall back when connection doesnt have valid ssl cert etc.)


# -------------------------------------------------------------------------------------------------
# coinbase API endpoint (public CA or custom CA)

had to recap on how the SSL handshake work
key reminder: the SSL handshake is a authentication process mainly for the client to determine that the server is a trusted server

SSL handshake
- client has standard CA public key OR custom CA public key
- when client sends a 1st hello message, server needs to send back it's SSL certificate (signed by CA private key & cert contains server's public key)
- client receives this SSL cert and, (1) decypts (using CA public key) & compare hashes to determine cert is legitimate, (2) encrypts secret message with server's public key
- server then receives secret & decrypts this using its private key (ensures that server is legitimate)
- then server uses private key to encrypt secret message & send it back to client
- finally, client confirms this connection is legitimate, & both then does symmetric communication using 1 common key (faster to encrypt & decrypt)

OpenSSL
widely used open source software lib that provides the tools to encrypt data & secure communications over computer networks
dont need to re-implement the underlying logic to attach a cert, verify a cert using hash etc.
its like the http library (we dont want to re-implement all the parsing logic etc. and just get the body of a request etc.)

assumption: my assumption is that since coinbase didnt provide a Custom root certificate (custom CA cert), this means that it should be using standard CA verification
to test this:
`openssl s_client -connect fix-md.sandbox.exchange.coinbase.com:6121 -showcerts`
- dont include the _URI scheme_ `tcp+ssl://` as openssl already assumes that you are using TLS over TCP

example output:
joechua@Chuas-MacBook-Air-3 market_infra % openssl s_client -connect fix-md.sandbox.exchange.coinbase.com:6121 -showcerts 
Connecting to 44.208.3.10
CONNECTED(00000005)
depth=2 C=US, O=Amazon, CN=Amazon Root CA 1
verify return:1
depth=1 C=US, O=Amazon, CN=Amazon RSA 2048 M01
verify return:1
depth=0 CN=*.sandbox.exchange.coinbase.com
verify return:1
...

## issue: FIX API are only for institutional investors

when trying to access https://exchange.coinbase.com/ , i get the following message:
"joechua247@gmail.com does not have access to Coinbase Exchange. If you are not applying on behalf of a business, continue to Advanced Trading."

- the advanced trading API only supports REST & websocket APIs
- need to connect to websocket API and draw in data from there instead
- could potentially simulate this environment by having a client send transactions that replay what happened, then have another client trade against it(the strategy program)

* dont be confused by coinbase pro (this was the old name for coinbase advanced trading API)
* additionally it seems that the FIX endpoint is not available to retail traders anymore due to low usage

## links for exchange API
Exchange FIX API Connectivity: https://docs.cdp.coinbase.com/exchange/fix-api/connectivity
FIX message formats: https://docs.cdp.coinbase.com/exchange/fix-api/market-data#logon-35%3Da
exchange sandbox docs: https://docs.cdp.coinbase.com/exchange/introduction/sandbox
exchange sandbox: https://public-sandbox.exchange.coinbase.com/trade/BTC-EUR
create API key for coinbase exchange APIs: https://help.coinbase.com/en/exchange/managing-my-account/how-to-create-an-api-key

## links for advanced trade API
advanced trade API FAQ: https://docs.cdp.coinbase.com/coinbase-business/advanced-trade-apis/faq#what-is-advanced-trade-api (mentions that exchange API is only for institutional clients && what happened to coinbase pro)


# -------------------------------------------------------------------------------------------------
# Clangd multiple presets

faced an issue where clangd (language server) could not read the compilation database(`compile_commands.json`)
this is due to the nested folders in the `build` folder (`build/release` & `build/debug`)
clangd's `CompilationDatabase` flag in `.clangd` can only read folder path of 1 level (hence this worked for `build` before)
i have since updated the presets to use `build_debug` & `build_release`

stack overflow: https://stackoverflow.com/questions/68885293/clangd-for-vscode-with-multiple-build-directories