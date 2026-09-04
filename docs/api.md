# API Specification

## Investigations
`POST   /api/v1/investigations`
`GET    /api/v1/investigations`
`GET    /api/v1/investigations/{id}`
`PATCH  /api/v1/investigations/{id}`
`DELETE /api/v1/investigations/{id}`

## Indicators
`POST /api/v1/indicators`
`GET  /api/v1/indicators`
`GET  /api/v1/indicators/{id}`

## Evidence
`POST /api/v1/evidence/upload`
`GET  /api/v1/evidence/{id}`

## PCAP Analysis
`POST /api/v1/pcap/analyze`
`GET  /api/v1/pcap/{id}`

## CTI Processing
`POST /api/v1/cti/enrich/{indicator_id}`
`GET  /api/v1/cti/{indicator_id}`

## AI Investigation
`POST /api/v1/analysis/{investigation_id}`
`GET  /api/v1/analysis/{investigation_id}`

## ATT&CK Generation 
`GET /api/v1/attack/{investigation_id}`

## Risk Score
`GET /api/v1/risk/{investigation_id}`

## Timeline Output
`GET /api/v1/timeline/{investigation_id}`

## Report Operations
`POST /api/v1/reports/{investigation_id}`
`GET  /api/v1/reports/{investigation_id}`
