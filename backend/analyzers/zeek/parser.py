import subprocess
import os
import tempfile
from typing import Dict, Any, List, Tuple
from datetime import datetime

def check_zeek_availability() -> bool:
    """Checks if the Zeek binary is accessible natively on the host system."""
    try:
        subprocess.run(["zeek", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def parse_zeek_log(filepath: str) -> List[Dict[str, Any]]:
    """Parses standard Zeek TSV log configurations."""
    records = []
    if not os.path.exists(filepath):
        return records
        
    with open(filepath, "r") as f:
        fields = []
        for line in f:
            if line.startswith("#fields"):
                fields = line.strip().split("\t")[1:]
            elif not line.startswith("#"):
                values = line.strip().split("\t")
                if fields and len(values) == len(fields):
                    records.append(dict(zip(fields, values)))
    return records

def process_pcap(filepath: str, investigation_id: int) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Attempts to parse a PCAP file securely using Zeek. 
    Zeek drops log artifacts into the current executing directory, so we launch it safely in an isolated temporary directory.
    """
    if not check_zeek_availability():
        return False, []
        
    all_events = []
    original_cwd = os.getcwd()
    
    # Create an isolated temporary directory to dump zeek parsed logic safely
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        try:
            # -C ignores invalid checksums cleanly, -r processes the offline payload securely
            subprocess.run(["zeek", "-C", "-r", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Extract common elements tracking back into general network schema
            if os.path.exists("conn.log"):
                conn_records = parse_zeek_log("conn.log")
                for c in conn_records:
                    all_events.append({
                        "investigation_id": investigation_id,
                        "source_ip": c.get("id.orig_h"),
                        "destination_ip": c.get("id.resp_h"),
                        "source_port": int(c.get("id.orig_p")) if c.get("id.orig_p") not in ["-", None] else None,
                        "destination_port": int(c.get("id.resp_p")) if c.get("id.resp_p") not in ["-", None] else None,
                        "protocol": c.get("proto").upper() if c.get("proto") != "-" else None,
                        "bytes": int(c.get("orig_bytes", 0)) if c.get("orig_bytes") not in ["-", None] else 0,
                        "timestamp": datetime.fromtimestamp(float(c.get("ts"))) if c.get("ts") else datetime.utcnow(),
                    })
                    
            if os.path.exists("dns.log"):
                dns_records = parse_zeek_log("dns.log")
                for d in dns_records:
                    if d.get("query") and d.get("query") != "-":
                        all_events.append({
                            "investigation_id": investigation_id,
                            "source_ip": d.get("id.orig_h"),
                            "destination_ip": d.get("id.resp_h"),
                            "protocol": "DNS",
                            "dns_name": d.get("query"),
                            "timestamp": datetime.fromtimestamp(float(d.get("ts"))) if d.get("ts") else datetime.utcnow()
                        })

            if os.path.exists("http.log"):
                http_records = parse_zeek_log("http.log")
                for h in http_records:
                    all_events.append({
                        "investigation_id": investigation_id,
                        "source_ip": h.get("id.orig_h"),
                        "destination_ip": h.get("id.resp_h"),
                        "protocol": "HTTP",
                        "http_host": h.get("host") if h.get("host") != "-" else None,
                        "http_uri": h.get("uri") if h.get("uri") != "-" else None,
                        "http_method": h.get("method") if h.get("method") != "-" else None,
                        "user_agent": h.get("user_agent") if h.get("user_agent") != "-" else None,
                        "status_code": int(h.get("status_code")) if h.get("status_code") not in ["-", None] else None,
                        "timestamp": datetime.fromtimestamp(float(h.get("ts"))) if h.get("ts") else datetime.utcnow()
                    })

        except Exception as e:
            print(f"Zeek extraction errored out securely inside container: {e}")
        finally:
            os.chdir(original_cwd)
            
    return True, all_events
