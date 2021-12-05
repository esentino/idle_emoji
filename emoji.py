from dataclasses import dataclass, field
from datetime import datetime, timedelta

from constants import SECOND_IN_MICROSECONDS


@dataclass
class Emoji:
    name: str
    image: str
    start_price: float
    start_income: float
    growth: float
    speed: float
    level: int = field(default=0)
    last_tick: datetime = field(default_factory=lambda: datetime.now())

    @property
    def buy_price(self) -> float:
        return self.start_price * (self.growth ** self.level)

    @property
    def production(self) -> float:
        return self.production_per_second * self.speed

    @property
    def production_per_second(self) -> float:
        return self.start_income * self.level

    @property
    def production_per_second_after_upgrade(self) -> float:
        return self.production_per_second + self.start_income

    def recalculate(self) -> float:
        current_time = datetime.now()
        delta: timedelta = current_time - self.last_tick
        tick_time_in_microseconds = timedelta(microseconds=self.speed * SECOND_IN_MICROSECONDS)
        ticks, _ = delta.__divmod__(tick_time_in_microseconds)
        self.last_tick = self.last_tick + ticks * tick_time_in_microseconds
        return self.production * ticks

    def buy(self, cash: float) -> float:
        left_cash = cash - self.buy_price
        self.level += 1
        return left_cash
