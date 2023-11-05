from datetime import datetime, timedelta

# Developed by Kevin Nguyen
# CPSC 335 - Algorithms


# Convert time strings to datetime objects for easier comparison
def convert_to_datetime(time_str):
    return datetime.strptime(time_str, "%H:%M")


def convert_to_string(time):
    return time.strftime("%H:%M")


def invert_time_slots(schedule):
    inverted_schedule = []
    start_of_day = convert_to_datetime("00:00")
    end_of_day = convert_to_datetime("23:59")

    # Convert time strings to datetime objects and find inverted slots
    for index, timeslot in enumerate(schedule):
        start_time = convert_to_datetime(timeslot[0])
        end_time = convert_to_datetime(timeslot[1])

        if index == 0 and start_time > start_of_day:
            inverted_schedule.append(
                [convert_to_string(start_of_day), convert_to_string(start_time)]
            )

        if index == len(schedule) - 1 and end_time < end_of_day:
            inverted_schedule.append(
                [convert_to_string(end_time), convert_to_string(end_of_day)]
            )
        elif index < len(schedule) - 1:
            next_start_time = convert_to_datetime(schedule[index + 1][0])
            if end_time < next_start_time:
                inverted_schedule.append(
                    [convert_to_string(end_time), convert_to_string(next_start_time)]
                )

    return inverted_schedule


def find_available_slots(avail_schedule, daily_activity, duration):
    # Convert busy schedule and daily activity timings to datetime objects
    avail_slots = [
        (convert_to_datetime(start), convert_to_datetime(end))
        for start, end in avail_schedule
    ]
    daily_available = (
        convert_to_datetime(daily_activity[0]),
        convert_to_datetime(daily_activity[1]),
    )

    # Find the intersection of busy slots with the available daily time
    merged_schedule = []
    for start, end in avail_slots:
        # As long as current starting time is less than ending daily schedule
        if start < daily_available[1]:
            # Case of any available slot that ends before daily schedule is irrelevant
            if end <= daily_available[0]:
                continue

            # Case of if available time slot is before daily schedule
            if start < daily_available[0] and end > daily_available[0]:
                start = daily_available[0]

            # If ending available slot is past daily schedule
            if end > daily_available[1]:
                end = daily_available[1]

            # Sanity Check
            if start < end:
                merged_schedule.append((start, end))

    # Debugging
    # new_merged = [
    #     (convert_to_string(start), convert_to_string(end))
    #     for start, end in merged_schedule
    # ]
    # print(f"MERGED SCHEDULE: \n{new_merged}\n\n")

    return merged_schedule


def find_common_time_slots(schedule1, schedule2, min_duration):
    def time_overlap(slot1, slot2):
        start1, end1 = slot1
        start2, end2 = slot2
        return max(start1, start2), min(end1, end2)

    def filter_slots_by_duration(slots, duration):
        filtered_slots = []
        for start, end in slots:
            if (end - start) >= timedelta(minutes=duration):
                filtered_slots.append(
                    [convert_to_string(start), convert_to_string(end)]
                )
        return filtered_slots

    common_slots = []
    for slot1 in schedule1:
        for slot2 in schedule2:
            overlap_start, overlap_end = time_overlap(slot1, slot2)
            if overlap_start < overlap_end:
                common_slots.append((overlap_start, overlap_end))

    # Filter common slots by minimum duration
    common_slots_filtered = filter_slots_by_duration(common_slots, min_duration)
    return common_slots_filtered


if __name__ == "__main__":
    person1_Schedule = None 
    person2_Schedule = None 
    person1_DailyAct = None
    person2_DailyAct = None
    duration_of_meeting = None
    
    # Sample Input
    # person1_Schedule = [["7:00", "8:30"], ["12:00", "13:00"], ["16:00", "18:00"]]
    # person1_DailyAct = ["9:00", "19:00"]

    # person2_Schedule = [
    #     ["9:00", "10:30"],
    #     ["12:20", "13:30"],
    #     ["14:00", "15:00"],
    #     ["16:00", "17:00"],
    # ]
    # person2_DailyAct = ["9:00", "18:30"]

    # duration_of_meeting = 30
    
    file = open('input_testcase08.txt')
    
    for line in file: 
        exec(line)

    inverted_person1_schedule = invert_time_slots(person1_Schedule)
    inverted_person2_schedule = invert_time_slots(person2_Schedule)

    # Debugging Code
    # print(f"Schedule 1 Before Merge: {inverted_person1_schedule}")
    # print(f"Schedule 2 Before Merge: {inverted_person2_schedule}")

    # Find available slots for each person
    person1_slots = find_available_slots(
        inverted_person1_schedule, person1_DailyAct, duration_of_meeting
    )
    person2_slots = find_available_slots(
        inverted_person2_schedule, person2_DailyAct, duration_of_meeting
    )

    # Debugging Code
    # new1 = [
    #     (convert_to_string(start), convert_to_string(end))
    #     for start, end in person1_slots
    # ]
    # new2 = [
    #     (convert_to_string(start), convert_to_string(end))
    #     for start, end in person2_slots
    # ]

    # print(f"Person 1 Available Slots:\n\n{new1}\n\n")
    # print(f"Person 2 Available Slots:\n\n{new2}\n\n")

    # Find common available slots for both persons
    common_slots = find_common_time_slots(
        person1_slots, person2_slots, duration_of_meeting
    )

    print(common_slots)  # Output