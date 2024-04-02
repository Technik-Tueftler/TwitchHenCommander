from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import StreamOnlineEvent, StreamOfflineEvent, ChannelRaidEvent, ChannelPointsCustomRewardRedemptionAddEvent
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
    # create the api instance and get user auth either from storage or website
    #twitch = await Twitch(settings["ID"], f"Bearer {settings['token']}")
    twitch = await Twitch('my_app_id', 'my_app_secret')
    # make sure to set the second parameter as the scope used to generate the token
    await twitch.set_user_authentication('token', [], 'refresh_token')
    # helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
    # await helper.bind()

    # get the currently logged in user
    user = await first(twitch.get_users())

    # create eventsub websocket instance and start the client.
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    # subscribing to the desired eventsub hook for our user
    # the given function (in this example on_follow) will be called every time this event is triggered
    # the broadcaster is a moderator in their own channel by default so specifying both as the same works in this example
    # We have to subscribe to the first topic within 10 seconds of eventsub.start() to not be disconnected.
    await eventsub.listen_stream_online(user.id, stream_online)
    await eventsub.listen_stream_offline(user.id, stream_offline)
    await eventsub.listen_channel_raid(stream_raid, to_broadcaster_user_id=None, from_broadcaster_user_id=user.id)
    await eventsub.listen_channel_points_custom_reward_redemption_add(user.id, stream_offline)
