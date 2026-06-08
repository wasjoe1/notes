#include<iostream>

class Log {
public:
    // default constructor => no need to create

    // higher the level, less stuff is printed
    // 1 - info
    // 2 - warn
    // 3 - error => something broke

    // make LEVEL:
        // static -> so that every single Log object shares the LEVEL variables & not create new ones
        // const -> const so that variables cant change it across the program (val is evaluated run-time)
            // => can also use constexpr - means value is evaluated at (compile-time) => compiler replaces variable name with the actual value everywhere it appears
            // => faster & more efficient => doesnt look up variable in mem while the program is running

    // version 1: static constexpr variable
    // static constexpr int LEVEL_INFO = 1;
    // static constexpr int LEVEL_WARN = 2;
    // static constexpr int LEVEL_ERROR = 3;

    // version 2:
        // plain enum (not enum class) => values leak into the Log class scope, can just use the LEVEL_INFO, LEVEL_WARN, LEVEL_ERROR (belongs to Log's namespace)
        // write it inside the class => keep global namespace clean; write inside class namespace
        // enum is static on its own; coz type definition => redundant to type static enum

    // 
    enum Level {  // Level is the same of the new custom data type
        // s_LevelInfo, // not a variable! should not use s_...
        LEVEL_INFO,  // named constants => just a value
        LEVEL_WARN,
        LEVEL_ERROR,
    };


private:
    Level m_log_level = LEVEL_INFO; // m means class member variable

public:
    void set_level(Level level) {
        m_log_level = level;
    }

    void info(const char* message) {
        if (m_log_level <= LEVEL_INFO) {
            std::cout << "[INFO]: " << message << std::endl;
            // std::endl does 2 things:
                // 1. adds a newline
                // 2. flush buffer
        }
    }

    void warn(const char* message) {
        if (m_log_level <= LEVEL_WARN) {
            std::cout << "[WARN]: " << message << std::endl;
        }
    }

    void error(const char* message) {
        if (m_log_level <= LEVEL_ERROR) {
            std::cout << "[ERROR]: " << message << std::endl;
        }
    }
};

int main() {
    Log logger;
    // logger.set_level(Log.LEVEL_INFO); // sets to level info
    logger.set_level(Log::LEVEL_INFO); // clean way of declaring class level property, not to specific obj // sets to level info
    logger.info("test info");

    logger.set_level(Log::LEVEL_ERROR);
    // should not print
    logger.warn("test warning!");
    // should print
    logger.error("test error!");
}