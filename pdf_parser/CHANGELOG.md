# Changelog

## 1.0.2

- Added logging to the `logs` worksheet for each processed PDF, including status and error details.
- Added optional MQTT heartbeat publishing so Home Assistant can detect `online` and `offline` addon state.
- Added MQTT configuration options for broker host, port, topic, username, and password.
- Fixed Docker build fallback by providing a default `BUILD_FROM` base image in the add-on `Dockerfile`.
