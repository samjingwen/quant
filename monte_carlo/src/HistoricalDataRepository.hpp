#pragma once
#include <string>
#include <vector>

class HistoricalDataRepository
{
  public:
    static std::vector<double> load_close_prices(const std::string& filename);
};
