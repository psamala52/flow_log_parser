import os
import parser as run


# Main function to orchestrate the process
def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    flow_log_file = os.path.join(current_dir, 'inputs', 'flow_logs.txt')
    lookup_file = os.path.join(current_dir, 'inputs', 'lookup_table.csv')
    tag_counts_output_file = os.path.join(current_dir, 'output', 'tag_counts.csv')
    port_protocol_counts_output_file = os.path.join(current_dir, 'output', 'port_protocol_counts.csv')

    # Read lookup table
    lookup = run.read_lookup_table(lookup_file)

    # Process flow logs
    tag_counts, port_protocol_counts, untagged_count = run.process_flow_logs(flow_log_file, lookup)

    # Write tag counts to CSV
    run.write_tag_counts(tag_counts, tag_counts_output_file)

    # Write port/protocol counts to CSV
    run.write_port_protocol_counts(port_protocol_counts, port_protocol_counts_output_file)

    print(f"Tag Counts and Port/Protocol Combination Counts generated successfully. Please check the output folder.")


if __name__ == "__main__":
    main()
