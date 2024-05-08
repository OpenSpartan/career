import sys
import os
import requests
import json
import locale

# Set locale for formatting numbers with thousand commas
locale.setlocale(locale.LC_ALL, '')

# Global constants
IMAGE_FOLDER = 'media'
LANGUAGE = 'en-us'
USER_AGENT = 'OpenSpartan.Career/1.0'
CAREER_ENDPOINT = 'https://gamecms-hacs.svc.halowaypoint.com/hi/Progression/file/RewardTracks/CareerRanks/careerRank1.json'
IMAGE_ENDPOINT = 'https://gamecms-hacs.svc.halowaypoint.com/hi/images/file/'
IMAGE_PREFIX = 'https://assets.den.dev/images/postmedia/halo-infinite-career-ranks/'

def download_image(image_id, token):
    if not image_id:
        return

    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": LANGUAGE,
        "X-343-Authorization-Spartan": token
    }

    folder_name, filename = os.path.split(image_id)
    os.makedirs(os.path.join(IMAGE_FOLDER, folder_name), exist_ok=True)

    file_path = os.path.join(IMAGE_FOLDER, folder_name, filename)

    if not os.path.exists(file_path):
        with open(file_path, "wb") as file:
            response = requests.get(f'{IMAGE_ENDPOINT}{image_id}', headers=headers)
            file.write(response.content)

def main():
    # Check if there are enough arguments
    if len(sys.argv) < 2:
        print("Usage: python -m career [spartan_token]")
        return
    
    # Extract the spartan_token from command line arguments
    spartan_token = sys.argv[1]

    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": LANGUAGE,
        "X-343-Authorization-Spartan": spartan_token
    }

    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    try:
        response = requests.get(CAREER_ENDPOINT, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Got career details.")
            raw_data = response.text

            with open("career_details.json", "w") as file:
                file.write(raw_data)

            json_data = json.loads(raw_data)
            ranks = json_data.get("Ranks", [])

            total_xp = sum(rank.get("XpRequiredForRank", 0) for rank in ranks)
            print(f'XP required overall: {locale.format_string("%d", total_xp, grouping=True)}')

            print('Processing rank data...')

            md_table = '''| Rank Image | Rank Adornment Image | Title | XP | Percent To Hero |
|:-----------|:---------------------|:------|:---------|:----------------|'''

            for rank in ranks:
                xp_required = rank.get("XpRequiredForRank", 0)
                rank_icon = rank.get("RankIcon", None)
                rank_large_icon = rank.get("RankLargeIcon", None)
                rank_adornment_icon = rank.get("RankAdornmentIcon", None)
                tier_type = rank.get("TierType", None)
                rank_tier = rank.get("RankTier", None)
                rank_title = rank.get("RankTitle", None)
                rank_subtitle = rank.get("RankSubTitle", None)
                current_rank = rank.get("Rank", 0)

                total_prior_xp = sum(other_rank.get("XpRequiredForRank", 0) for other_rank in ranks if other_rank.get("Rank", 0) < current_rank)
                percent_progress = total_prior_xp / total_xp
                formatted_percentage = "%.2f%%" % (percent_progress * 100)
                formatted_xp = locale.format_string("%d", xp_required, grouping=True)

                download_image(rank_icon, spartan_token)
                download_image(rank_large_icon, spartan_token)
                download_image(rank_adornment_icon, spartan_token)

                md_table += f'\n| <img src="{IMAGE_PREFIX}{rank_icon}" alt="Large rank icon for {rank_title} {rank_subtitle}"/> | <img src="{IMAGE_PREFIX}{rank_adornment_icon}" alt="Adornment rank icon for {rank_title} {rank_subtitle}"/> | {rank_subtitle} {rank_title} { rank_tier } | {formatted_xp} | {formatted_percentage} |'

            with open("career_table.md", "w") as file:
                file.write(md_table)
        else:
            print(f"Failed to get response. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
