"""Missing-info intake: ask the user for anything not in their files."""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

KNOWN_FIELDS = [
    ("work_authorization", "Work authorization (e.g. US citizen, needs sponsorship)"),
    ("salary_expectation", "Salary expectation"),
    ("availability", "Available start date"),
    ("years_experience", "Years of experience"),
    ("highest_education", "Highest education"),
    ("willing_to_relocate", "Willing to relocate? (y/n)"),
]


def ask_missing_info(parent=None) -> dict[str, str]:
    """Pop up a dialog; returns dict of field -> answer. Empty dict if cancelled."""
    dlg = QDialog(parent)
    dlg.setWindowTitle("Application details needed")
    form = QFormLayout(dlg)
    fields: dict[str, QLineEdit] = {}
    for key, label in KNOWN_FIELDS:
        edit = QLineEdit()
        form.addRow(label + ":", edit)
        fields[key] = edit
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(dlg.accept)
    buttons.rejected.connect(dlg.reject)
    form.addRow(buttons)
    if dlg.exec() != QDialog.Accepted:
        return {}
    return {k: v.text().strip() for k, v in fields.items() if v.text().strip()}
