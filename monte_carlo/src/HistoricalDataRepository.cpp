#include "HistoricalDataRepository.hpp"
#include <fstream>
#include <sstream>

std::vector<double> HistoricalDataRepository::load_close_prices(const std::string& filename)
{
    std::ifstream fin(filename);
    std::string line;
    std::vector<double> prices;

    // skip header
    std::getline(fin, line);

    while (std::getline(fin, line))
    {
        std::istringstream iss(line);

        std::string date, open, high, low, close;

        std::getline(iss, date, ',');
        std::getline(iss, open, ',');
        std::getline(iss, high, ',');
        std::getline(iss, low, ',');
        std::getline(iss, close, ',');

        if (!close.empty())
            prices.push_back(std::stod(close));
    }

    return prices;
}
