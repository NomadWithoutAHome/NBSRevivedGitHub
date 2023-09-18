import json

def load_json_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

# Load episode data from the JSON file
episode_data = load_json_data('static/Data/episode_data.json')

# Load season data from the JSON file
seasons_data = load_json_data('static/Data/season_data.json')

def extract_season_number(season_name):
    try:
        # Split the season name by space and get the last part, which is the season number
        season_number = season_name.split()[-1]
        # Convert it to an integer
        return int(season_number)
    except (IndexError, ValueError):
        return None


# Search for episodes by season number
season_number = 1  # Replace with the desired season number from the search query

matched_episodes = []

for season_name, episodes in episode_data.items():
    # Extract the season number from the season name
    season_number_in_data = extract_season_number(season_name)

    # Check if the extracted season number matches the desired season number
    if season_number_in_data == season_number:
        matched_episodes.extend(episodes)

print(matched_episodes)