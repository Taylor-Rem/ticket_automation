class LedgerScrape:
    def __init__(self, webdriver):
        self.webdriver = webdriver


class LedgerOps(LedgerScrape):
    def __init__(self, webdriver):
        super().__init__(webdriver)
