import datetime as dt

from nautilus_trader.common.enums import LogColor
from nautilus_trader.indicators.average.ma_factory import MovingAverageFactory, MovingAverageType
from nautilus_trader.indicators.macd import MovingAverageConvergenceDivergence
from nautilus_trader.indicators.stochastics import Stochastics
from nautilus_trader.model import BarType, Bar, InstrumentId, Quantity
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.trading import Strategy
from nautilus_trader.trading.config import StrategyConfig


class SuperAlphaStrategyConfig(StrategyConfig, frozen=True):
    bar_type: BarType
    instrument_id: InstrumentId


class SuperAlphaStrategy(Strategy):
    def __init__(self, config: SuperAlphaStrategyConfig):
        super().__init__(config=config)
        self.bars_processed = 0
        self.in_position = True

        self.ema_9 = MovingAverageFactory.create(9, MovingAverageType.EXPONENTIAL)

        self.macd_8_17_9 = MovingAverageConvergenceDivergence(8, 17, MovingAverageType.EXPONENTIAL)
        self.macd_signal_8_17_9 = MovingAverageFactory.create(9, MovingAverageType.EXPONENTIAL)

        self.stoch_14_5 = Stochastics(14, 5)

        self.start_time = None
        self.end_time = None

    def on_start(self):
        self.start_time = dt.datetime.now()
        self.log.info(f"Strategy started at: {self.start_time}")

        self.subscribe_bars(self.config.bar_type)
        self.register_indicator_for_bars(self.config.bar_type, self.ema_9)
        self.register_indicator_for_bars(self.config.bar_type, self.macd_8_17_9)
        self.register_indicator_for_bars(self.config.bar_type, self.stoch_14_5)

    def on_bar(self, bar: Bar):
        self.log.info(f"Processing bar: {bar}")

        self.bars_processed += 1

        if self.macd_8_17_9.initialized:
            self.macd_signal_8_17_9.update_raw(self.macd_8_17_9.value)

        if not (self.ema_9.initialized and self.macd_8_17_9.initialized and self.stoch_14_5.initialized):
            self.log.info("Waiting for indicators to initialize...")
            return

        ema_9_val = self.ema_9.value
        macd_8_17_9_val = self.macd_8_17_9.value
        macd_signal_8_17_9_val = self.macd_signal_8_17_9.value
        stoch_14_5_val_k = self.stoch_14_5.value_k
        stoch_14_5_val_d = self.stoch_14_5.value_d

        # Start trading if at least 1 minute has passed since the strategy started
        if (dt.datetime.now() - self.start_time).total_seconds() < 60:
            return

        self.log.info(
            f"Checking momentum conditions - Price: {bar.close}, "
            f"MACD vs Signal: {macd_8_17_9_val:.6f} vs {macd_signal_8_17_9_val:.6f}, "
            f"Close vs EMA9: {bar.close} vs {ema_9_val:.6f}, "
            f"Stoch K vs D: {stoch_14_5_val_k:.2f} vs {stoch_14_5_val_d:.2f}")

        if (not self.in_position
                and macd_8_17_9_val > macd_signal_8_17_9_val
                and bar.close > ema_9_val
                and stoch_14_5_val_k > stoch_14_5_val_d):

            self.log.info(f"Market Buy order: {bar}", color=LogColor.YELLOW)

            self.submit_order(
                self.order_factory.market(
                    instrument_id=self.config.instrument_id,
                    order_side=OrderSide.BUY,
                    time_in_force=TimeInForce.GTC,
                    quantity=Quantity.from_int(1)
                )
            )

            self.in_position = True

        elif (self.in_position
              and macd_8_17_9_val < macd_signal_8_17_9_val
              and bar.close < ema_9_val
              and stoch_14_5_val_k < stoch_14_5_val_d):

            self.log.info(f"Market Sell order: {bar}", color=LogColor.YELLOW)

            self.submit_order(
                self.order_factory.market(
                    instrument_id=self.config.instrument_id,
                    order_side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC,
                    quantity=Quantity.from_int(1)
                )
            )

            self.in_position = False


def on_stop(self):
    self.end_time = dt.datetime.now()
    self.log.info(
        f"Strategy finished at: {self.end_time} | "
        f"Duration: {(self.end_time - self.start_time).total_seconds():.2f} seconds.",
    )

    self.log.info(f"Strategy stopped. Processed {self.bars_processed} bars.")
