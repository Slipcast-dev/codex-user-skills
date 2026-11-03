# Search, training and optional agent discovery

Documentation checked: 2026-10-10. Recheck official sources before changing crawler controls or making provider-specific claims.

- Google Search: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide — Search does not use llms.txt for ranking or visibility in its generative features. Follow current indexing and Search guidance.
- OpenAI: https://developers.openai.com/api/docs/bots — OAI-SearchBot supports search; GPTBot controls potential training use. Settings are independent. Do not enable training access merely to pursue search visibility.
- Google crawler controls: https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers — Googlebot affects Search. Google-Extended is a separate policy token for future Gemini training and specified Gemini/Vertex grounding uses; it does not affect Google Search inclusion or ranking. Explain the grounding tradeoff before applying the user’s intended policy.
- Agentic browsing: https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt — llms.txt may help consumers that explicitly support this convention; this does not establish a ranking benefit in Google Search.

Record provider, purpose, documented crawler/control, desired policy, observed current configuration and source date separately. Confirm the user's intended search/training policy; do not infer one from the other. llms-full.txt is optional publication of content, not an access-control mechanism or an automatic license grant. Do not include private, gated or third-party content without the appropriate rights and authorization.

For visibility experiments fix query set, product, locale, date and account conditions. Repeat measurements and distinguish correlation from causation. Do not claim universal extraction/ranking behavior based on one answer.
