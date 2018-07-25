import csv


def write_csv(filename, lines):
    with open(filename, "wb") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(lines)


def read_csv(filename):
    lines = []
    with open(filename, "rb") as f:
        csvreader = csv.reader(f)
        for line in csvreader:
            lines.append(line)
    return lines


def read_csv_without_first_line(file_name):
    lines = read_csv(file_name)
    return lines[1:]


def try_float(value):
    try:
        value = float(value)
    except:
        value = value

    return value


def get_column(lines, columnid, elementType=''):
    column = []
    for line in lines:
        try:
            value = line[columnid]
        except:
            continue

        if elementType == 'float':
            value = try_float(value)

        column.append(value)
    return column
