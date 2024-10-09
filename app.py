import os
import parser as run


# Main function to orchestrate the process
def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    flow_log_file = os.path.join(current_dir, 'input', 'flow_logs.txt')
    lookup_file = os.path.join(current_dir, 'input', 'lookup_table.csv')
    tag_counts_output_file = os.path.join(current_dir, 'output', 'tag_counts.csv')
    port_protocol_counts_output_file = os.path.join(current_dir, 'output', 'port_protocol_counts.csv')

    # Read lookup table
    # The line `lookup = run.read_lookup_table(lookup_file)` is calling a function named
    # `read_lookup_table` from the module `run` to read and process the lookup table data from the
    # file specified by `lookup_file`. The function is expected to return the processed lookup data
    # which will be stored in the variable `lookup` for further use in the script.
    lookup = run.read_lookup_table(lookup_file)

    # Process flow logs
    # The line `tag_counts, port_protocol_counts, untagged_count =
    # run.process_flow_logs(flow_log_file, lookup)` is calling a function named `process_flow_logs`
    # from the module `run` with the arguments `flow_log_file` and `lookup`.
    tag_counts, port_protocol_counts, untagged_count = run.process_flow_logs(flow_log_file, lookup)

    # Write tag counts to CSV
    # The line `run.write_tag_counts(tag_counts, tag_counts_output_file)` is calling a function named
    # `write_tag_counts` from the module `run`. This function is responsible for writing the tag
    # counts data, which is stored in the `tag_counts` variable, to a CSV file specified by the
    # `tag_counts_output_file` path. The function will take the tag counts data and write it to the
    # CSV file for further analysis or reporting purposes.
    run.write_tag_counts(tag_counts, tag_counts_output_file)

    # Write port/protocol counts to CSV
    # The line `run.write_port_protocol_counts(port_protocol_counts,
    # port_protocol_counts_output_file)` is calling a function named `write_port_protocol_counts` from
    # the module `run`. This function is responsible for writing the port/protocol counts data, which
    # is stored in the `port_protocol_counts` variable, to a CSV file specified by the
    # `port_protocol_counts_output_file` path. The function will take the port/protocol counts data
    # and write it to the CSV file for further analysis or reporting purposes.
    run.write_port_protocol_counts(port_protocol_counts, port_protocol_counts_output_file)

    print(f"Tag Counts and Port/Protocol Combination Counts generated successfully. Please check the output folder.")


if __name__ == "__main__":
    main()