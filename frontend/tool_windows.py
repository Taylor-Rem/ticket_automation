from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from frontend.helper_windows import HelperWidget
from functools import partial


class TicketWindow(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Ticket Helper")
        self.operation_details_window = OperationDetailsWindow(self.main_app)

        self.change_ticket_status_btn = self.create_configured_dropdown(
            ["Change Ticket Status", "Resolve", "In Progress", "Unresolve"],
            self.operations.change_ticket_status,
        )

        self.layout.addItem(
            QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.remove_transaction_btn = self.create_button(
            "Remove Transactions",
            lambda: self.perform_operation(
                [
                    {
                        "type": "dropdown",
                        "items": ["All", "Except Metered", "Late Fees"],
                        "callback": self.operations.test,
                    }
                ]
            ),
        )

        self.fix_manually = self.create_button(
            "Fix Manually", self.operations.open_ticket
        )

        self.add_back_btn()

    def perform_operation(self, widget_info):
        self.operation_details_window.create_operation_widgets(widget_info)
        self.main_app.switch_window(self.operation_details_window)


class OperationDetailsWindow(HelperWidget):
    def __init__(self, main_app, operation_details=None):
        super().__init__(main_app, "Operation Details")
        if operation_details:
            self.create_operation_widgets(operation_details)
        self.add_back_btn()

    def create_operation_widgets(self, widget_info):
        for info in widget_info:
            widget_type = info["type"]
            if widget_type == "button":
                self.create_button(info["text"], info["callback"])
            elif widget_type == "dropdown":
                self.create_configured_dropdown(info["items"], info["callback"])
            elif widget_type == "text":
                self.create_text_input(
                    info["title"], info["label"], info["default_text"]
                )
