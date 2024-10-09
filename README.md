# Flow Log Parser

This Python program parses flow logs and maps each row to a tag based on a lookup table. The lookup table is a CSV file that defines mappings between destination ports, protocols, and tags.

## Assumptions
- The program only supports the **default log format** for flow logs.
- The **only supported version** of the flow logs is **version 2**.
- The lookup table contains mappings for destination ports and protocols, and it's assumed that protocols are case-insensitive.

## Features
- Parses large flow log files (up to 10MB).
- Supports up to 10,000 mappings in the lookup table.
- Handles both **TCP** and **UDP** protocols.
- Tags flow logs based on port-protocol combinations.
- Provides counts of matches for each tag and each port/protocol combination.
- Flow logs with no matching tag are categorized as "Unknown tagged".

## Directory Structure
```plaintext
.
├── input/flow_logs.txt                 # Example flow log file
├── input/lookup_table.csv              # Example lookup table file
├── output/port_protocol_counts.csv     # Output port protocol count file
├── output/tag_counts.csv
├── parser.py                           # For process example data using Python script
├── app.py                              # For run main Python script
└── README.md                           # Info file
```

## Reference 
    https://iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

## Usage
- Prerequisites
    Ensure that Python 3.x installed on machine.

## Running the Program

1. Clone the repository:
```bash
git clone https://github.com/psamala52/flow_log_parser.git
cd flow_log_parser
```

2. Prepare input files:
 - `flow_logs.txt`: This is the flow log file we want to parse.
 - `lookup_table.csv`: This is the lookup table that maps port/protocol combinations to tags.

3. Run the program:
```bash
   python app.py
```

4. The program will output the following(check output folder):

    A count of matches for each tag.
    A count of matches for each port/protocol combination.

Sample Output
=============
```plaintext
Copy code
Tag Counts:
sv_P2,1
sv_P1,2
email,3
dynamic,7
sv_P4,1

Port/Protocol Combination Counts:
443,tcp,1
23,tcp,1
25,tcp,1
110,tcp,1
993,tcp,1
143,tcp,1
1024,tcp,1
80,tcp,1
1030,tcp,1
56000,tcp,1
49321,tcp,1
49152,tcp,1
49153,tcp,1
49154,tcp,1
```

Tests Performed
===============

* `Flow log format`: The program was tested with flow logs in the default format to ensure correct parsing.
* `Large file handling`: The program was tested with large flow log files (up to 10MB) to ensure it can handle larger datasets.
* `Lookup table handling`: The program was tested mappings in the lookup table (up to 10,000) to ensure it can handle data records limit.
* `Edge cases`:
    * Logs with unmatched ports or protocols are correctly categorized as "Unknown tagged".
    * Case insensitivity for protocol names was validated.
* `Performance`: The program efficiently processes large files without the need for external libraries like pandas.