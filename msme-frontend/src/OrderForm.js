import { useState } from "react";

export default function OrderForm() {
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const submitOrder = async (e) => {
        e.preventDefault();
        setLoading(true);

        const order = {
            customer_name: e.target.name.value,
            customer_email: e.target.email.value,
            item_name: e.target.item.value,
            quantity: Number(e.target.quantity.value),
        };

        const response = await fetch("http://127.0.0.1:8000/order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(order),
        });

        const data = await response.json();
        setResult(data);
        setLoading(false);
    };

    return (
        <div className="backdrop-blur-xl bg-white/90 text-gray-900 rounded-2xl shadow-2xl p-8 transition-all hover:-translate-y-1">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                📦 Place Order
            </h2>

            <form
                onSubmit={submitOrder}
                className="grid grid-cols-1 md:grid-cols-2 gap-4"
            >
                <input
                    name="name"
                    placeholder="Customer Name"
                    className="input"
                    required
                />
                <input
                    name="email"
                    type="email"
                    placeholder="Email"
                    className="input"
                    required
                />

                <select name="item" className="input md:col-span-2" required>
                    <option value="">Select Item</option>
                    <option value="cement">Cement</option>
                    <option value="bricks">Bricks</option>
                    <option value="steel">Steel</option>
                </select>

                <input
                    name="quantity"
                    type="number"
                    placeholder="Quantity"
                    className="input md:col-span-2"
                    required
                />

                <button
                    type="submit"
                    className="md:col-span-2 mt-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-3 rounded-xl font-medium shadow-lg transition-all hover:scale-[1.02]"
                >
                    {loading ? "Processing..." : "Submit Order"}
                </button>
            </form>

            {result && (
                <div className="mt-6 p-4 rounded-xl bg-slate-100 text-sm">
                    <p><b>Decision:</b> {result.decision}</p>
                    <p><b>Reason:</b> {result.reason}</p>
                    <p><b>Assigned Staff:</b> {result.assigned_staff || "None"}</p>
                    <p><b>Explanation:</b> {result.explanation}</p>
                </div>
            )}
        </div>
    );
}
