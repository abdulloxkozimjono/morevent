import math

def haversine_km(lat1, lon1, lat2, lon2):
    """
    Ikkita koordinata orasidagi masofani kilometrda hisoblaydi.
    """
    R = 6371  # Yer radiusi km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c
