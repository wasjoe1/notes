possible projects to look into:
DATABASES:
- clickhouse - open source column oriented SQL DB designed for OLAP (online analytical processing), allows generating analytical data reports in real-time
    built for modern hardware & desgined from scratch when C++20/ 23 was introduced (uses the latest features)
    maintainers are intensely active on github
    actively look for community contributions
    aggressively tag issues for newcomers `easy task`, `help wanted` - team doesnt have immediate bandwidth but are well-defined `good first issue` or `intern tasks ____/____` or `task for contributors`
~~- MySQL - (30+ years old) => not so good as it contains complex hybrid ancient procedural C & newer object-oriented C++~~
~~- MongoDB - => not so good as its packed with deeply nested custom libraries~~
META:
- folly - meta's core lib of C++ components, containing high performance alternatives to the C++ std lib
- velox - meta's C++ DB acceleration engine
GOOGLE:
- abseil - google's open source collection of core C++ lib code to augment C++ std lib
SYSTEMS:
- envoy project - graduate project serving as gold standard for large-scale enterprise-grade cloud native C++ architecture
- serenityOS - systems-level programming written in modern C++

PR to look at:
- already merged requests: Pull request tab, check `is:pr` `is:merged`
    - meaning that they were approved by maintainers and are good code that got merged
- refactors: `label:architecture` or `label:refactor`
    - as these include code that went from "bad" to "good"

some comments worth noting:
- use `std::move` to avoid copy
- should be passed as const `std::string_view` instead of const `std::string&`
- this raw pointer introduces a lifetime risk, please wrap this in `std::unique_ptr`