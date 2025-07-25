#pragma once

#include "FileReader.hpp"
#include "FileType.hpp"
#include <memory>

class FileReaderFactory {
public:
    static std::unique_ptr<FileReader> create(FileType type);
};
