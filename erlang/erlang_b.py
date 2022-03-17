"""Docs"""
from dataclasses import dataclass
from math import ceil


@dataclass
class ErlangB:
    """Docstring for calc_erlang_b."""

    traffic: float
    block_prob: float
    channels: int

    def __post_init__(self) -> None:
        """Docstring for __post_init__."""
        if self.block_prob not in range(0, 1) and not isinstance(
            self.block_prob, float
        ):
            raise ValueError("Block probability must be in range [0, 1]")
        if not isinstance(self.channels, int) and self.channels <= 0:
            raise ValueError("Channels must be a positive integer")
        if self.traffic <= 0 and not isinstance(self.traffic, float):
            raise ValueError("Traffic must be a positive number")

    def get_block_prob(self) -> float:
        """Docstring for get_block_prob."""
        inv_block_prob = 1
        for i in range(1, self.channels + 1):
            inv_block_prob = 1 + i / self.traffic * inv_block_prob
        return round(1 / inv_block_prob, 4)

    def get_traffic(self) -> float:
        """Docstring for get_traffic."""
        _traffic = 0.05
        _block_prob = 0
        while _block_prob < self.block_prob:
            _block_prob = self.get_block_prob()
            _traffic += 0.05
        return round(_traffic - 0.05, 4)

    def get_n_channels(self) -> int:
        """Docstring for get_n_channels."""
        _channels = 0
        _block_prob = 1
        while _block_prob > self.block_prob:
            _channels += 1
            _block_prob = self.get_block_prob()
        return ceil(_channels)


if __name__ == "__main__":
    b = ErlangB(traffic=50, block_prob=0.2, channels=12)
    print(b.get_traffic())
