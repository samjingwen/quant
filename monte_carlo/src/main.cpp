#include "HistoricalDataRepository.hpp"
#include <iostream>

int main()
{
    auto prices = HistoricalDataRepository::load_close_prices("../data/sample_prices.csv");

    std::cout << "Loaded " << prices.size() << " closing prices:" << std::endl;

    for (size_t i = 0; i < prices.size(); ++i)
        std::cout << "Day " << i + 1 << ": " << prices[i] << std::endl;

    return 0;
}