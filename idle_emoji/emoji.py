from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .constants import SECOND_IN_MICROSECONDS


@dataclass
class Emoji:
    name: str
    image: str
    start_price: float
    start_income: float
    growth: float
    speed: float
    level: int = field(default=0)
    last_tick: datetime = field(default_factory=datetime.now)

    @property
    def buy_price(self) -> float:
        """

        >>> em = Emoji('abc','bcd',4,0,2,2,3)
        >>> em.buy_price
        32

        :return:
        """
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

    def recalculate(self, current_time: datetime) -> float:
        """
        Calculate income from last check and calculate next last check.
        For example:
        Last tick -> 00:00:00
        current time -> 00:00:10
        speed of emoji -> 3seconds
        Compute time elapsed 10s
        In 10s 3 times emoji generate income
        return 3 time income
        and move last tick to 3 times 3s -> 00:00:09

        >>> em = Emoji("a","a",1,1,1,3,1,datetime(2022,1,1,0,0,0,))
        >>> em.production
        3
        >>> em.recalculate(datetime(2022,1,1,0,0,10,))
        9

        :return: return income from elapsed time
        """
        delta: timedelta = current_time - self.last_tick
        tick_time_in_microseconds = timedelta(microseconds=self.speed * SECOND_IN_MICROSECONDS)
        ticks, _ = delta.__divmod__(tick_time_in_microseconds)
        self.last_tick = self.last_tick + ticks * tick_time_in_microseconds
        return self.production * ticks

    def buy(self, cash: float) -> float:
        """Lece bo chce

        >>> em = Emoji('aaa', 'aaaa',1,0,1,1,1)
        >>> em.buy(5)
        4
        >>> em.level
        2

        :param cash:
        :return:
        """
        left_cash = cash - self.buy_price
        self.level += 1
        return left_cash
