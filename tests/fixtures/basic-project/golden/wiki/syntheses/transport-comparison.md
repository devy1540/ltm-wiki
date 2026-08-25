---
title: Supported Transport Comparison
type: synthesis
---

# Supported Transport Comparison

<a id="claim-transport-approved-client-internal-policy"></a>
### Claim: transport-approved-client-internal-policy

- **Kind:** derived
- **State:** current
- **Statement:** Public clients should use HTTP with JSON for compatibility with existing clients and debugging tools; controlled internal high-throughput services may use gRPC.
- **Derived from:** [transport-public-http](../topics/transport.md#claim-transport-public-http) and [transport-internal-grpc](../topics/transport.md#claim-transport-internal-grpc)
- **Evidence chain:**
  - [Architecture v1](../../sources/architecture-v1.md), heading "Public transport", lines 5-8
  - [Architecture v2](../../sources/architecture-v2.md), heading "Approved decision", lines 5-9

## Historical limitation

The earlier recommendation to make gRPC the default for every new public and
internal integration is [superseded](../topics/transport.md#claim-transport-all-new-grpc)
by the approved v2 decision; it is retained as historical context, not as the
current policy.
