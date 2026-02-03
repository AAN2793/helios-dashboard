"""Simple trading journal utility.
Tracks entry/exit prices, position size, P/L, win/loss counts.
"""
from dataclasses import dataclass, asdict
from typing import Iterable, List


@dataclass
class Trade:
    symbol: str
    entry_price: float
    exit_price: float
    position_size: float  # positive for long, negative for short

    @property
    def pnl(self) -> float:
        """Profit/loss in dollars."""
        return (self.exit_price - self.entry_price) * self.position_size

    @property
    def is_win(self) -> bool:
        return self.pnl >= 0


class TradingJournal:
    def __init__(self) -> None:
        self.trades: List[Trade] = []

    def add_trade(self, trade: Trade) -> None:
        self.trades.append(trade)

    def extend(self, trades: Iterable[Trade]) -> None:
        self.trades.extend(trades)

    @property
    def total_pnl(self) -> float:
        return sum(trade.pnl for trade in self.trades)

    @property
    def win_count(self) -> int:
        return sum(1 for trade in self.trades if trade.is_win)

    @property
    def loss_count(self) -> int:
        return sum(1 for trade in self.trades if not trade.is_win)

    @property
    def win_rate(self) -> float | None:
        total = len(self.trades)
        return (self.win_count / total) * 100 if total else None

    def summary(self) -> dict:
        return {
            "total_trades": len(self.trades),
            "total_pnl": self.total_pnl,
            "win_count": self.win_count,
            "loss_count": self.loss_count,
            "win_rate": self.win_rate,
        }

    def to_dicts(self) -> List[dict]:
        return [asdict(trade) | {"pnl": trade.pnl, "is_win": trade.is_win} for trade in self.trades]


if __name__ == "__main__":
    journal = TradingJournal()
    journal.add_trade(Trade(symbol="AAPL", entry_price=150.0, exit_price=158.0, position_size=10))
    journal.add_trade(Trade(symbol="TSLA", entry_price=215.0, exit_price=205.0, position_size=5))
    for line in journal.to_dicts():
        print(line)
    print(journal.summary())
