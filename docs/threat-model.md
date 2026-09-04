# Threat Model

The application parses untrusted evidence like PCAPs and event logs sourced from potentially malicious environments.

## Threat Assessment
1. **Malicious PCAP crafting** to exploit the network parser backend (Scapy/Zeek).
2. **LLM Prompt Injection**: An attacker might leave specific logs embedded heavily in headers. Our parser forces data into strict JSON structures prior to interacting with Ollama.
3. **Data Exfiltration**: CTI enrichment logic is isolated. Only requested IP addresses / Hash strings are submitted to OTX/AV engines. Raw payloads are NEVER submitted to prevent leakage.
4. **Denial of Service**: Giant PCAP payloads. Restricted by `MAX_UPLOAD_SIZE` validations at API Gateway.
