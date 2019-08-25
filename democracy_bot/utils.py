"""Utility functions"""

import discord


def get_name(member: discord.Member):
    """Returns nick primarily and falls back to username"""
    return member.name if member.nick is None else member.nick
