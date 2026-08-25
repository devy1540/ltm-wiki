---
title: Client Policy
type: topic
---

# Client Policy

<a id="claim-client-timeout-30-seconds"></a>
### Claim: client-timeout-30-seconds

- **Kind:** sourced
- **State:** stale
- **Statement:** Clients must use a 30-second request timeout.
- **Former evidence:**
  - **Source:** [Client Policy](../../sources/policy.md)
  - **Digest:** sha256:1e5a4a8b80c727eec7905a96f8a122914d14fffb4f3b3dd1e11845eb700b5d9e
  - **Locator:** heading "Timeout", lines 3-5
- **Reason:** The replacement at the same source path does not support a numeric request-timeout rule.

<a id="claim-client-reliability-guidance-ownership"></a>
### Claim: client-reliability-guidance-ownership

- **Kind:** sourced
- **State:** current
- **Statement:** The platform team owns client reliability guidance.
- **Evidence:**
  - **Source:** [Client Policy](../../sources/policy.md)
  - **Locator:** heading "Ownership", lines 3-8
