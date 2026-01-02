"""
All functions to collect the links and send the collected to the configured platforms
"""

from datetime import datetime, UTC
import twitchio
import db
import hashtag_handler as hashh
import environment_verification as env
from watcher import logger

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


async def register_new_links(author: twitchio.message.Message, new_links: list) -> None:
    """
    Prevents duplications and add all new links to app_data.
    :display_name: Displayname of chatter
    :param new_hashtags: List of links from a message
    :return: None
    """
    async with hashh.lock:
        unique_links = [link for link in new_links if link not in hashh.app_data["links"]]
        merged_links = set(hashh.app_data["links"]).union(set(unique_links))
        hashh.app_data["links"] = list(merged_links)
        db_links = set()
        for link in unique_links:
            logger.debug(f"Register new link: {link} from {author.display_name}")
            user = await db.get_twitch_user(author.id, author.display_name)
            db_links.add(
                db.Link(
                    user_id=user.id,
                    stream_id=hashh.app_data["stream_id"],
                    timestamp=datetime.now(UTC),
                    url=link,
                )
            )
        _ = await db.add_all_data(db_links)
