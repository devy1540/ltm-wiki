---
title: Transport
type: topic
---

# Transport

This topic exists before source ingestion and must be reconciled rather than
replaced by a new duplicate page.

<a id="claim-transport-public-http"></a>
### Claim: transport-public-http

- **Kind:** sourced
- **State:** current
- **Statement:** Public client integrations use HTTP with JSON payloads.
- **Evidence:**
  - **Source:** [Architecture v1](../../sources/architecture-v1.md)
  - **Locator:** heading "Public transport", lines 5-8
  - **Source:** [Architecture v2](../../sources/architecture-v2.md)
  - **Locator:** heading "Approved decision", lines 5-9
- **Contradicts:** [transport-all-new-grpc](#claim-transport-all-new-grpc)
- **Supersedes:** [transport-all-new-grpc](#claim-transport-all-new-grpc)

<a id="claim-transport-all-new-grpc"></a>
### Claim: transport-all-new-grpc

- **Kind:** sourced
- **State:** superseded
- **Statement:** gRPC should be the default transport for every new public and internal integration.
- **Evidence:**
  - **Source:** [Protocol Review](../../sources/protocol-review.md)
  - **Locator:** heading "Recommendation", lines 5-9
- **Contradicts:** [transport-public-http](#claim-transport-public-http)
- **Superseded by:** [transport-public-http](#claim-transport-public-http) and [transport-internal-grpc](#claim-transport-internal-grpc), the approved Architecture v2 decision.

<a id="claim-transport-internal-grpc"></a>
### Claim: transport-internal-grpc

- **Kind:** sourced
- **State:** current
- **Statement:** Controlled internal high-throughput services may use gRPC.
- **Evidence:**
  - **Source:** [Architecture v2](../../sources/architecture-v2.md)
  - **Locator:** heading "Approved decision", lines 5-9
- **Supersedes:** [transport-all-new-grpc](#claim-transport-all-new-grpc)

<a id="claim-transport-rollout-owner"></a>
### Claim: transport-rollout-owner

- **Kind:** sourced
- **State:** current
- **Statement:** The platform team owns the transport migration checklist.
- **Evidence:**
  - **Source:** [Operational Notes](../../sources/operational-notes.md)
  - **Locator:** heading "Rollout ownership", lines 5-8

<a id="claim-transport-public-http"></a>
### Claim: transport-public-http

- **Kind:** sourced
- **State:** current
- **Statement:** This duplicate claim ID is intentionally invalid.
- **Evidence:**
  - **Source:** [Architecture v1](../../sources/architecture-v1.md)
  - **Locator:** heading "Public transport", lines 5-8
