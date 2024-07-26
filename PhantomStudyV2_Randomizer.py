import random
import pandas as pd


def generate_randomized_sequence_v8(participant_id, full_day=True):
    # Define the phantom variations and their pairs
    phantom_pairs_full_day = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2', 'E1', 'E2', 'F1', 'F2']
    phantom_pairs_half_day = ['A1', 'A2', 'C1', 'C2', 'E1', 'E2']

    # Select the appropriate set of phantoms based on participant's allocated time
    if full_day:
        phantom_pairs = phantom_pairs_full_day
    else:
        phantom_pairs = phantom_pairs_half_day

    # Randomize the order of phantom variations
    phantom_pairs_grouped = [phantom_pairs[i:i + 2] for i in range(0, len(phantom_pairs), 2)]
    random.shuffle(phantom_pairs_grouped)
    phantom_pairs = [phantom for pair in phantom_pairs_grouped for phantom in pair]

    techniques = ['Augmented-Reality', 'Freehand']

    operations = []
    toggle = False  # To alternate the order of techniques
    for i in range(0, len(phantom_pairs), 2):
        p1 = phantom_pairs[i]
        p2 = phantom_pairs[i + 1]

        # Alternate the techniques order
        if toggle:
            t1, t2 = techniques
        else:
            t2, t1 = techniques
        toggle = not toggle

        # Randomize the side order for p1
        sides_p1 = ['Left', 'Right']
        random.shuffle(sides_p1)

        # Randomize the side order for p2
        sides_p2 = ['Left', 'Right']
        random.shuffle(sides_p2)

        # Assign sides and techniques to both phantoms in the pair in sequence
        for side in sides_p1:
            operations.append({'Participant': participant_id, 'Phantom': p1, 'Side': side, 'Technique': t1})
        for side in sides_p2:
            operations.append({'Participant': participant_id, 'Phantom': p2, 'Side': side, 'Technique': t2})

    # Since pairs should be operated in sequence, no further shuffling is needed
    return operations


def get_participant_info():
    participants = []
    while True:
        initials = input("Enter participant initials (or 'done' to finish): ")
        if initials.lower() == 'done':
            break
        full_day_input = input("Is the participant participating full day? (yes/no): ")
        full_day = True if full_day_input.lower() == 'yes' else False
        participants.append((initials, full_day))
    return participants


def main():
    participants = get_participant_info()
    all_operations = []
    for initials, full_day in participants:
        operations = generate_randomized_sequence_v8(initials, full_day)
        all_operations.extend(operations)

    df = pd.DataFrame(all_operations)
    print(df)
    df.to_csv("randomized_sequences.csv", index=False)
    print("Randomized sequences have been saved to 'randomized_sequences.csv'.")


if __name__ == "__main__":
    main()
