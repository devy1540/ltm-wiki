# Architecture v1

Published: 2026-01-10

## Public transport

Public client integrations use HTTP with JSON payloads. This keeps the integration
surface compatible with existing clients and debugging tools.

## Internal experimentation

Internal services may experiment with gRPC, but this document does not approve it
as the default transport.
