from nautilus_trader.adapters.interactive_brokers.common import IB, IB_VENUE
from nautilus_trader.adapters.interactive_brokers.config import IBMarketDataTypeEnum
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersInstrumentProviderConfig, \
    SymbologyMethod, InteractiveBrokersDataClientConfig, InteractiveBrokersExecClientConfig
from nautilus_trader.adapters.interactive_brokers.factories import InteractiveBrokersLiveDataClientFactory, \
    InteractiveBrokersLiveExecClientFactory
from nautilus_trader.config import LoggingConfig
from nautilus_trader.live.config import TradingNodeConfig, RoutingConfig, LiveDataEngineConfig
from nautilus_trader.live.node import TradingNode
from nautilus_trader.model import InstrumentId, BarType
from nautilus_trader.model.instruments import Instrument

from strategy import SuperAlphaStrategy, SuperAlphaStrategyConfig


def main():
    instrument_id = InstrumentId.from_str("AMD.NASDAQ")

    instrument_provider = InteractiveBrokersInstrumentProviderConfig(
        symbology_method=SymbologyMethod.IB_SIMPLIFIED,
        load_ids=frozenset([instrument_id])
    )

    config_node = TradingNodeConfig(
        trader_id="TESTER-001",
        logging=LoggingConfig(log_level="INFO"),
        data_clients={
            IB: InteractiveBrokersDataClientConfig(
                ibg_host="127.0.0.1",
                ibg_port=7497,
                ibg_client_id=1,
                handle_revised_bars=False,
                use_regular_trading_hours=True,
                instrument_provider=instrument_provider,
            ),
        },
        exec_clients={
            IB: InteractiveBrokersExecClientConfig(
                ibg_host="127.0.0.1",
                ibg_port=7497,
                ibg_client_id=1,
                account_id="DU1234567",  # This must match with the IB Gateway/TWS node is connecting to
                instrument_provider=instrument_provider,
                routing=RoutingConfig(
                    default=True,
                ),
            ),
        },
        data_engine=LiveDataEngineConfig(
            time_bars_timestamp_on_close=False,  # Will use opening time as `ts_event` (same like IB)
            validate_data_sequence=True,  # Will make sure DataEngine discards any Bars received out of sequence
        ),
        timeout_connection=90.0,
        timeout_reconciliation=5.0,
        timeout_portfolio=5.0,
        timeout_disconnection=5.0,
        timeout_post_stop=2.0,
    )

    node = TradingNode(config=config_node)

    strategy_config = SuperAlphaStrategyConfig(
        bar_type=BarType.from_str("AMD.NASDAQ-30-SECOND-LAST-EXTERNAL"),
        instrument_id=instrument_id
    )

    strategy = SuperAlphaStrategy(strategy_config)
    node.trader.add_strategy(strategy)

    node.add_data_client_factory(IB, InteractiveBrokersLiveDataClientFactory)
    node.add_exec_client_factory(IB, InteractiveBrokersLiveExecClientFactory)
    node.build()
    node.portfolio.set_specific_venue(IB_VENUE)

    try:
        node.run()
    finally:
        node.dispose()


if __name__ == "__main__":
    # Load API_KEY for EODHD API from .env file
    # load_dotenv('../.env')

    main()
