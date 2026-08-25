# Architecture v2

Published: 2026-03-15

## Approved decision

Public client integrations continue to use HTTP with JSON payloads. Internal
high-throughput services may use gRPC when both endpoints are controlled by the
team.

This decision supersedes the Protocol Review recommendation to make gRPC the
default for every new integration.
