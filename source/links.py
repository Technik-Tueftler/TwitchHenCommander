"""
All functions to collect the links and send the collected to the configured platforms
"""

from datetime import datetime, UTC
import twitchio
import db
import hashtag_handler as hashh
import environment_verification as env

async def separate_links(message: twitchio.message.Message) -> list[str]:
    """
    Separate all links from a twitch message

    Args:
        message (twitchio.message.Message): Chat message from twitch

    Returns:
        list[str]: List of separated links
    """
    links = env.link_settings["link_pattern"].findall(message.content)
    if links is None:
        return []
    return links

async def review_links(links: set, _: str) -> set:
    """
    Review the seperated links and check if there are allowed

    Args:
        links (set): _description_
        _ (str):

    Returns:
        set: Reviewed links
    """
    return links


async def register_new_links(author: twitchio.message.Message, new_links: set) -> None:
    """
    Prevents duplications and add all new links to app_data.
    :display_name: Displayname of chatter
    :param new_hashtags: List of links from a message
    :return: None
    """
    async with hashh.lock:
        merged_links = set(hashh.app_data["links"]).union(set(new_links))
        hashh.app_data["links"] = list(merged_links)
        db_links = set()
        for link in merged_links:
            user = await db.get_twitch_user(author.id, author.display_name)
            db_links.add(
                db.Link(
                    user_id=user.id,
                    timestamp=datetime.now(UTC),
                    url=link,
                )
            )
        _ = await db.add_all_data(db_links)
