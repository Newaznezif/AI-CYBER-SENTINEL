# Database Design

## Tables
1. **Investigation**
   - id, investigation_number, title, description, status, severity, confidence, open and close timestamps.
2. **Indicator**
   - id, investigation_id, type, value, normalized_value, source, confidence.
3. **Evidence**
   - id, investigation_id, type, filename, sha256, size, source.
4. **Observation**
   - Represents a fact extracted from evidence.
5. **Network Event**
   - Store normalized network activity (source_ip, destination_ip, ports, protocol).
6. **Threat Intelligence**
   - CTI provider responses. Store raw response and processed categories.
7. **IDS Alert**
   - Suricata/Zeek alert signatures.
8. **Attack Technique**
   - MITRE mappings and confidence.
9. **Risk Assessment**
   - Scores mapped deterministically.
10. **Recommendation**
    - Action item mapped.
11. **Timeline Event**
    - Event for chronological display.
