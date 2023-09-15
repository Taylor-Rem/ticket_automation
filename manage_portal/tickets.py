from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class TicketScrape:
    def __init__(self, browser):
        self.browser = browser

    def scrape_ticket(self):
        try:
            property = self.browser.return_element_html(
                By.XPATH,
                "//tr/td[@class='text-xs-right' and contains(text(), 'Property')]/following-sibling::td[@class='text-xs-left']/strong/a",
            )
        except NoSuchElementException:
            property = None

        try:
            unit = self.browser.return_element_html(
                By.XPATH,
                "//tr/td[@class='text-xs-right' and contains(text(), 'Space')]/following-sibling::td[@class='text-xs-left']/a/strong",
            )
        except NoSuchElementException:
            unit = None

        try:
            resident = self.browser.return_element_html(
                By.XPATH,
                "//tr/td[@class='text-xs-right' and contains(text(), 'Resident')]/following-sibling::td[@class='text-xs-left']/a/strong",
            )
        except NoSuchElementException:
            resident = None

        try:
            title = self.browser.return_element_html(
                By.XPATH,
                '//*[contains(@class, "pull-left") and contains(@class, "text-xs-left") and contains(@class, "blue--text")]',
            )
        except:
            title = None

        try:
            description = self.browser.return_element_html(
                By.XPATH,
                "//tr/td[@class='text-xs-right' and contains(text(), 'Description')]/following-sibling::td[@class='text-xs-left']",
            )
        except NoSuchElementException:
            description = None

        return property, unit, resident, title, description


class TicketOperations(TicketScrape):
    def __init__(self, browser):
        super().__init__(browser)
        self.icons = {
            "Resolve": "done_outline",
            "In Progress": "scatter_plot",
            "Unresolve": "error",
            "Back": "arrow_back",
        }

    def change_ticket_status(self, selection):
        resolve_ticket_btn = self.browser.wait_for_presence_of_element(
            By.XPATH, "//button[contains(., 'Change Ticket Status')]"
        )
        self.browser.click_element(resolve_ticket_btn)

        resolution_btn = self.browser.wait_for_element_clickable(
            By.XPATH,
            f"//button[.//i[contains(@class, 'material-icons') and text()='{self.icons[selection]}']]",
        )
        self.browser.click_element(resolution_btn)

        back = selection == "In Progress" or selection == "Unresolve"

        if back:
            back_btn = self.browser.wait_for_element_clickable(
                By.XPATH,
                f"//a[.//i[contains(@class, 'material-icons') and text()='arrow_back']]",
            )
            self.browser.click_element(back_btn)
