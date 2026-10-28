---
Title: "OpenAI selected for the sourcing layer"
Reference: "Owner reply and official OpenAI documentation checked 2026-10-27"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# OpenAI Provider Selection

The owner's answer to the sourcing-provider question is: **Use OpenAI**.

This selects the provider, not a model, budget or credential. No key was supplied and no API request was made.

## Documentation And Design Implications

[Official web-search guidance](https://developers.openai.com/api/docs/guides/tools-web-search) documents Responses API hosted `web_search`, domain allowlists and returned consulted-source URLs. Use that route for supplemental discovery, deriving approved domains from the source registry. Recheck retrieved candidates against the registry; search output does not establish medical evidence eligibility. Preserve source lists and citation annotations for audit. Actual account/model availability and budget enforcement remain implementation checks.

[Official function-calling guidance](https://developers.openai.com/api/docs/guides/function-calling) documents strict function schemas. Use strict schemas plus local argument validation for biomedical connectors; the server still executes those functions and applies policy.

Proposed configuration: provider `openai`, credential `OPENAI_API_KEY` in backend environment, configurable model, and OpenAI-hosted search as the initial search path. A separate search vendor is not planned for this path. Direct biomedical connectors remain the primary evidence retrieval route. The plan changes only this provider choice; it does not claim a functioning integration.
