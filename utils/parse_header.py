def parse_header(lines):
    header = {}
    for line in lines:
        if "Peso Neto" in line:
            try:
                header["Peso Neto"] = float(line.split()[-1])
            except:
                header["Peso Neto"] = 0.0
    return header, None