import csv, os
from collections import defaultdict


# Function to read the lookup table file and create a mapping
def read_lookup_table(lookup_file):
    """
    The function `read_lookup_table` reads a lookup table from a CSV file and stores the data in a
    dictionary.
    
    :param lookup_file: The `lookup_file` parameter is a file containing data that will be used to
    create a lookup table. The function `read_lookup_table` reads this file, extracts relevant
    information (such as `dstport`, `protocol`, and `tag`) from each row, and stores it in a dictionary
    where
    :return: The function `read_lookup_table` reads a lookup table from a CSV file and returns a
    dictionary where the keys are tuples of `(dstport, protocol)` and the values are corresponding tags.
    """
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
    """
    The function `process_flow_logs` reads a flow log file, maps protocol numbers to protocol names,
    looks up tags based on destination port and protocol, and counts tag occurrences and port/protocol
    combinations.
    
    :param flow_log_file: The `flow_log_file` parameter is the file path to a log file containing
    network flow data. This function `process_flow_logs` reads the flow log file, extracts information
    such as destination port and protocol, looks up a tag based on this information using a provided
    lookup dictionary, and then counts the
    :param lookup: The `lookup` parameter in the `process_flow_logs` function is a dictionary that maps
    a tuple of `(dstport, protocol)` to a tag. The function uses this lookup dictionary to assign a tag
    based on the destination port and protocol extracted from the flow log file. If the tuple is found
    :return: The function `process_flow_logs` returns three values: `tag_counts`,
    `port_protocol_counts`, and `untagged_count`. `tag_counts` is a dictionary containing the count of
    each tag based on the lookup, `port_protocol_counts` is a dictionary containing the count of each
    port/protocol combination, and `untagged_count` is an integer representing the count of entries that
    were untag
    """
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
    """
    The function `write_tag_counts` writes tag counts to a CSV file with columns for tags and their
    corresponding counts.
    
    :param tag_counts: A dictionary where the keys are tags and the values are the corresponding counts
    of those tags
    :param output_file: The `output_file` parameter is a string that represents the file path where the
    tag counts will be written to. This file will be created or overwritten if it already exists. Make
    sure to provide the full path along with the file name and extension where you want to save the tag
    counts data
    """
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tag', 'Count'])
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])

# Function to write port/protocol counts to a CSV file
def write_port_protocol_counts(port_protocol_counts, output_file):
    """
    The function writes port, protocol, and count data to a CSV file.
    
    :param port_protocol_counts: The `port_protocol_counts` parameter is a dictionary that contains the
    counts of protocols for each port. The keys of the dictionary are tuples of `(port, protocol)` and
    the values are the corresponding counts
    :param output_file: The `output_file` parameter is a string that represents the file path where the
    output will be written. This function opens the specified file in write mode ('w') and writes the
    port, protocol, and count data to it in CSV format
    """
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Port', 'Protocol', 'Count'])
        for (port, protocol), count in port_protocol_counts.items():
            writer.writerow([port, protocol, count])