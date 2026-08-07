# device-alerts-service

device-alerts-service — domain: devices

- **Port:** 8902
- **Language:** Python 3.11 + Flask
- **Database:** `devices` (Postgres, table `device_alerts`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/device_alerts/`          |
| POST      | `/api/device_alerts/`          |
| GET       | `/api/device_alerts/<id>`      |
| PUT/PATCH | `/api/device_alerts/<id>`      |
| DELETE    | `/api/device_alerts/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** device.alert.triggered
**Subscribes:** device.reading

## HTTP peer dependencies

- `device-registry-service`
- `notifications-service`
- `care-teams-service`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
