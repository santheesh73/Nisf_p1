import logging


class AuditService:
    def log_event(self, event: str, **payload) -> None:
        logging.getLogger("nisf.audit").info(event, extra=payload)
