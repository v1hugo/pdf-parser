def parse_extras(lines):
    kilos_seleccionados = next((float(line.split(':')[1].strip().split()[0].replace(',', '')) for line in lines if "Kilogramos Seleccionados:" in line), 0.0)
    kilos_por_seleccionar = next((float(line.split(':')[1].strip().split()[0].replace(',', '')) for line in lines if "Kilogramos por Seleccionar:" in line), 0.0)
    return kilos_seleccionados, kilos_por_seleccionar
