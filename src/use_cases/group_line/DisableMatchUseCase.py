from DomainService import (
    match_service,
)


class DisableMatchUseCase:

    def execute(self) -> None:
        match_service.disable()
