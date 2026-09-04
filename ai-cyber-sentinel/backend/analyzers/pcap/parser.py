import hashlib
from datetime import datetime
from scapy.all import PcapReader, IP, IPv6, TCP, UDP, DNSQR
from scapy.layers.http import HTTPRequest, HTTPResponse
from typing import List, Dict, Any, Tuple

def analyze_pcap_file(filepath: str, investigation_id: int) -> Dict[str, Any]:
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    size = 0
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)
            size += len(chunk)
            
    summary = {
        "md5": md5_hash.hexdigest(),
        "sha256": sha256_hash.hexdigest(),
        "size": size,
        "packet_count": 0,
        "duration": 0.0,
        "first_timestamp": None,
        "last_timestamp": None
    }
    
    network_events = []
    
    # Process packets using memory-efficient PcapReader
    with PcapReader(filepath) as pcap_reader:
        for packet in pcap_reader:
            summary["packet_count"] += 1
            
            ts = float(packet.time)
            
            if summary["first_timestamp"] is None or ts < summary["first_timestamp"]:
                summary["first_timestamp"] = ts
            if summary["last_timestamp"] is None or ts > summary["last_timestamp"]:
                summary["last_timestamp"] = ts
                
            event = {
                "investigation_id": investigation_id,
                "timestamp": datetime.fromtimestamp(ts),
                "bytes": len(packet),
                "protocol": None,
                "source_ip": None,
                "destination_ip": None,
                "source_port": None,
                "destination_port": None,
                "dns_name": None,
                "http_method": None,
                "http_host": None,
                "http_uri": None,
                "user_agent": None,
                "status_code": None
            }
            
            if IP in packet:
                event["source_ip"] = packet[IP].src
                event["destination_ip"] = packet[IP].dst
            elif IPv6 in packet:
                event["source_ip"] = packet[IPv6].src
                event["destination_ip"] = packet[IPv6].dst
                
            if TCP in packet:
                event["protocol"] = "TCP"
                event["source_port"] = packet[TCP].sport
                event["destination_port"] = packet[TCP].dport
                
                # Basic TLS SNI inspection placeholder (advanced extraction omitted for simple Scapy)
                if packet[TCP].dport == 443 or packet[TCP].sport == 443:
                    event["protocol"] = "TLS"
                    
            elif UDP in packet:
                event["protocol"] = "UDP"
                event["source_port"] = packet[UDP].sport
                event["destination_port"] = packet[UDP].dport
                
            if packet.haslayer(DNSQR):
                qname = packet[DNSQR].qname
                if qname:
                    event["dns_name"] = qname.decode(errors='ignore').strip('.')
                    
            if packet.haslayer(HTTPRequest):
                http_layer = packet[HTTPRequest]
                event["http_method"] = http_layer.Method.decode(errors='ignore') if http_layer.Method else None
                event["http_host"] = http_layer.Host.decode(errors='ignore') if http_layer.Host else None
                event["http_uri"] = http_layer.Path.decode(errors='ignore') if http_layer.Path else None
                event["user_agent"] = http_layer.User_Agent.decode(errors='ignore') if hasattr(http_layer, 'User_Agent') and http_layer.User_Agent else None
                
            if packet.haslayer(HTTPResponse):
                http_layer = packet[HTTPResponse]
                # Extracting Status-Code safely
                if hasattr(http_layer, 'Status_Code') and http_layer.Status_Code:
                    try:
                        event["status_code"] = int(http_layer.Status_Code.decode(errors='ignore'))
                    except:
                        pass
                        
            # Only append useful network events, otherwise it gets too large
            if event["source_ip"] and event["destination_ip"] and event["protocol"]:
                # Simple aggregation for demonstration (normally, you'd track flows)
                network_events.append(event)
                
    if summary["first_timestamp"] and summary["last_timestamp"]:
        summary["duration"] = summary["last_timestamp"] - summary["first_timestamp"]

    return {
        "summary": summary,
        "events": network_events
    }
