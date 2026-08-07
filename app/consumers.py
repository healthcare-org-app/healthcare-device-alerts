"""Kafka consumers for device-alerts-service.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("device-alerts-service.consumers")

TABLE = "device_alerts"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("device.reading")
    def _on_device_reading(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    # Trigger alert on out-of-range reading.
                    metric = data.get("metric"); value = data.get("value")
                    thresholds = {"heart_rate": (40, 150), "glucose": (60, 300), "spo2": (90, 101)}
                    rng = thresholds.get(metric)
                    if not rng or value is None: return
                    low, high = rng
                    if low <= float(value) <= high: return
                    alert = {"device_id": data.get("device_id"), "patient_id": data.get("patient_id"),
                             "metric": metric, "value": value, "severity": "high"}
                    row = db.query_one(f"INSERT INTO {TABLE} (data) VALUES (%s) RETURNING *", (Json(alert),))
                    bus.publish("device.alert.triggered", key=str(row["id"]), value={**alert, "alert_id": row["id"]})
        except Exception as e:
            log.exception("device-alerts-service/device.reading handler failed: %s", e)
        emit_audit(bus, action="consume.device.reading", actor="system:device-alerts-service",
                   target=None, details={"envelope_id": envelope.get("id")})

