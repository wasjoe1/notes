# Design patterns
This notes cover design patterns used in software.

# 8 common design patterns by neetcode

# -------------------------------------------------------------------------------------------------
# 8 common design patterns by neetcode
`creational`
1. factory method - creates objs without exposing exact class of the instance being created
2. singleton - class only has 1 global instance
3. builder - constructs complex objs step by step (building custom burger)

1. factory method
    - not the same as singleton!! => its own design pattern
    - mainly to provide an interface for creating objs without exposing the concrete class
    ```cpp
    class Shape {
        public:
        virtual void draw() = 0;
    };

    class Circle : public Shape {
        public:
        void draw() override {}
    };

    class ShapeFactory {
        public:
        static Shape* createShape() {
            return new Circle();
        }
    }
    // this shows that Circle class constructor was never exposed, yet we can create a Circle instance via the
    // ShapeFactory by calling createShape => & then it still has the draw method
    ```
2. Singleton
    - only class itself can create a single instance
    - need a factory method => more accurate to say a singleton uses a static factory method to control obj creation
        1. private constructor
        2. static storage of instance
    ```cpp
    class Logger {
    public:
        static Logger& getInstance() {
            static Logger instance; // static instace that holds the single instance of the classs
            return instance
        };
    private:
        Logger() {} // private constructor
    };

    // THUS
    Logger log; // X compile error => this actually does 1. allocate mem for log, constructor for Logger() is called, obj is initialized => constructor is actually called!!
    Logger* log = new Logger(); // X compile error
    ```
