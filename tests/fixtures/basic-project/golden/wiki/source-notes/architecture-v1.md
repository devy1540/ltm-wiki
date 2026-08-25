---
title: Architecture v1
type: source-note
source_path: sources/architecture-v1.md
source_digest: sha256:d87ad807d731ef256b34694477e0ada3d407370fb3aba49096b97aa3ebf18dd9
---

# Architecture v1

This source specifies HTTP with JSON for public client integrations and permits
only experimentation with gRPC by internal services; it does not approve gRPC as
a default.

## Important assertions

- Public client integrations use HTTP with JSON payloads ([Transport claim](../topics/transport.md#claim-transport-public-http)); heading "Public transport", lines 5-8.
