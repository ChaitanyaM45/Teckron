import { useState } from "react";

export default function Bottleneck() {
    const [issues, setIssues] = useState([]);
    const [loading, setLoading] = useState(false);

    const checkBottlenecks = async () => {
        setLoading(true);
        const response = await fetch("http://127.0.0.1:8000/bottleneck");
        const data = await response.json();
        setIssues(data.bottlenecks);
        setLoading(false);
    };

    return (
        <div className="backdrop-blur-xl bg-white/90 text-gray-900 rounded-2xl shadow-2xl p-8 transition-all hover:-translate-y-1">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                ⚙️ System Bottlenecks
            </h2>

            <p className="text-gray-600 mb-6">
                AI analyzes operational bottlenecks in real time to help you take faster
                decisions.
            </p>

            <button
                onClick={checkBottlenecks}
                className="w-full bg-slate-900 text-white py-3 rounded-xl transition-all hover:bg-slate-800 hover:shadow-lg"
            >
                {loading ? "Analyzing..." : "Check Bottlenecks"}
            </button>

            {issues.length > 0 && (
                <ul className="mt-6 space-y-2 text-sm">
                    {issues.map((issue, index) => (
                        <li
                            key={index}
                            className="p-3 rounded-lg bg-orange-50 border-l-4 border-orange-400"
                        >
                            ⚠️ {issue}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
