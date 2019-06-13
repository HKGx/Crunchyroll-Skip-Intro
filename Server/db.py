from json import load

from pony.orm import *

with open("config.json") as f:
    config = load(f)

db = Database()

ROLE_NONE = 1 << 0
ROLE_ADD = 1 << 1
ROLE_UPDATE = 1 << 2
ROLE_REMOVE = 1 << 3
ROLE_ALL = ROLE_NONE | ROLE_ADD | ROLE_UPDATE | ROLE_REMOVE


class Episode(db.Entity):
    id = PrimaryKey(int)
    name = Optional(str)
    show = Optional(str)
    season = Optional(str)
    intro_end = Required(float)

    @property
    def full_episode_name(self):
        show_name = self.show if self.show else "Show Not Known"
        season = self.season if self.season else "Season Not Know"
        name = self.name if self.name else "Name Not Known"
        return f"{show_name} — season: {season} — {name}"


class BotRoles(db.Entity):
    id = PrimaryKey(str)
    role = Required(int)


db.bind(**config)
# db.drop_all_tables(with_all_data=True)
db.generate_mapping(create_tables=True)

