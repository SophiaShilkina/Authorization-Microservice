from dataclasses import dataclass, field

from ..events import DomainEvent


@dataclass
class BaseDM(slots=True):
    _domain_events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    def _add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> list[DomainEvent]:
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events
