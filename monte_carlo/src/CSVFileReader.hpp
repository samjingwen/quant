#pragma once

#include "FileReader.hpp"

class CSVFileReader final : public FileReader {
public:
  std::vector<double> read(const std::string& filename) const override;
};
