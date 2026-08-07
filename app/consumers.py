"""Kafka consumers for device-alerts-service.

One handler per subscribed topic. Handlers are best-effort logging plus
audit — services override this file to implement real cross-domain behavior.
"""
from __future__ import annotations

import logging

from healthcare_common.audit import emit_audit

log = logging.getLogger("device-alerts-service.consumers")


def register(svc) -> None:
    bus = svc.bus

    @bus.on("device.reading")
    def _on_device_reading(envelope: dict) -> None:
        log.info("device-alerts-service: received device.reading id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.device.reading", actor="system:device-alerts-service",
                   target=None, details={"envelope_id": envelope.get("id")})

