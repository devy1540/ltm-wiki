---
title: Architecture v2
type: source-note
source_path: sources/architecture-v2.md
source_digest: sha256:fbea0a54c9380276ae4b929d75667c228c86cdb34d26d3d28b1f088a1831a68c
---

# Architecture v2

This source approves continued HTTP with JSON for public clients and permits gRPC
for controlled internal high-throughput services. It explicitly supersedes the
Protocol Review's gRPC-default recommendation.

## Important assertions

- Public client integrations continue to use HTTP with JSON payloads ([Transport claim](../topics/transport.md#claim-transport-public-http)); heading "Approved decision", lines 5-9.
- Controlled internal high-throughput services may use gRPC ([Transport claim](../topics/transport.md#claim-transport-internal-grpc)); heading "Approved decision", lines 5-9.
- The gRPC-default recommendation is superseded ([Transport claim](../topics/transport.md#claim-transport-all-new-grpc)); heading "Approved decision", lines 11-12.
