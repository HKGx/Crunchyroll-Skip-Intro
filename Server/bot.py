import json

import discord
from discord.ext.commands import Bot, when_mentioned_or

import db
from cogs.crunchy import CrunchyCog

with open("bot.json") as f:
    config = json.load(f)


class CustomClient(Bot):

    def __init__(self, command_prefix):
        super(CustomClient, self).__init__(command_prefix=command_prefix, help_command=None)
        self.add_cog(CrunchyCog(self))

    @property
    def full_name(self):
        return f"{self.user.name}#{self.user.discriminator}"

    async def get_owner(self) -> discord.User:
        return (await self.application_info()).owner

    @property
    def invite_link(self):
        return f"https://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=1945632255"

    async def on_ready(self):
        try:
            with db.db_session:
                db.BotRoles(id=(await self.get_owner()).id.__str__(), role=db.ROLE_ALL)
        except db.TransactionIntegrityError:
            pass
        inv_link = f"Invite Link: {self.invite_link}"
        user_name = f"User: {self.full_name}"
        uwus = "#" * max(len(inv_link), len(user_name))
        print(uwus)
        print(inv_link)
        print(user_name)
        print(uwus, flush=True)

    async def on_message(self, message):
        await self.process_commands(message)


if __name__ == '__main__':
    client = CustomClient(command_prefix=when_mentioned_or("c!"))
    client.run(config["token"])
