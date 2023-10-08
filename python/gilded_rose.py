# -*- coding: utf-8 -*-
import abc
import enum


class AbsStrategy(object, metaclass=abc.ABCMeta):
    MIN_QUALITY = 0
    MAX_QUALITY = 50

    def __init__(self, item: 'Item'):
        self.__item = item

    @abc.abstractmethod
    def get_daily_sell_in_change(self) -> int:
        """"""

    @abc.abstractmethod
    def get_daily_quality_change_before_end_date(self, days_till_end_date: int) -> int:
        """"""

    @abc.abstractmethod
    def get_daily_quality_change_after_end_date(self, current_quality: int) -> int:
        """"""

    def update_item(self):
        self.__update_quality()
        self.__update_sell_in()

    def __update_sell_in(self):
        self.__item.sell_in += self.get_daily_sell_in_change()

    def __update_quality(self):
        if self.__item.sell_in <= 0:
            change = self.get_daily_quality_change_after_end_date(self.__item.quality)
        else:
            change = self.get_daily_quality_change_before_end_date(self.__item.sell_in)

        if change == 0:
            return

        if change > 0:
            self.__item.quality = min(self.__item.quality + change, self.MAX_QUALITY)
        else:
            self.__item.quality = max(self.__item.quality + change, self.MIN_QUALITY)


class NoChangeStrategy(AbsStrategy):
    def get_daily_sell_in_change(self) -> int:
        return 0

    def get_daily_quality_change_before_end_date(self, days_till_end_date: int) -> int:
        return 0

    def get_daily_quality_change_after_end_date(self, current_quality: int) -> int:
        return 0


class NormalSellInChangeStrategy(AbsStrategy, metaclass=abc.ABCMeta):
    def get_daily_sell_in_change(self) -> int:
        return -1


class CommonStrategy(NormalSellInChangeStrategy):
    def get_daily_quality_change_before_end_date(self, days_till_end_date: int) -> int:
        return -1

    def get_daily_quality_change_after_end_date(self, current_quality: int) -> int:
        return -2


class CheeseStrategy(NormalSellInChangeStrategy):
    def get_daily_quality_change_before_end_date(self, days_till_end_date: int) -> int:
        return 1

    def get_daily_quality_change_after_end_date(self, current_quality: int) -> int:
        return 2


class TicketsStrategy(NormalSellInChangeStrategy):
    def get_daily_quality_change_before_end_date(self, days_till_end_date: int) -> int:
        if days_till_end_date <= 5:
            return 3
        if days_till_end_date <= 10:
            return 2
        return 1

    def get_daily_quality_change_after_end_date(self, current_quality: int) -> int:
        return -current_quality


class ConjuredStrategy(NormalSellInChangeStrategy):
    def get_daily_quality_change_before_end_date(self, days_till_end_date: int) -> int:
        return -2

    def get_daily_quality_change_after_end_date(self, current_quality: int) -> int:
        return -2


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    @classmethod
    def get_strategy(cls, item: 'Item') -> AbsStrategy:
        match item.name:
            case "Sulfuras, Hand of Ragnaros":
                return NoChangeStrategy(item)
            case "Aged Brie":
                return CheeseStrategy(item)
            case "Backstage passes to a TAFKAL80ETC concert":
                return TicketsStrategy(item)
            case "Conjured Mana Cake":
                return ConjuredStrategy(item)
            case _:
                return CommonStrategy(item)

    def update_quality(self):
        for item in self.items:
            strategy = self.get_strategy(item)
            strategy.update_item()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
