---
title: Client request behavior
type: synthesis
---

# Client request behavior

<a id="claim-client-request-behavior"></a>
### Claim: client-request-behavior

- **Kind:** derived
- **State:** stale
- **Statement:** Client requests should fail after 30 seconds.
- **Former evidence:**
  - **Source:** [Client Policy](../../sources/policy.md)
  - **Digest:** sha256:1e5a4a8b80c727eec7905a96f8a122914d14fffb4f3b3dd1e11845eb700b5d9e
  - **Locator:** heading "Timeout", lines 3-5
- **Derived from:** [client-timeout-30-seconds](../topics/client-policy.md#claim-client-timeout-30-seconds)
