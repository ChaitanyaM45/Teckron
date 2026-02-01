from langgraph.graph import StateGraph
from decision_logic import (
    evaluate_order,
    assign_staff,
    deduct_inventory,
    mark_staff_unavailable,
    detect_bottlenecks,
    save_order_to_excel,
    explain_decision
)


def decision_node(state):
    order = state.get("order")

    if order is None:
        state["bottlenecks"] = detect_bottlenecks()
        return state

    decision, reason = evaluate_order(order)

    if decision != "PASS":
        save_order_to_excel(order, decision)
        state["decision"] = decision
        state["reason"] = reason
        state["explanation"] = explain_decision(decision, order)
        return state

    staff = assign_staff(order.item_name)

    if not staff:
        save_order_to_excel(order, "HOLD")
        state["decision"] = "HOLD"
        state["reason"] = "No available staff with required skill"
        state["explanation"] = explain_decision("HOLD", order)
        return state

    
    deduct_inventory(order.item_name, order.quantity)
    mark_staff_unavailable(staff)
    save_order_to_excel(order, "ACCEPT", staff)

    state["decision"] = "ACCEPT"
    state["reason"] = "Inventory and staff available"
    state["assigned_staff"] = staff
    state["explanation"] = explain_decision("ACCEPT", order, staff)

    return state


def build_agent():
    graph = StateGraph(dict)
    graph.add_node("decision", decision_node)
    graph.set_entry_point("decision")
    return graph.compile()
