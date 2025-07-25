#include "FileReaderFactory.hpp"
#include "CSVFileReader.hpp"

std::unique_ptr<FileReader> FileReaderFactory::create(const FileType type) {
    switch (type) {
        case FileType::CSV:
            return std::make_unique<CSVFileReader>();
        case FileType::Parquet:
            throw std::runtime_error("ParquetFileReader not implemented yet.");
        default:
            throw std::runtime_error("Unknown ReaderType");
    }
}
