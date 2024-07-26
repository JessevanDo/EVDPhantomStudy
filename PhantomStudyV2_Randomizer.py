import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# To track the counts of phantom variations at each position in the sequence
position_counts = {
    0: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0},
    1: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0},
    2: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0},
    3: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0},
    4: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0},
    5: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
}

# To track the counts of starting modalities
modality_start_counts = {'Augmented-Reality': 0, 'Freehand': 0}

# To track the counts of starting sides for each individual phantom
phantom_side_start_counts = {
    'A1': {'Left': 0, 'Right': 0}, 'A2': {'Left': 0, 'Right': 0},
    'B1': {'Left': 0, 'Right': 0}, 'B2': {'Left': 0, 'Right': 0},
    'C1': {'Left': 0, 'Right': 0}, 'C2': {'Left': 0, 'Right': 0},
    'D1': {'Left': 0, 'Right': 0}, 'D2': {'Left': 0, 'Right': 0},
    'E1': {'Left': 0, 'Right': 0}, 'E2': {'Left': 0, 'Right': 0},
    'F1': {'Left': 0, 'Right': 0}, 'F2': {'Left': 0, 'Right': 0}
}


def generate_randomized_sequence_v12(participant_id, full_day=True):
    global position_counts, modality_start_counts, phantom_side_start_counts
    # Define the phantom variations and their pairs
    phantom_pairs_full_day = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2', 'E1', 'E2', 'F1', 'F2']
    phantom_pairs_half_day = ['A1', 'A2', 'C1', 'C2', 'E1', 'E2']

    # Select the appropriate set of phantoms based on participant's allocated time
    phantom_pairs = phantom_pairs_full_day if full_day else phantom_pairs_half_day

    # Group the phantom pairs
    phantom_pairs_grouped = [phantom_pairs[i:i + 2] for i in range(0, len(phantom_pairs), 2)]

    # Balance the sequence of phantom variations
    sequence = []
    for position in range(len(phantom_pairs_grouped)):
        phantom_pairs_grouped.sort(key=lambda pair: position_counts[position][pair[0][0]])
        selected_pair = phantom_pairs_grouped.pop(0)
        sequence.extend(selected_pair)
        # Update position counts
        position_counts[position][selected_pair[0][0]] += 1
        position_counts[position][selected_pair[1][0]] += 1

    techniques = ['Augmented-Reality', 'Freehand']

    operations = []
    # Determine starting modality to balance starts across participants
    if modality_start_counts['Augmented-Reality'] <= modality_start_counts['Freehand']:
        toggle = False  # Start with AR
        modality_start_counts['Augmented-Reality'] += 1
    else:
        toggle = True  # Start with Freehand
        modality_start_counts['Freehand'] += 1

    side_count = {'Left': 0, 'Right': 0}

    for i in range(0, len(sequence), 2):
        p1 = sequence[i]
        p2 = sequence[i + 1]

        # Alternate the techniques order
        if toggle:
            t1, t2 = techniques
        else:
            t2, t1 = techniques
        toggle = not toggle

        # Randomize the side order for p1 and p2 while balancing the side starts
        sides_p1 = ['Left', 'Right']
        sides_p2 = ['Left', 'Right']

        # Ensure balanced starts
        if side_count['Left'] > side_count['Right']:
            sides_p1 = ['Right', 'Left']
            sides_p2 = ['Right', 'Left']
        elif side_count['Right'] > side_count['Left']:
            sides_p1 = ['Left', 'Right']
            sides_p2 = ['Left', 'Right']
        else:
            random.shuffle(sides_p1)
            random.shuffle(sides_p2)

        phantom_side_start_counts[p1][sides_p1[0]] += 1
        phantom_side_start_counts[p2][sides_p2[0]] += 1

        side_count[sides_p1[0]] += 1
        side_count[sides_p2[0]] += 1

        # Assign sides and techniques to both phantoms in the pair in sequence
        for side in sides_p1:
            operations.append({'Participant': participant_id, 'Phantom': p1, 'Side': side, 'Technique': t1})
        for side in sides_p2:
            operations.append({'Participant': participant_id, 'Phantom': p2, 'Side': side, 'Technique': t2})

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


def visualize_balance(position_counts, modality_start_counts, phantom_side_start_counts):
    # Convert position counts to a DataFrame for visualization
    position_df = pd.DataFrame(position_counts).T

    # Plot the balance of phantom variations at each position
    position_df.plot(kind='bar', figsize=(10, 6), stacked=True)
    plt.title('Balance of Phantom Variations at Each Position')
    plt.xlabel('Position in Sequence')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.legend(title='Phantom Variation')
    plt.show()

    # Plot the balance of starting modalities
    modality_df = pd.DataFrame.from_dict(modality_start_counts, orient='index', columns=['Count'])
    modality_df.plot(kind='bar', figsize=(6, 4))
    plt.title('Balance of Starting Modalities')
    plt.xlabel('Modality')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.show()

    # Plot the balance of starting sides for each phantom
    phantom_side_df = pd.DataFrame(phantom_side_start_counts).T
    phantom_side_df.plot(kind='bar', figsize=(12, 8), stacked=True)
    plt.title('Balance of Starting Sides for Each Phantom')
    plt.xlabel('Phantom')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.legend(title='Side')
    plt.show()


def main():
    participants = get_participant_info()
    all_operations = []
    for initials, full_day in participants:
        operations = generate_randomized_sequence_v12(initials, full_day)
        all_operations.extend(operations)

    df = pd.DataFrame(all_operations)
    print(df)
    df.to_csv("randomized_sequences.csv", index=False)
    print("Randomized sequences have been saved to 'randomized_sequences.csv'.")

    # Visualize the balance
    visualize_balance(position_counts, modality_start_counts, phantom_side_start_counts)


if __name__ == "__main__":
    main()
