cmake_minimum_required(VERSION 3.31.6)
project(monte_carlo_simulation)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(monte_carlo
        src/main.cpp
        src/FileReader.hpp
        src/FileType.hpp
        src/FileReaderFactory.cpp
        src/FileReaderFactory.hpp
        src/CSVFileReader.cpp
        src/CSVFileReader.hpp
        src/FileReader.hpp

)
