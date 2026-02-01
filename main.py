from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from models import OrderRequest, DecisionResponse
from agent import build_agent
from daily_insight import generate_daily_insight, latest_insight


# 1️⃣ Create FastAPI app
app = FastAPI(title="Decision-Centric MSME AI")


# 2️⃣ Enable CORS (Frontend → Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3️⃣ Scheduler setup (Agent Push)
scheduler = BackgroundScheduler()

def daily_job():
    insight = generate_daily_insight()
    print("📊 DAILY AI INSIGHT:", insight["text"])

# 🔥 Generate insight immediately on startup (KEY LINE)
daily_job()

# 🔁 Scheduler continues running in background
scheduler.add_job(daily_job, "interval", days=1)  # keep daily for judges
scheduler.start()



# 4️⃣ Build decision agent
agent = build_agent()


# 5️⃣ API: Process Order
@app.post("/order", response_model=DecisionResponse)
def process_order(order: OrderRequest):
    result = agent.invoke({"order": order})

    return DecisionResponse(
        decision=result["decision"],
        reason=result["reason"],
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        assigned_staff=result.get("assigned_staff"),
        explanation=result.get("explanation"),
    )


# 6️⃣ API: Check Bottlenecks
@app.get("/bottleneck")
def get_bottleneck():
    result = agent.invoke({"order": None})
    return {"bottlenecks": result.get("bottlenecks", [])}


# 7️⃣ API: Get Daily Auto-Insight (Frontend)
@app.get("/daily-insight")
def get_daily_insight():
    return latest_insight
