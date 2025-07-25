#pragma once

#include <string>
#include <vector>

class FileReader {
public:
  virtual ~FileReader() = default;

  virtual std::vector<double> read(const std::string& filename) const = 0;
};
