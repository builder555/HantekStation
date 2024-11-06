## Hantek Station - Bench Power Supply Control

![screenshot](screenshot.png)

## Usage

### Prerequisites

- docker
- docker-compose

### Run

1. Connect your Hantek PSU to your computer (or Raspberry Pi). See [here](https://github.com/builder555/hantek-controller) for options to connect.
1. Download [compose.yml](compose.yml)
1. Run `docker compose up -d` in the same directory
1. Navigate to http://localhost:8000 (or `http://<ip address>:8000` if connecting remotely)

## Development

### Run

If you DO NOT have the psu connected, replace `devices` section from compose.dev.yml with 

```yaml
    environment:
      - NO_DEVICE=1
```

```bash
docker compose -f compose.dev.yml up -d --build
```

UI will run on http://localhost:5173 
API runs on http://localhost:8000
