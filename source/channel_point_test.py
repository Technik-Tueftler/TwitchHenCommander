            subscriptions_channel_point = {
                "type": "channel.channel_points_custom_reward_redemption.add",
                "version": "1",
                "condition": {"broadcaster_user_id": settings["broadcaster_id"]},
                "transport": {"method": "websocket", "session_id": websocket_id},
            }
            headers = {
                "Client-ID": settings["ID"],
                "Authorization": f"Bearer {settings['token']}",
            }
            response = requests.post(
                TWITCH_SUBSCRIPTION_URL,
                json=subscriptions_channel_point,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
            print(response.json())

if event_data["metadata"]["subscription_type"] == "channel.channel_points_custom_reward_redemption.add":
    print("da war was")