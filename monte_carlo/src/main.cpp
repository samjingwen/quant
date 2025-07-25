#include "FileReaderFactory.hpp"
#include <iostream>

int main() {
  const auto reader = FileReaderFactory::create(FileType::CSV);
  const auto prices = reader->read("../data/sample_prices.csv");

  std::println("Read {} closing prices:", prices.size());

  for (size_t i = 0; i < prices.size(); ++i)
    std::println("Day {}: {}", i + 1, prices[i]);

  return 0;
}
