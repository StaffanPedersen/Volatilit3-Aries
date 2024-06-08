import csv
import io


def parse_output(self, output, scan_type=None):
    """temp hardcoding av scan_type"""
    if scan_type is None:
        scan_type = 'List'

    if scan_type == 'List':
        parse_output_csv(self, output)
    else:
        print("Invalid scan type.")


def parse_output_csv(self, output):
    csv_reader = csv.reader(io.StringIO(output))
    headers = next(csv_reader)
    tree_depth_index = headers.index("TreeDepth") if "TreeDepth" in headers else None
    if tree_depth_index is not None:
        headers.pop(tree_depth_index)
    data = [row[:tree_depth_index] + row[tree_depth_index + 1:] if tree_depth_index is not None else row for row in
            csv_reader]
    return headers, data
