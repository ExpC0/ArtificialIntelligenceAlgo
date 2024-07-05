#Roll: 1907117

def normalize_input(value, base=1):
    return value / base


def calculate_occupancy_membership(room_occupancy_level):
    membership_degrees = {}

    if room_occupancy_level < 0 or room_occupancy_level > 1:
        membership_degrees["low"] = 0
        membership_degrees["medium"] = 0
        membership_degrees["high"] = 0
    elif room_occupancy_level < 0.2:
        membership_degrees["low"] = 1
        membership_degrees["medium"] = float((room_occupancy_level - 0) * (1 / (0.2 - 0)))
        membership_degrees["high"] = 0
    elif room_occupancy_level >= 0.2 and room_occupancy_level <= 0.4:
        membership_degrees["low"] = 1
        membership_degrees["medium"] = 1
        membership_degrees["high"] = 0
    elif room_occupancy_level >= 0.4 and room_occupancy_level <= 0.6:
        membership_degrees["low"] = float((0.6 - room_occupancy_level) * (1 / (0.6 - 0.4)))
        membership_degrees["medium"] = 1
        membership_degrees["high"] = float((room_occupancy_level - 0.4) * (1 / (0.6 - 0.4)))
    elif room_occupancy_level >= 0.6 and room_occupancy_level <= 0.8:
        membership_degrees["low"] = 0
        membership_degrees["medium"] = 1
        membership_degrees["high"] = 1
    elif room_occupancy_level >= 0.8 and room_occupancy_level <= 1:
        membership_degrees["low"] = 0
        membership_degrees["medium"] = float((1 - room_occupancy_level) * (1 / (1 - 0.8)))
        membership_degrees["high"] = 1

    return membership_degrees


def calculate_time_membership(time_of_day):
    time_membership_degrees = {}

    if time_of_day < 0 or time_of_day > 24:
        time_membership_degrees["early"] = 0
        time_membership_degrees["midday"] = 0
        time_membership_degrees["evening"] = 0
    elif time_of_day <= 4:
        time_membership_degrees["early"] = 1
        time_membership_degrees["midday"] = float(time_of_day * (1 / 4))
        time_membership_degrees["evening"] = 0
    elif time_of_day > 4 and time_of_day < 6:
        time_membership_degrees["early"] = 1
        time_membership_degrees["midday"] = 1
        time_membership_degrees["evening"] = 0
    elif time_of_day >= 6 and time_of_day <= 10:
        time_membership_degrees["early"] = float((10 - time_of_day) * (1 / 4))
        time_membership_degrees["midday"] = 1
        time_membership_degrees["evening"] = float((time_of_day - 6) * (1 / 4))
    elif time_of_day >= 10 and time_of_day <= 12:
        time_membership_degrees["early"] = 0
        time_membership_degrees["midday"] = 1
        time_membership_degrees["evening"] = 1
    elif time_of_day >= 12 and time_of_day <= 24:
        time_membership_degrees["early"] = 0
        time_membership_degrees["midday"] = float((24 - time_of_day) * (1 / 12))
        time_membership_degrees["evening"] = 1

    return time_membership_degrees


def assess_rules(time_degrees, occupancy_degrees):
    short_duration = (max(time_degrees['early'], occupancy_degrees['low']) + min(time_degrees['midday'],
                                                                                 occupancy_degrees['low'])) / 2
    medium_duration = (min(time_degrees['midday'], occupancy_degrees['medium']) + min(time_degrees['evening'],
                                                                                      occupancy_degrees['medium'])) / 2
    long_duration = time_degrees['evening']
    return short_duration, medium_duration, long_duration


def defuzzify_durations(short_term, mid_term, long_term):
    numerator = 0
    denominator = 0
    for i in range(60):
        time_degrees = calculate_time_membership(i)
        max_value = max(
            min(time_degrees["early"], short_term),
            min(time_degrees["midday"], mid_term),
            min(time_degrees["evening"], long_term)
        )
        numerator += i * max_value
        denominator += max_value
    center_of_gravity = numerator / denominator if denominator != 0 else 0
    return center_of_gravity


time_input = 8
occupancy_input = 4

normalized_time = normalize_input(time_input)
normalized_occupancy = normalize_input(occupancy_input, 10)

time_membership_values = calculate_time_membership(normalized_time)
occupancy_membership_values = calculate_occupancy_membership(normalized_occupancy)

short_term_result, mid_term_result, long_term_result = assess_rules(time_membership_values, occupancy_membership_values)

final_result = defuzzify_durations(short_term_result, mid_term_result, long_term_result)
print("Defuzzified Result: ", final_result)
