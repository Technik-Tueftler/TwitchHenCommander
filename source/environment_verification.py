#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

client_id = os.getenv("CLIENT_ID", None)
token = os.getenv("TOKEN", None)
nickname = os.getenv("NICKNAME", None)
init_channels = os.getenv("INIT_CHANNELS", None)

app_settings = {"ID": client_id, "token": token, "nickname": nickname, "channels": None}


def check_env_available() -> bool:
    if None not in (client_id, token, nickname, init_channels):
        return True
    return False


def check_config_available() -> bool:
    return False


def setting_verification() -> bool:
    if check_env_available():
        app_settings["channels"] = init_channels.split(",")
        return True
    if check_config_available():
        return True
    return False


def main() -> None:
    setting_verification()


if __name__ == "__main__":
    main()
