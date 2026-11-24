---
name: universal-devops-sre
description: >-
  Site Reliability Engineering (SRE) and DevOps Architect expertise for production infrastructure:
  Docker multi-stage builds, Kubernetes (Deployments, Services, Ingress, HPA, PodDisruptionBudgets),
  GitHub Actions CI/CD pipelines, Terraform Infrastructure as Code (IaC), Prometheus/Grafana
  observability, OpenTelemetry distributed tracing, and zero-downtime rolling deployments.
  Use when creating Dockerfiles, configuring CI/CD pipelines, or setting up cloud infrastructure.
---

# Principal DevOps & Site Reliability Engineer Handbook

Build robust, automated, zero-downtime deployment pipelines and production-grade containerized infrastructure.

---

## 1. Production Docker Best Practices

1. **Multi-Stage Builds**:
   - Separate build dependencies from runtime artifacts to produce minimal, secure images.
   - Example (Node.js/Next.js or Go):
     ```dockerfile
     # Stage 1: Build
     FROM golang:1.22-alpine AS builder
     WORKDIR /app
     COPY go.mod go.sum ./
     RUN go mod download
     COPY . .
     RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /server .

     # Stage 2: Minimal Runtime
     FROM alpine:3.19
     RUN apk --no-cache add ca-certificates
     WORKDIR /app
     COPY --from=builder /server /app/server
     USER 10001:10001
     EXPOSE 8080
     CMD ["/app/server"]
     ```
2. **Non-Root Execution**:
   - NEVER run containers as `root` in production. Always specify `USER <uid>:<gid>`.
3. **Layer Caching**:
   - Copy dependency manifests (`package.json`, `requirements.txt`, `go.mod`) and install dependencies BEFORE copying application source code.

---

## 2. Kubernetes Resiliency Standards

1. **Health Probes**:
   - Every pod must declare `livenessProbe` (detects deadlock/hangs) and `readinessProbe` (gates traffic until service is ready).
2. **Resource Requests & Limits**:
   - Every container must declare explicit `requests.cpu`, `requests.memory`, `limits.cpu`, and `limits.memory` to prevent node OOM-killing.
3. **Graceful Shutdown**:
   - Application must trap `SIGTERM`, stop accepting new connections, drain existing requests (10-30s window), and exit cleanly.

---

## 3. CI/CD Pipeline Automation

- Run linting, type-checking, and unit tests on every PR.
- Pin GitHub Action versions to exact SHAs or releases (e.g. `actions/checkout@v4`).
- Use matrix builds for multi-platform or multi-version compatibility testing.
