import time
from fastapi import HTTPException
from app.config import settings
from app.rate_limiter import r

def check_and_record_cost(input_tokens: int, output_tokens: int):
    today = time.strftime("%Y-%m-%d")
    cost_key = f"daily_cost:{today}"
    
    # Calculate cost
    cost = (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006
    
    # Get current cost from Redis
    current_cost_str = r.get(cost_key)
    current_cost = float(current_cost_str) if current_cost_str else 0.0
    
    if current_cost >= settings.daily_budget_usd:
        raise HTTPException(503, "Daily budget exhausted. Try tomorrow.")
        
    # Increment cost atomically
    r.incrbyfloat(cost_key, cost)
    # Expire after 32 days
    r.expire(cost_key, 32 * 24 * 3600)

def get_daily_cost() -> float:
    today = time.strftime("%Y-%m-%d")
    cost_key = f"daily_cost:{today}"
    current_cost_str = r.get(cost_key)
    return float(current_cost_str) if current_cost_str else 0.0
