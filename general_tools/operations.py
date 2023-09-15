from manage_portal.tickets import TicketOperations
from resmap.navigation import ResmapNav


class TicketMaster(TicketOperations):
    def __init__(self, browser):
        super().__init__(browser)

    def scrape_ticket(self):
        (
            self.property,
            self.unit,
            self.resident,
            self.title,
            self.description,
        ) = self.ticket_ops.scrape_ticket()


class ResmapNavMaster(ResmapNav):
    def __init__(self, browser):
        super().__init__(browser)

    def nav_to_ledger(self, property, unit, resident):
        self.nav_to_unit(property, unit)
        self.open_ledger(resident)


class Operations(TicketMaster, ResmapNavMaster):
    def __init__(self, browser):
        self.browser = browser
        TicketMaster.__init__(self, browser)
        ResmapNavMaster.__init__(self, browser)

    def open_ticket(self):
        self.scrape_ticket()
        self.browser.launch_operation(self.browser.resmap_url)
        self.nav_to_ledger(self.property, self.unit, self.resident)

    def test(self):
        print("working")
