# Security Boundaries

## Application Objective
This application is designed purely as an analytical assistant. 
**No autonomous external attacks, exploitation or probing should be done.**
All targets are isolated in mock environment labs or are just PCAP traces.

## Principles
1. **Never use `NEXT_PUBLIC` for API keys** – Keys for CTI (OTX, etc.) live strictly on backend via `.env` file.
2. **Evidence Immutability** – Never modify original files or logs. Cryptographic checksums (SHA256, MD5) are taken immediately.
3. **Safe Content Extraction** – Do not execute packet payloads, perform automated reverse shell tests, or simulate payloads.
4. **Safe UI** – Do not render raw HTML from untrusted event logs. Sanitize display elements in dashboard.
5. **Rate Limiting** – Hardened against denial-of-service through endpoints in later phases.
