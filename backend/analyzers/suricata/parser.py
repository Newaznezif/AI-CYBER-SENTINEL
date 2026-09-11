import subprocess
import os
import tempfile
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple

import shutil

def get_suricata_binary() -> str | None:
    if os.name == "nt":
        npcap_path = r"C:\Windows\System32\Npcap"
        suricata_dir = r"C:\Program Files\Suricata"
        current_path = os.environ.get("PATH", "")
        if npcap_path not in current_path and os.path.exists(npcap_path):
            os.environ["PATH"] = f"{npcap_path};{suricata_dir};{current_path}"

    cmd = shutil.which("suricata")
    if not cmd and os.name == "nt" and os.path.exists(r"C:\Program Files\Suricata\suricata.exe"):
        cmd = r"C:\Program Files\Suricata\suricata.exe"
    return cmd

def check_suricata_availability() -> bool:
    cmd = get_suricata_binary()
    if not cmd:
        return False
    try:
        res = subprocess.run([cmd, "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0
    except (FileNotFoundError, OSError):
        return False

def parse_eve_json(filepath: str, investigation_id: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    alerts = []
    events = []
    
    if not os.path.exists(filepath):
        return alerts, events
        
    with open(filepath, "r") as f:
        for line in f:
            try:
                record = json.loads(line.strip())
                event_type = record.get("event_type")
                
                # Base attributes
                src_ip = record.get("src_ip")
                dest_ip = record.get("dest_ip")
                proto = record.get("proto")
                ts_str = record.get("timestamp")
                ts = None
                if ts_str:
                    try:
                        # Suricata timestamps are ISO 8601
                        ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00')[:-6] + '+00:00')
                    except Exception:
                        ts = datetime.utcnow()
                else:
                    ts = datetime.utcnow()

                if event_type == "alert":
                    alert_data = record.get("alert", {})
                    severity_num = alert_data.get("severity", 3)
                    
                    sev_mapping = {1: "HIGH", 2: "MEDIUM", 3: "LOW", 4: "INFO"}
                    sev_str = sev_mapping.get(severity_num, "INFO")
                    
                    alerts.append({
                        "investigation_id": investigation_id,
                        "source": "SURICATA",
                        "signature": alert_data.get("signature", "Unknown Alert"),
                        "severity": sev_str,
                        "timestamp": ts,
                        "source_ip": src_ip,
                        "destination_ip": dest_ip,
                        "protocol": proto,
                        "raw_alert": record
                    })
                
                elif event_type in ["flow", "dns", "http", "tls"]:
                    base_event = {
                        "investigation_id": investigation_id,
                        "source_ip": src_ip,
                        "destination_ip": dest_ip,
                        "source_port": record.get("src_port"),
                        "destination_port": record.get("dest_port"),
                        "protocol": proto,
                        "timestamp": ts
                    }
                    
                    if event_type == "flow":
                        flow_data = record.get("flow", {})
                        base_event["bytes"] = flow_data.get("bytes_toclient", 0) + flow_data.get("bytes_toserver", 0)
                        base_event["packets"] = flow_data.get("pkts_toclient", 0) + flow_data.get("pkts_toserver", 0)
                    elif event_type == "dns":
                        base_event["dns_name"] = record.get("dns", {}).get("rrname")
                        base_event["protocol"] = "DNS"
                    elif event_type == "http":
                        http_data = record.get("http", {})
                        base_event["http_host"] = http_data.get("hostname")
                        base_event["http_uri"] = http_data.get("url")
                        base_event["http_method"] = http_data.get("http_method")
                        base_event["user_agent"] = http_data.get("http_user_agent")
                        base_event["status_code"] = http_data.get("status")
                        base_event["protocol"] = "HTTP"
                    elif event_type == "tls":
                        base_event["protocol"] = "TLS"
                        base_event["tls_metadata"] = record.get("tls", {})
                    
                    events.append(base_event)
            except Exception as e:
                pass
                
    return alerts, events

def process_pcap(filepath: str, investigation_id: int) -> Tuple[bool, List[Dict[str, Any]], List[Dict[str, Any]]]:
    if not check_suricata_availability():
        return False, [], []
        
    alerts = []
    events = []
    original_cwd = os.getcwd()
    
    cmd = get_suricata_binary() or "suricata"
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        try:
            # Execute Suricata locally reading the PCAP offline payload
            subprocess.run([cmd, "-r", filepath, "-l", temp_dir, "-k", "none"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            eve_path = os.path.join(temp_dir, "eve.json")
            alerts, events = parse_eve_json(eve_path, investigation_id)
        except Exception as e:
            print(f"Suricata extraction errored out securely inside container: {e}")
        finally:
            os.chdir(original_cwd)
            
    return True, alerts, events
