import { useEffect, useState } from "react";
import OrderForm from "./OrderForm";
import Bottleneck from "./Bottleneck";

export default function App() {
  const [dailyInsight, setDailyInsight] = useState("Loading daily insight...");

  useEffect(() => {
    fetch("https://msme-s.onrender.com/daily-insight")
      .then((res) => res.json())
      .then((data) => {
        if (data?.text) setDailyInsight(data.text);
      })
      .catch(() => {
        setDailyInsight("Unable to fetch daily insight.");
      });
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1e3c72] to-[#2a5298] text-white">
      {/* Header */}
      <header className="py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-bold tracking-wide">
          Decision-Centric MSME AI
        </h1>
        <p className="mt-4 text-white/80 text-lg">
          Smart decisions for small & medium businesses
        </p>
      </header>

      {/* Dashboard */}
      <main className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-10 pb-20">
        <OrderForm />
        <Bottleneck />

        {/* Daily Insight Card */}
        <div className="md:col-span-2 backdrop-blur-xl bg-white/90 text-gray-900 rounded-2xl shadow-2xl p-8">
          <h2 className="text-xl font-semibold mb-3 flex items-center gap-2">
            📊 Daily AI Insight
          </h2>
          <p className="text-gray-700">{dailyInsight}</p>
        </div>
      </main>
    </div>
  );
}
