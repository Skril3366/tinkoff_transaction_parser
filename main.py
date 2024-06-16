from dataclasses import dataclass
from enum import Enum

import pandas as pd
from bs4 import BeautifulSoup

DATA_QA_TYPE_FIELD = "data-qa-type"


class TimelineOperations(Enum):
    LIST = "timeline-operations-list"
    DATE = "timeline-operations-date"


class OperationType(Enum):
    SOURCE_AND_TARGET = "operation-source-and-target"
    MONEY = "operation-money"
    DESCRIPTION = "operation-description"
    TITLE = "operation-title"
    FOOTER_USER_MESSAGE = "operation-footer-user-message"


@dataclass
class Operation:
    date: str
    source_and_target: str
    money: str
    description: str
    title: str
    footer_user_message: str

    @staticmethod
    def from_dict(data: dict[str, str]) -> "Operation":
        return Operation(
            date=data.get(TimelineOperations.DATE.value, ""),
            source_and_target=data.get(OperationType.SOURCE_AND_TARGET.value, ""),
            money=data.get(OperationType.MONEY.value, ""),
            description=data.get(OperationType.DESCRIPTION.value, ""),
            title=data.get(OperationType.TITLE.value, ""),
            footer_user_message=data.get(OperationType.FOOTER_USER_MESSAGE.value, ""),
        )


def parse_tags(tag) -> dict[str, str]:
    result: dict[str, str] = {}
    if not hasattr(tag, "attrs"):
        return result

    if DATA_QA_TYPE_FIELD in tag.attrs:
        qa_type = tag.attrs[DATA_QA_TYPE_FIELD]
        text = tag.get_text(strip=True)
        result[qa_type] = text

    for child in tag.children:
        result.update(parse_tags(child))
    return result


def iterate_over_children(tag):
    current_date: str | None = None
    for child in tag.children:
        if child.name == "h4":
            current_date = child.text
        elif child.name == "div":
            data: dict[str, str] = parse_tags(child)
            data[TimelineOperations.DATE.value] = current_date if current_date else ""
            yield Operation.from_dict(data)


def parse_html(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    data = soup.select_one(f"[{DATA_QA_TYPE_FIELD}='{TimelineOperations.LIST.value}']")
    results = iterate_over_children(data)

    pd.DataFrame(results).to_csv(output_path, index=False)


if __name__ == "__main__":
    parse_html("input/input.html", "output/output.csv")
