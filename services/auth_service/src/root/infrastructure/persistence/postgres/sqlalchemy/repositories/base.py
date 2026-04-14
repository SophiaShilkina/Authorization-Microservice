from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError


class SqlAlchemyRepository:
    @staticmethod
    def _extract_constraint_name(exc: IntegrityError, candidates: Sequence[str]) -> str | None:
        driver_exc = getattr(exc, "driver_exception", None) or getattr(exc, "orig", None)
        if driver_exc is None:
            return None

        diag = getattr(driver_exc, "diag", None)
        if diag is not None:
            name = getattr(diag, "constraint_name", None)
            if name:
                return name

        name = getattr(driver_exc, "constraint_name", None)
        if name:
            return name

        text = str(driver_exc)
        for candidate in candidates:
            if candidate in text:
                return candidate

        return None
