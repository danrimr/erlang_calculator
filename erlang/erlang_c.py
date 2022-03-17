"""Docs."""
from dataclasses import dataclass
from math import ceil, exp


@dataclass
class ErlangC:
    """Docstring for calc_erlang_c."""

    call_per_hour: float
    call_duration: float
    delay_time: float

    def __post_init__(self) -> None:
        """Docstring for __post_init__."""
        if self.call_per_hour <= 0:
            raise ValueError("Call per hour must be a positive number")
        if self.call_duration <= 0:
            raise ValueError("Call duration must be a positive number")
        if self.delay_time < 0:
            raise ValueError("Delay time must be a positive number")

    def calc_n_agents(self) -> int:
        """Docstring for calc_n_agents."""
        load_a = lambda x, y: round(x * y / 3600, 4)
        a_load_value = load_a(self.call_per_hour, self.call_duration)
        agents = ceil(a_load_value)
        _, service_level = self.calculate(agents, a_load_value)

        while service_level < 0.8:
            agents += 1
            _, service_level = self.calculate(agents, a_load_value)
        return agents, round(service_level, 4)

    def calculate(self, n_agents, a_load_value) -> list[float, float]:
        """Docstring for calculate."""
        aux1 = 0
        aux2 = 1

        for i in range(1, n_agents + 1):
            for j in range(0, i):
                aux2 *= (n_agents - j) / a_load_value
            aux1 += aux2
            aux2 = 1

        prob = 1 + aux1 * (n_agents - a_load_value) / n_agents
        prob = round(1 / prob, 4)
        service_level = 1 - prob * exp(
            (a_load_value - n_agents) * (self.delay_time / self.call_duration)
        )
        service_level = round(service_level, 4)

        return prob, service_level


if __name__ == "__main__":
    b = ErlangC(call_per_hour=15, call_duration=120, delay_time=30)
    print(b.calc_n_agents())
