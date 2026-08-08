import os
import random
import json
from urllib.parse import quote

import requests


# ============================================================
# CONFIGURATION
# ============================================================

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

CATAAS_BASE = "https://cataas.com"


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
    Downloads the image/GIF from CATAAS first and then
    uploads the actual file to Discord.

    This prevents CATAAS from generating a different
    random cat when the Discord image is opened.
    """

    print("Downloading cat from CATAAS...")
    print("URL:", image_url)

    # --------------------------------------------------------
    # Download the actual image from CATAAS
    # --------------------------------------------------------

    image_response = requests.get(
        image_url,
        timeout=30
    )

    image_response.raise_for_status()

    content_type = image_response.headers.get(
        "Content-Type",
        "image/jpeg"
    ).lower()

    print("CATAAS content type:", content_type)

    # --------------------------------------------------------
    # Determine filename
    # --------------------------------------------------------

    if "gif" in content_type:
        filename = "cat.gif"

    elif "png" in content_type:
        filename = "cat.png"

    elif "webp" in content_type:
        filename = "cat.webp"

    else:
        filename = "cat.jpg"

    print("Filename:", filename)

    # --------------------------------------------------------
    # Discord Embed
    # --------------------------------------------------------

    embed = {
        "title": title,
        "image": {
            "url": f"attachment://{filename}"
        }
    }

    if message:
        embed["description"] = message

    payload = {
        "embeds": [embed]
    }

    # --------------------------------------------------------
    # Upload actual image to Discord
    # --------------------------------------------------------

    print("Uploading cat to Discord...")

    response = requests.post(
        DISCORD_WEBHOOK,
        data={
            "payload_json": json.dumps(payload)
        },
        files={
            "file": (
                filename,
                image_response.content,
                content_type
            )
        },
        timeout=30
    )

    # --------------------------------------------------------
    # Check Discord response
    # --------------------------------------------------------

    if response.status_code not in (200, 204):
        print("Discord webhook failed.")
        print("Status:", response.status_code)
        print("Response:", response.text)

        response.raise_for_status()

    print("Successfully posted the exact cat image to Discord.")


# ============================================================
# CAT TYPES
# ============================================================

def random_cat():
    """
    Random normal cat.
    """

    return (
        "🐱 Daily Cat",
        f"{CATAAS_BASE}/cat"
    )


def random_cat_gif():
    """
    Random cat GIF.
    """

    return (
        "😹 Cat GIF of the Hour",
        f"{CATAAS_BASE}/cat/gif"
    )


def tagged_cat():
    """
    Random tagged cat.
    """

    tag = random.choice(CAT_TAGS)

    return (
        f"🐱 Today's {tag.title()} Cat",
        f"{CATAAS_BASE}/cat/{quote(tag)}"
    )


def cat_saying():
    """
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
    Random tagged cat saying something.
    """

    tag = random.choice(CAT_TAGS)
    message = random.choice(CAT_MESSAGES)

    encoded_tag = quote(tag)
    encoded_message = quote(message)

    return (
        "😂 Cat of the Hour",
        f"{CATAAS_BASE}/cat/{encoded_tag}/says/{encoded_message}",
        message
    )


# ============================================================
# DETERMINE WHAT TO POST
# ============================================================

def get_post_for_current_time():
    """
    Every time GitHub Actions runs this script,
    randomly select one of the available cat types.
    """

    posts = [
        random_cat,
        random_cat_gif,
        tagged_cat,
        cat_saying,
        tagged_cat_saying
    ]

    selected_post = random.choice(posts)

    print("Selected cat type:", selected_post.__name__)

    return selected_post()


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("        CAT DISCORD POSTER")
    print("========================================")

    # --------------------------------------------------------
    # Select random cat post
    # --------------------------------------------------------

    post = get_post_for_current_time()

    title = post[0]
    image_url = post[1]

    # Some cat types contain a message
    message = post[2] if len(post) > 2 else None

    print("Post title:", title)

    if message:
        print("Message:", message)

    # --------------------------------------------------------
    # Download and send to Discord
    # --------------------------------------------------------

    send_to_discord(
        title=title,
        image_url=image_url,
        message=message
    )

    print("========================================")
    print("             COMPLETE")
    print("========================================")


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
