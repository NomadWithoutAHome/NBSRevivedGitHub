from helpers import load_json_data
def search_episodes_by_titles(titles, data):
    matching_episodes = []
    for title in titles:
        for season, episodes in data.items():
            for episode in episodes:
                if episode["Episode Title"] == title:
                    matching_episodes.append(episode)
    return matching_episodes

#load json data from file
data = load_json_data('static/data/episode_data.json')
# Search for multiple episodes by title
titles_to_search = ["Simpsons Roasting on an Open Fire", "Bart the Genius"]
matching_episodes = search_episodes_by_titles(titles_to_search, data)

print(matching_episodes)