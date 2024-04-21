"""
All functions for establishing the connection of a websocket to twitch and catching
the callbacks with a 2nd try.
"""

from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import (
    StreamOnlineEvent,
    StreamOfflineEvent,
    ChannelRaidEvent,
    ChannelPointsCustomRewardRedemptionAddEvent,
)
from twitchAPI.eventsub.websocket import EventSubWebsocket
import hashtag_handler as hashh

TARGET_SCOPES = []


async def stream_online(data: StreamOnlineEvent) -> None:
    await hashh.allow_collecting(True)


async def stream_offline(data: StreamOfflineEvent) -> None:
    await hashh.allow_collecting(False)
    await hashh.tweet_hashtags()


async def stream_raid(data: ChannelRaidEvent) -> None:
    print("raid")


async def channel_points(data: ChannelPointsCustomRewardRedemptionAddEvent) -> None:
    print("raid")


async def websocket_listener_2(settings: dict):
    twitch = await Twitch("my_app_id", "my_app_secret")
    await twitch.set_user_authentication("token", [], "refresh_token")
    user = await first(twitch.get_users())

    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    await eventsub.listen_stream_online(user.id, stream_online)
    await eventsub.listen_stream_offline(user.id, stream_offline)
    await eventsub.listen_channel_raid(
        stream_raid, to_broadcaster_user_id=None, from_broadcaster_user_id=user.id
    )
    await eventsub.listen_channel_points_custom_reward_redemption_add(
        user.id, stream_offline
    )
