import os
import random
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import quote

import requests


# ============================================================
# CONFIGURATION
# ============================================================

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

CATAAS_BASE = "https://cataas.com"

IST = ZoneInfo("Asia/Kolkata")


# ============================================================
# RANDOM DATA
# ============================================================

CAT_TAGS = [
    "cute",
    "orange"
]

CAT_MESSAGES = [
    "I need food.",
    "Feed me.",
    "Leave me alone.",
    "I am judging you.",
    "Where is my food?",
    "I own this place.",
    "Human detected.",
    "Not today.",
    "Give me treats.",
    "Why are you looking at me?",
    "I was sleeping.",
    "This is my house.",
    "You may pet me.",
    "No.",
    "I have decided.",
]


# ============================================================
# DISCORD
# ============================================================

def send_to_discord(title, image_url, message=None):
    """
    Sends a cat image/GIF to Discord using a webhook.
    """

    embed = {
        "title": title,
        "image": {
            "url": image_url
        }
    }

    if message:
        embed["description"] = message

    payload = {
        "embeds": [embed]
    }

    response = requests.post(
        DISCORD_WEBHOOK,
        json=payload,
        timeout=30
    )

    if response.status_code not in (200, 204):
        print("Discord webhook failed.")
        print("Status:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()

    print("Successfully posted to Discord.")


# ============================================================
# CAT TYPES
# ============================================================

def random_cat():
    """
    9 AM
    Random normal cat.
    """

    return (
        "🐱 Daily Cat",
        f"{CATAAS_BASE}/cat"
    )


def random_cat_gif():
    """
    12 PM
    Random cat GIF.
    """

    return (
        "😹 Cat GIF of the Day",
        f"{CATAAS_BASE}/cat/gif"
    )


def tagged_cat():
    """
    3 PM
    Random tagged cat.
    """

    tag = random.choice(CAT_TAGS)

    return (
        f"🐱 Today's {tag.title()} Cat",
        f"{CATAAS_BASE}/cat/{quote(tag)}"
    )


def cat_saying():
    """
    6 PM
    Random cat saying something.
    """

    message = random.choice(CAT_MESSAGES)

    encoded_message = quote(message)

    return (
        "💬 Cat Has Something to Say",
        f"{CATAAS_BASE}/cat/says/{encoded_message}",
        message
    )


def tagged_cat_saying():
    """
    9 PM
    Random tagged cat saying something.
    """

    tag = random.choice(CAT_TAGS)
    message = random.choice(CAT_MESSAGES)

    encoded_tag = quote(tag)
    encoded_message = quote(message)

    return (
        "😂 Cat of the Night",
        f"{CATAAS_BASE}/cat/{encoded_tag}/says/{encoded_message}",
        message
    )


# ============================================================
# DETERMINE WHAT TO POST
# ============================================================

def get_post_for_current_time():
    """
    Determines which cat post should be sent based on IST.
    """

    now = datetime.now(IST)

    hour = now.hour

    print("Current IST time:", now.strftime("%Y-%m-%d %H:%M:%S"))

    if hour == 9:
        return random_cat()

    elif hour == 12:
        return random_cat_gif()

    elif hour == 15:
        return tagged_cat()

    elif hour == 18:
        return cat_saying()

    elif hour == 21:
        return tagged_cat_saying()

    else:
        print(f"No scheduled cat post for {hour}:00 IST.")
        return None


# ============================================================
# MAIN
# ============================================================

def main():

    post = get_post_for_current_time()

    if post is None:
        return

    title = post[0]
    image_url = post[1]

    # Some posts contain an additional message
    message = post[2] if len(post) > 2 else None

    print("Post type:", title)
    print("Cat URL:", image_url)

    send_to_discord(
        title=title,
        image_url=image_url,
        message=message
    )


if __name__ == "__main__":
    main()
