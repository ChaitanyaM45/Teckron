import pandas as pd
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

INVENTORY_FILE = "inventory.xlsx"
STAFF_FILE = "staff.xlsx"
ORDERS_FILE = "orders.xlsx"


def load_inventory():
    # Loads inventory data from Excel into a dictionary
    df = pd.read_excel(INVENTORY_FILE)
    inventory = {}

    for _, row in df.iterrows():
        inventory[row["item_name"].strip().lower()] = {
            "quantity": int(row["quantity"]),
            "min_required": int(row["min_required"])
        }

    return inventory


def load_staff():
    # Loads staff data and availability from Excel
    df = pd.read_excel(STAFF_FILE)
    staff = []

    for _, row in df.iterrows():
        staff.append({
            "name": row["staff_name"].strip(),
            "skill": row["skill"].strip().lower(),
            "available": str(row["available"]).strip().lower() == "yes"
        })

    return staff


def evaluate_order(order):
    # Evaluates whether an order can be processed based on inventory
    inventory = load_inventory()
    item = order.item_name.strip().lower()

    if item not in inventory:
        return "REJECT", "Item not found in inventory"

    if inventory[item]["quantity"] < order.quantity:
        return "HOLD", "Insufficient stock"

    return "PASS", "Inventory available"


def assign_staff(item_name):
    # Assigns an available staff member whose skill matches the item
    item = item_name.strip().lower()

    for staff in load_staff():
        if staff["skill"] == item and staff["available"]:
            return staff["name"]

    return None


def deduct_inventory(item_name, quantity):
    # Deducts ordered quantity from inventory after acceptance
    item = item_name.strip().lower()
    df = pd.read_excel(INVENTORY_FILE)

    for idx, row in df.iterrows():
        if row["item_name"].strip().lower() == item:
            df.at[idx, "quantity"] = max(0, int(row["quantity"]) - quantity)
            break

    df.to_excel(INVENTORY_FILE, index=False)


def mark_staff_unavailable(staff_name):
    # Marks the assigned staff member as unavailable
    df = pd.read_excel(STAFF_FILE)

    for idx, row in df.iterrows():
        if row["staff_name"].strip().lower() == staff_name.strip().lower():
            df.at[idx, "available"] = "no"
            break

    df.to_excel(STAFF_FILE, index=False)


def detect_bottlenecks():
    # Detects inventory shortages and staff unavailability
    inventory = load_inventory()
    staff = load_staff()
    bottlenecks = []

    for item, data in inventory.items():
        if data["quantity"] < data["min_required"]:
            bottlenecks.append(f"Inventory shortage: {item}")

        if not any(s["skill"] == item and s["available"] for s in staff):
            bottlenecks.append(f"Staff unavailable for: {item}")

    return bottlenecks


def save_order_to_excel(order, decision, assigned_staff=None):
    # Saves order details and decision outcome to Excel
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "customer_name": order.customer_name,
        "customer_email": order.customer_email,
        "customer_phone": order.customer_phone,
        "item_name": order.item_name,
        "quantity": order.quantity,
        "decision": decision,
        "assigned_staff": assigned_staff or ""
    }

    try:
        df = pd.read_excel(ORDERS_FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([row])

    df.to_excel(ORDERS_FILE, index=False)


def explain_decision(decision, order, staff=None):
    # Uses Groq LLM to generate a human-readable explanation
    prompt = f"""
    You are an MSME operations assistant.

    Decision: {decision}
    Item: {order.item_name}
    Quantity: {order.quantity}
    Assigned Staff: {staff}

    Explain this decision in one short, clear sentence for a business owner.
    """

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()