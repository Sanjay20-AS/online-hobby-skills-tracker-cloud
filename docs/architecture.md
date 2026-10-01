# Architecture

## Logical architecture

Browser -> React -> HTTPS REST -> FastAPI -> PostgreSQL/Object Storage.

## Cloud architecture

- Static frontend hosting
- Managed PostgreSQL
- Stateless FastAPI instances
- S3-compatible object storage
- GitHub Actions CI

## Scalability

The API does not keep application state in process memory. A load balancer can distribute requests across multiple backend instances while PostgreSQL and object storage remain shared persistent services.
