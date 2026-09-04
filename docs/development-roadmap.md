# Developer Roadmap

## PHASE 0 - ARCHITECTURE AND PROJECT INITIALIZATION

Architecture and repository setup. Basic initialized configurations.

## PHASE 1 - BACKEND FOUNDATION

FastAPI APIs, DB integrations structure, services boilerplate.

## PHASE 2 - POSTGRESQL DATABASE

Schema initialization. Models construction. Alembic.

## PHASE 3 - INVESTIGATION MANAGEMENT

CRUD for investigations.

## PHASE 4 - INDICATOR MANAGEMENT

Support for IPv4, IPv6, URLs, domains, hashes, IPs.

## PHASE 5 - EVIDENCE MANAGEMENT

Store/Retrieve logical references to PCAPs, logs. Maintain strict non-modification checks.

## PHASE 6 - PCAP ANALYSIS WITH SCAPY

Raw parser for PCAP. Create models out of captures.

## PHASE 7 - ZEEK INTEGRATION

Read conn.log, etc. via zeek processing of offline captures.

## PHASE 8 - SURICATA INTEGRATION

Read eve.json for alert, flow, DNS, HTTP, TLS.

## PHASE 9 - CTI ABSTRACTION

Providers and managers base implementations.

## PHASE 10 - PHASE 12 CTI INTEGRATIONS

OTX, AbuseIPDB, VirusTotal

## PHASE 13 - CORRELATION ENGINE

Unify attributes and observations into logical trees.

## PHASE 14 - MITRE ATT&CK VALIDATION

## PHASE 15 - OLLAMA AI ENGINE

LLM integration and structured prompt pipelines.

## PHASE 16 - DETERMINISTIC RISK ENGINE

Deterministic score evaluator based on weights setup.

## PHASE 17 - TIMELINE ENGINE

Create temporal event layouts.

## PHASE 18 - DETECTION ENGINE

Rule-based correlation matches.

## PHASE 19 - THREAT HUNTING

Search endpoints across indicators and alerts.

## PHASE 20 - PHASE 23 FRONTEND

Dashboard, UI components, Investigations views, PCAP, ATT&CK integrations visually.

## PHASE 24 - REPORT GENERATION

Reporting views and export.

## PHASE 25 - CONTROLLED DEMONSTRATION LAB

Closed environment generation.

## PHASE 26 - END-TO-END INTEGRATION

Final workflows integration tests.

## PHASE 27 - PHASE 30 WRAP UP

Sec Hardening, Optimization, Documentation, Final Review.
