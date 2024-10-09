import csv, os
from collections import defaultdict


# Function to read the lookup table file and create a mapping
def read_lookup_table(lookup_file):
    lookup = {}
    with open(lookup_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dstport = row['dstport'].strip().lower()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()
            lookup[(dstport, protocol)] = tag
            
            # Check for the limit of mappings
            if len(lookup) > 10000:
                raise ValueError("Exceeded maximum number of mappings (10,000).")
    return lookup

# Function to process flow log file and generate counts
def process_flow_logs(flow_log_file, lookup):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0
    
    # Check file size before processing
    if os.path.getsize(flow_log_file) > 10 * 1024 * 1024:  # 10 MB limit
        raise ValueError("The flow log file exceeds the maximum size of 10 MB.")

    # Refer : https://iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
    # The list updated as per given sample data
    # Protocol number to protocol name mapping
    PROTOCOL_MAP = {
        '1': 'icmp',      # Internet Control Message Protocol
        '2': 'igmp',      # Internet Group Management Protocol
        '6': 'tcp',       # Transmission Control Protocol
        '17': 'udp',      # User Data gram Protocol
        '41': 'ipv6',     # IPv6 encapsulation
        '47': 'gre',      # Generic Routing Encapsulation
        '50': 'esp',      # Encapsulating Security Payload
        '51': 'ah',       # Authentication Header
        '58': 'icmpv6',   # ICMP for IPv6
        '89': 'ospf',     # Open Shortest Path First
        '103': 'pim',     # Protocol Independent Multicast
        '132': 'sctp',    # Stream Control Transmission Protocol
        '112': 'vrrp',    # Virtual Router Redundancy Protocol
        '115': 'l2tp',    # Layer Two Tunneling Protocol
        '137': 'mpls-in-ip',  # Multi protocol Label Switching in IP
        '255': 'reserved' # Reserved for future use
        # Add more protocol numbers as needed and check Refer web site for it 
    }


    with open(flow_log_file, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) < 12:
                continue
            dstport = parts[5].strip().lower()
            protocol = parts[7].strip().lower()
            
            protocol_number = parts[7].strip().lower()


# Validate that the log line has at least 11 parts for version 2 logs
            if len(parts) < 11:  # Version 2 logs should have 11 or more fields
                print(f"Skipping invalid log line: {line.strip()}")
                continue

            # Extract relevant fields based on the expected structure of version 2 logs
            version = parts[0].strip().lower()      # Log version (should be '2')
            account_id = parts[1].strip().lower()   # Account ID (string)
            interface_id = parts[2].strip().lower()  # ENI ID (string)
            src_addr = parts[3].strip().lower()     # Source IP (string)
            dst_addr = parts[4].strip().lower()     # Destination IP (string)
            dstport = parts[5].strip().lower()      # Destination port (string)
            srcport = parts[6].strip().lower()      # Source port (string)
            protocol_number = parts[7].strip().lower()  # Protocol number (string)
            packets = parts[8].strip().lower()      # Packets (int)
            bytes = parts[9].strip().lower()        # Bytes (int)
            start_time = parts[10].strip().lower()  # Start time (int)
            end_time = parts[11].strip().lower()    # End time (int)
            action = parts[12].strip().lower()      # Accept or Reject (string)
            log_status = parts[13].strip().lower()  # Log status (string)

            # Validate the version number
            if version != '2':
                print(f"Unsupported log version: {version}. Skipping line: {line.strip()}")
                continue

            # Convert protocol number to protocol name (e.g., 6 -> tcp, 17 -> udp)
            protocol = PROTOCOL_MAP.get(protocol_number, 'unknown')

            # Lookup tag based on dstport and protocol
            key = (dstport, protocol)
            if key in lookup:
                tag = lookup[key]
            else:
                tag = "Unknown tagged"
                untagged_count += 1

            # Increment tag counts
            tag_counts[tag] += 1
            # Increment port/protocol combination counts
            port_protocol_counts[(dstport, protocol)] += 1

    return tag_counts, port_protocol_counts, untagged_count

# Function to write tag counts to a CSV file
def write_tag_counts(tag_counts, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tag', 'Count'])
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])

# Function to write port/protocol counts to a CSV file
def write_port_protocol_counts(port_protocol_counts, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Port', 'Protocol', 'Count'])
        for (port, protocol), count in port_protocol_counts.items():
            writer.writerow([port, protocol, count])
