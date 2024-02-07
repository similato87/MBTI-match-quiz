import json

def load_questions_and_dimensions():
    with open('quiz_questions.json', 'r') as file:
        data = json.load(file)
    questions = [item["question"] for item in data]
    dimensions = [item["dimension"] for item in data]
    return questions, dimensions


def take_quiz(questions):
    answers = []
    print("Please answer with 'y' for Yes or 'n' for No to the following questions:")
    for question in questions:
        while True:
            answer = input(question + " (y/n): ").lower()
            if answer in ['y', 'n']:
                answers.append('Yes' if answer == 'y' else 'No')
                break
            else:
                print("Invalid response. Please use 'y' for Yes or 'n' for No.")
    return answers


def save_user_profile(name, age, gender, occupation, answers):
    with open('user_profiles.txt', 'a') as file:
        profile = f"{name},{age},{gender},{occupation}," + ",".join(answers) + "\n"
        file.write(profile)


def load_user_profiles():
    profiles = []
    with open('user_profiles.txt', 'r') as file:
        for line in file:
            profiles.append(line.strip().split(','))
    return profiles


def load_config():
    config = {}
    with open('config.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = float(value)
    return config


def calculate_4d_distance(user_answers, other_user_answers, dimensions, config):
    dimension_scores = {'I-E': 0, 'N-S': 0, 'T-F': 0, 'J-P': 0}

    for user_answer, other_answer, dimension in zip(user_answers, other_user_answers, dimensions):
        if user_answer == other_answer:
            dimension_scores[dimension] += config.get(dimension, 1)  # Default weight is 1 if not specified

    # Normalize the scores to be between 0 and 1 for each dimension
    for dimension in dimension_scores:
        dimension_scores[dimension] = dimension_scores[dimension] / dimensions.count(dimension)

    # Calculate 4D Euclidean distance
    distance = sum((1 - score) ** 2 for score in dimension_scores.values()) ** 0.5
    return 100 * (1 - distance / 2 ** 0.5)  # Convert to percentage, max distance is sqrt(4) in 4D space


def find_matches(current_user_profile, all_profiles, dimensions, config):
    matches = []
    for profile in all_profiles:
        if profile[0] == current_user_profile[0]:  # Skip the current user
            continue
        match_score = calculate_4d_distance(current_user_profile[4:], profile[4:], dimensions, config)
        matches.append((profile[0], match_score))
    return sorted(matches, key=lambda x: x[1], reverse=True)


def display_matches(matches):
    print("Your top matches:")
    for name, percentage in matches:
        print(f"{name}: {percentage:.2f}% match")


def determine_mbti(answers, dimensions):
    mbti_dimensions = {'I-E': 0, 'N-S': 0, 'T-F': 0, 'J-P': 0}
    for answer, dimension in zip(answers, dimensions):
        if answer == 'Yes':
            mbti_dimensions[dimension] += 1  # Increment for 'Yes' responses
        else:
            mbti_dimensions[dimension] -= 1  # Decrement for 'No' responses

    # Determine MBTI type
    mbti_type = ''
    mbti_type += 'I' if mbti_dimensions['I-E'] < 0 else 'E'
    mbti_type += 'N' if mbti_dimensions['N-S'] > 0 else 'S'
    mbti_type += 'F' if mbti_dimensions['T-F'] > 0 else 'T'
    mbti_type += 'P' if mbti_dimensions['J-P'] > 0 else 'J'

    return mbti_type

def determine_mbti(answers, dimensions):
    mbti_dimensions = {'I-E': 0, 'N-S': 0, 'T-F': 0, 'J-P': 0}
    for answer, dimension in zip(answers, dimensions):
        if answer == 'Yes':
            mbti_dimensions[dimension] += 1  # Increment for 'Yes' responses
        else:
            mbti_dimensions[dimension] -= 1  # Decrement for 'No' responses

    # Determine MBTI type
    mbti_type = ''
    mbti_type += 'I' if mbti_dimensions['I-E'] < 0 else 'E'
    mbti_type += 'N' if mbti_dimensions['N-S'] > 0 else 'S'
    mbti_type += 'F' if mbti_dimensions['T-F'] > 0 else 'T'
    mbti_type += 'P' if mbti_dimensions['J-P'] > 0 else 'J'

    return mbti_type

def main():
    questions, dimensions = load_questions_and_dimensions()
    config = load_config()
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    gender = input("Enter your gender: ")
    occupation = input("Enter your occupation: ")

    answers = take_quiz(questions)
    save_user_profile(name, age, gender, occupation, answers)

    mbti_result = determine_mbti(answers, dimensions)
    print(f"{name}, your MBTI type is: {mbti_result}")

    all_profiles = load_user_profiles()
    current_user_profile = [name, age, gender, occupation] + answers
    matches = find_matches(current_user_profile, all_profiles, dimensions, config)
    display_matches(matches[:5])  # Display top 5 matches




if __name__ == "__main__":
    main()
