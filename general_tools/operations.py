from manage_portal.tickets import TicketOperations
from resmap.navigation import ResmapNav
from resmap.ledger import LedgerOps


class TicketMaster(TicketOperations):
    def __init__(self, browser):
        super().__init__(browser)


class ResmapNavMaster(ResmapNav):
    def __init__(self, browser):
        super().__init__(browser)

    def open_ticket(self, property, unit, resident, destination="unit"):
        self.browser.launch_operation(self.browser.resmap_url)
        self.nav_to_unit(property, unit)
        if destination == "ledger":
            self.open_ledger(resident)


class LedgerMaster(LedgerOps):
    def __init__(self, browser):
        super().__init__(browser)


class Operations:
    def __init__(self, browser):
        self.browser = browser
        self.ticket_master = TicketMaster(browser)
        self.resmap_master = ResmapNavMaster(browser)
        self.ledger_master = LedgerMaster(browser)

    def perform_operation(self, operation, details):
        pass

    def open_ticket(self, ticket_info, destination):
        property = ticket_info[0]
        unit = ticket_info[1]
        resident = ticket_info[2]
        self.resmap_master.open_ticket(property, unit, resident, destination)


# class OperationsFunctions(Operations):
#     def __init__(self, browser):
#         super().__init__(browser)

#     def open_ticket(self, property, unit, resident, destination):
#         self.ticket_master._scrape_ticket()
#         self.resmap_master.open_ticket(property, unit, resident, destination)
