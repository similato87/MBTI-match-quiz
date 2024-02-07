# Personality Quiz Matcher

This Python application allows users to take a personality quiz, save their profile, and find matches with other users based on their answers. It utilizes a set of questions to evaluate the user's Myers-Briggs Type Indicator (MBTI) personality type and calculates match percentages with other users' profiles.

## Files Included

- `config.txt`: Contains configuration settings for the quiz, such as weightings for different dimensions of personality traits.
- `quiz_questions.json`: A JSON file with a list of questions and the corresponding personality dimensions they relate to.
- `user_profiles.txt`: A text file where user profiles are stored after taking the quiz. Each line represents a user's profile, including their name, age, gender, occupation, and quiz answers.
- `main.py`: The main Python script that runs the quiz, saves user profiles, and finds matches based on personality dimensions.

## Features

- **Personality Quiz**: Users can answer a series of Yes/No questions to assess their personality type across four dimensions (e.g., Introversion-Extraversion, Intuition-Sensing).
- **Save Profiles**: Upon completing the quiz, a user's profile, including their name, age, gender, occupation, and quiz responses, is saved for future matching.
- **Find Matches**: The application calculates match percentages between the current user and all other users based on their quiz responses and the configured weights for each personality dimension.
- **MBTI Assessment**: Users receive an MBTI type result based on their answers, providing insights into their personality.

## How to Use

1. Ensure you have Python installed on your system.
2. Place all project files (`config.txt`, `quiz_questions.json`, `user_profiles.txt`, and `main.py`) in the same directory.
3. Run the Python script from the command line:

```bash
python main.py
```

4. Follow the prompts to enter your name, age, gender, and occupation.
5. Answer the personality quiz questions with 'y' (Yes) or 'n' (No).
6. View your MBTI result and top matches with other users.

## Configuration

- Modify `config.txt` to adjust the weights for each personality dimension. The format is `Dimension=Weight`, where `Dimension` can be one of `I-E`, `N-S`, `T-F`, `J-P`.
- Update `quiz_questions.json` to change or add new questions. Each question must be associated with a personality dimension.

## Dependencies

- Python 3.x
- `json` module (included in standard Python library)

## Note

The application appends new user profiles to `user_profiles.txt`. Ensure to manage this file size and contents as needed.
