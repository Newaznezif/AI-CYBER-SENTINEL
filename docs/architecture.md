# Core Architecture Principle

Never build this:
`IP → AI → MALICIOUS`

Build this:
```text
                       RAW EVIDENCE
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
           PCAP            LOGS        INDICATORS
             │              │              │
             ▼              ▼              ▼
         ANALYSIS       NORMALIZATION    VALIDATION
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    EVIDENCE STORE
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
          NETWORK ANALYSIS       CTI ENRICHMENT
                 │                     │
                 └──────────┬──────────┘
                            ▼
                     CORRELATION ENGINE
                            │
                            ▼
                     AI ANALYSIS ENGINE
                            │
                            ▼
                  MITRE ATT&CK VALIDATION
                            │
                            ▼
                     RISK ENGINE
                            │
                            ▼
                    HUMAN VALIDATION
                            │
                  ┌─────────┴─────────┐
                  ▼                   ▼
             RESPONSE             REPORT
```

## Layers:
- **API**: Handles HTTP endpoints.
- **Service**: Business logic.
- **Repository**: Database abstraction layers.
- **Workers**: Asynchronous processors for big PCAP payloads.
