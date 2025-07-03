from sqlalchemy.orm import Session
from typing import Type, Any
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import and_
import json


def get_dropdown_options(
    db: Session,
    model: Type[DeclarativeMeta],
    value_key: str = "id",
    label_key: str = "name",
    conditions: dict[str, Any] = None,
    selected_value:Any = None
) -> list[dict]:
    """
    Returns a list of dropdown options from a database model.

    Args:
        db (Session): SQLAlchemy database session.
        model (SQLAlchemy model): The table/model to query.
        value_key (str): The field to use as the value in the dropdown.
        label_key (str): The field to use as the label in the dropdown.
        conditions (dict): Optional filters to apply (e.g., {"is_active": True}).

    Returns:
        List[dict]: A list of dictionaries with "value" and "label".
    """

    # Start building the query
    query = db.query(model)

    # Apply conditions if provided

    if conditions:
        filters = []
        for field, value in conditions.items():
            column = getattr(model, field)
            filters.append(column == value)
        
        query = query.filter(and_(*filters))

    # Sort by label_key if provided
    if label_key:
        query = query.order_by(getattr(model, label_key).asc())

    # Execute the query
    results = query.all()

    # Format results as dropdown options
    options = []
    for item in results:
        value = getattr(item, value_key)
        label = getattr(item, label_key)
        is_selected = True if selected_value == value else False
        options.append({
            "value": value,
            "label": label,
            "selected": is_selected
        })

    return options




import json

def get_json_dropdown_options(
    file_path: str,
    value_key: str = "value",
    label_key: str = "label",
    selected_value: any = None,
    search: str = None
) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    options = []

    for item in data:
        label = item.get(label_key, "")
        value = item.get(value_key, "")

        if search and search.lower() not in str(label).lower():
            continue

        options.append({
            "value": value,
            "label": label,
            "selected": selected_value == value
        })

    return options



