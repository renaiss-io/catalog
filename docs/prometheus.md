
# Hosting Prometheus Locally with Docker and Exposing it as a Data Source using ngrok

This guide outlines the process of setting up a local Prometheus instance using Docker, making it accessible online, and subsequently integrating it as a data source for PQL queries.

## Prerequisites
- Docker Compose installed on your local machine. You can find installation instructions [here](https://docs.docker.com/compose/install/).
- An ngrok account. If you don't have one, sign up at [ngrok.com](ngrok.com.)

## Tutorial

### 1. Create Prometheus Configuration 
Start by creating a Prometheus configuration file at `/tmp/prometheus/prometheus.yml`. Below is a sample configuration that specifies the scrape interval and two targets, Prometheus itself, and the node exporter.

```
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["prometheus:9090"]
  - job_name: node_exporter
    static_configs:
      - targets: ["node-exporter:9100"]
```

### 2. Configure ngrok

Create a ngrok.yml configuration file at `/tmp/prometheus/ngrok.yml`. Insert your ngrok authentication token.

```
version: "2"
authtoken: "YOUR_AUTHENTICATION_TOKEN"

tunnels:
  demo:
    proto: http
    addr: prometheus:9090
```
### 3. Docker compose configuration setup

Compose a `docker-compose.yml` file that defines three services: Prometheus, node-exporter, and ngrok.

```
version: '3'
services:
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    ports:
      - 9090:9090
    volumes:
      - /tmp/prometheus:/etc/prometheus
    command:
      - --config.file=/etc/prometheus/prometheus.yml
    
  node-exporter:
    image: prom/node-exporter
    container_name: node-exporter

  ngrok:
      image: ngrok/ngrok:latest
      restart: unless-stopped
      command:
        - "start"
        - "--all"
        - "--config"
        - "/etc/ngrok.yml"
      volumes:
        - /tmp/ngrok/ngrok.yml:/etc/ngrok.yml
      ports:
        - 4040:4040
```

#### 4. Launch Docker Services
Execute the Docker Compose command to initiate the services.

```docker compose up -d ```

You can check the status of the three services running.

```docker compose ps``` 

You can access to the promtheus dashboard from your browser  http://localhost:9090

### 5. Setup as Prometheus as PQL datasource  


Begin by configuring the `env.json` file to establish the connection. To identify the running agents linked to your ngrok account, navigate to the [ngrok dashboard](https://dashboard.ngrok.com/tunnels/agent). In the dashboard, you'll find a panel resembling the one below:

<img src="../images/ngrok-agent.svg" alt="alt text" width="400" />

The highlighted DNS name within the red box is the key detail you'll need to set up in the `env.json` file. Open the `env.json` file and insert the following configuration block:

```
    {
      "name": "prometheus",
      "type": "Prometheus",
      "vars": {
        "prom_address": "<ngrok_url>",
        "window": "300s"
      }
    }
```

Replace <ngrok_url> with the DNS name you identified in the ngrok dashboard.

By following these steps, you will have successfully hosted Prometheus locally using Docker, exposed it via ngrok, and set it up as a data source for PQL queries. 