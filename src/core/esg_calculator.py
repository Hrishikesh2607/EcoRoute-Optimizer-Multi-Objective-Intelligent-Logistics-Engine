CO2_GRAMS_PER_MILE = 404

def calculate_co2_grams(total_distance_miles):
    return total_distance_miles * CO2_GRAMS_PER_MILE

def calculate_route_distance(graph, path):
    return sum(graph[u][v]["distance"] for u, v in zip(path[:-1], path[1:]))

def generate_esg_report(graph, ga_path, baseline_path):
    ga_distance = calculate_route_distance(graph, ga_path)
    baseline_distance = calculate_route_distance(graph, baseline_path)

    ga_co2 = calculate_co2_grams(ga_distance)
    baseline_co2 = calculate_co2_grams(baseline_distance)

    co2_saved_grams = baseline_co2 - ga_co2
    co2_saved_pct = (co2_saved_grams / baseline_co2 * 100) if baseline_co2 > 0 else 0

    return {
        "ga_route_distance_mi": round(ga_distance, 2),
        "baseline_route_distance_mi": round(baseline_distance, 2),
        "ga_route_co2_grams": round(ga_co2, 1),
        "baseline_route_co2_grams": round(baseline_co2, 1),
        "co2_saved_grams": round(co2_saved_grams, 1),
        "co2_saved_pct": round(co2_saved_pct, 2),
        "co2_saved_kg": round(co2_saved_grams / 1000, 3),
    }