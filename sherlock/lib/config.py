import json


class Config:
    """Branches configuration module"""

    is_loaded = False
    content: dict = None
    path = './config.json'
    wiki = []

    @classmethod
    def load(self):
        """load config file"""

        with open(self.path) as file:
            self.content = json.load(file)
            self.wiki = self.content.keys()

        self.is_loaded = True

    @classmethod
    def get(self, section: str, name: str):
        """get specific section & attribute of the configuration"""

        if not self.is_loaded:
            self.load()

        # pylint: disable=unsubscriptable-object
        return self.content[section][name]

    @classmethod
    def check(self, wiki: str):
        """"check if the current wiki is supported by the configuration"""

        if not self.is_loaded:
            self.load()

        if wiki is None:
            raise AssertionError("You must provide a `site` to crawl")

        if wiki in self.wiki:
            return

        raise NotImplementedError(
            f'"{wiki}" is not in the config file ({self.path})')
