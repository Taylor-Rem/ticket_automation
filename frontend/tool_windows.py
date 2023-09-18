from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QComboBox, QLineEdit
from frontend.helper_windows import HelperWidget
from functools import partial


class TicketWindow(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Ticket Helper")
        self.operation_details_window = OperationDetailsWindow(self.main_app)
        self.handle_exceptions_window = HandleExceptionsWindow(self.main_app)

        self.change_ticket_status_btn = self.create_configured_dropdown(
            ["Change Ticket Status", "Resolve", "In Progress", "Unresolve"],
            self.operations.ticket_master.change_ticket_status,
        )

        self.layout.addItem(
            QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.remove_transaction_btn = self.create_button(
            "Remove Transactions",
            partial(
                self.create_operation_window_with_widgets,
                "Remove Transactions",
                [
                    {
                        "type": "dropdown",
                        "items": [
                            "Choose Transactions",
                            "All",
                            "Except Metered",
                            "Late Fees",
                        ],
                    },
                    {
                        "type": "text",
                        "default_text": "Transaction Name",
                    },
                    {
                        "type": "text",
                        "default_text": "Transaction Amount",
                    },
                ],
            ),
        )
        self.credit_charges_btn = self.create_button(
            "Credit Charges",
            partial(
                self.create_operation_window_with_widgets,
                "Credit Charges",
                [
                    {
                        "type": "dropdown",
                        "items": ["Select Charges", "All"],
                    },
                    {
                        "type": "dropdown",
                        "items": ["Credit Type", "Concession", "Credit"],
                    },
                    {
                        "type": "text",
                        "default_text": "Charge Name",
                    },
                    {
                        "type": "text",
                        "default_text": "Charge Amount",
                    },
                ],
            ),
        )

        self.fix_manually = self.create_button(
            "Open Ticket", partial(self.open_ticket, "ledger")
        )

        self.add_back_btn()

    def check_for_ticket_exceptions(self):
        ticket_info = self.operations.ticket_master.scrape_ticket()

        exceptions = []
        if ticket_info[3] is None:
            exceptions.append("unit")
        if ticket_info[4] is None:
            exceptions.append("resident")

        if exceptions:
            self.handle_exceptions_window = HandleExceptionsWindow(
                self.main_app, exceptions
            )
            self.main_app.switch_window(self.handle_exceptions_window)

        return ticket_info

    def open_ticket(self, destination):
        ticket_info = self.check_for_ticket_exceptions()
        self.operations.open_ticket(ticket_info, destination)

    def create_exception_window_with_widgets(self, exceptions):
        self.handle_exceptions_window.create_exception_widgets(exceptions)
        self.main_app.switch_window(self.handle_exceptions_window)

    def create_operation_window_with_widgets(self, operation, widgets_info):
        self.operation_details_window.create_operation_widgets(operation, widgets_info)
        self.main_app.switch_window(self.operation_details_window)


class OperationDetailsWindow(HelperWidget):
    def __init__(self, main_app, operation_details=None):
        super().__init__(main_app, "Operation Details")
        if operation_details:
            self.create_operation_widgets(operation_details)

    def create_operation_widgets(self, operation, widgets_info):
        self.clear_layout()
        default_texts = {}
        for info in widgets_info:
            widget_type = info["type"]
            if widget_type == "button":
                button = self.create_button(info["text"], info["callback"])
                self.layout.addWidget(button)
            elif widget_type == "dropdown":
                dropdown = self.create_configured_dropdown(info["items"])
                self.layout.addWidget(dropdown)
            elif widget_type == "text":
                text_input = self.create_text_input(info["default_text"])
                self.layout.addWidget(text_input)
                default_texts[text_input] = info["default_text"]
        submit_callback = partial(self.submit, operation)
        submit_button = self.create_button("Submit", submit_callback)
        self.layout.addWidget(submit_button)
        self.add_back_btn()
        self.default_texts = default_texts

    def submit(self, operation):
        details = []
        for widget, default_text in self.default_texts.items():
            if widget.text() != default_text and widget.text() != "":
                details.append(widget.text())
        self.operations.perform_operation(operation, details)


class HandleExceptionsWindow(HelperWidget):
    def __init__(self, main_app, exception=None):
        super().__init__(main_app, "Exception:")
        self.exception_inputs = {}
        if exception:
            self.create_exception_widgets(exception)

    def create_exception_widgets(self, exceptions):
        for exception in exceptions:
            text_input = self.create_text_input(f"Enter {exception} or continue.")
            self.layout.addWidget(text_input)
            self.exception_inputs[exception] = text_input

        submit_btn = self.create_button("Submit", self.submit)
        self.layout.addWidget(submit_btn)

        self.add_back_btn()

    def submit(self):
        entered_values = {}
        for exception, text_input in self.exception_inputs.items():
            entered_values[exception] = text_input.text()

        self.main_app.switch_window(self.main_app.ticket_window)
