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

def calculate_category_matches(user_answers, other_user_answers, dimensions, config):
    category_scores = {'DL': 0, 'RD': 0, 'FG': 0, 'PVB': 0}
    category_counts = {'DL': 0, 'RD': 0, 'FG': 0, 'PVB': 0}

    for user_answer, other_answer, dimension in zip(user_answers, other_user_answers, dimensions):
        category_counts[dimension] += 1
        if user_answer == other_answer:
            category_scores[dimension] += config.get(dimension, 1)  # Default weight is 1 if not specified

    # Normalize the scores to be between 0 and 1 for each category
    for dimension in category_scores:
        category_scores[dimension] = 100 * (category_scores[dimension] / category_counts[dimension])

    return category_scores

def find_matches(current_user_profile, all_profiles, dimensions, config):
    matches = []
    for profile in all_profiles:
        if profile[0] == current_user_profile[0]:  # Skip the current user
            continue
        category_matches = calculate_category_matches(current_user_profile[4:], profile[4:], dimensions, config)
        average_match_score = sum(category_matches.values()) / len(category_matches)
        matches.append((profile[0], average_match_score, category_matches))
    return sorted(matches, key=lambda x: x[1], reverse=True)

def explain_high_match(category_matches):
    # Sort categories by match score
    sorted_categories = sorted(category_matches, key=category_matches.get, reverse=True)
    top_two_categories = sorted_categories[:2]
    explanation = ""

    # Combinations of top two categories and their explanations
    if 'DL' in top_two_categories and 'RD' in top_two_categories:
        explanation = ("Your top compatibilities lie in Daily Lifestyle and Relationship Dynamics, suggesting you both enjoy similar everyday activities and share effective communication and space in relationships. This combination lays a solid foundation for day-to-day harmony and understanding in partnership dynamics.")
    elif 'DL' in top_two_categories and 'FG' in top_two_categories:
        explanation = ("High matches in Daily Lifestyle and Future Goals indicate a shared enjoyment of daily routines and a common vision for the future. This suggests not only a comfortable daily life together but also aligned long-term aspirations, making for a cohesive partnership.")
    elif 'DL' in top_two_categories and 'PVB' in top_two_categories:
        explanation = ("Your compatibility in Daily Lifestyle and Personal Values and Beliefs highlights a blend of shared daily habits and core values. This unique mix can enrich your day-to-day interactions with deep respect and understanding for each other's principles and lifestyles.")
    elif 'RD' in top_two_categories and 'FG' in top_two_categories:
        explanation = ("Your strongest matches in Relationship Dynamics and Future Goals suggest a profound connection in how you manage relationships and envision your future together. This alignment promises a partnership that's not only emotionally intelligent but also forward-looking.")
    elif 'RD' in top_two_categories and 'PVB' in top_two_categories:
        explanation = ("With top compatibilities in Relationship Dynamics and Personal Values and Beliefs, your relationship is likely to be characterized by strong communication, mutual respect, and shared fundamental values, offering a promising basis for a deep and enduring connection.")
    elif 'FG' in top_two_categories and 'PVB' in top_two_categories:
        explanation = ("The combination of Future Goals and Personal Values and Beliefs as your highest compatibilities points to a relationship grounded in shared aspirations and core principles. This pairing suggests a strong, values-driven partnership with aligned life goals.")

    return explanation

def display_matches(matches):
    print("Your top matches:")
    for name, percentage, category_matches in matches:
        print(f"{name}: {percentage:.2f}% overall match")
        explanation = explain_high_match(category_matches)
        print(explanation)

def main():
    questions, dimensions = load_questions_and_dimensions()
    config = load_config()
    name = input("Enter your name(e.g. Rachel Green): ")
    age = input("Enter your age(e.g. 30): ")
    gender = input("Enter your gender(e.g. M or F): ")
    occupation = input("Enter your occupation(e.g. Developer): ")

    answers = take_quiz(questions)
    save_user_profile(name, age, gender, occupation, answers)

    all_profiles = load_user_profiles()
    current_user_profile = [name, age, gender, occupation] + answers
    matches = find_matches(current_user_profile, all_profiles, dimensions, config)
    display_matches(matches[:5])  # Display top 5 matches

if __name__ == "__main__":
    main()
