import math

class GameState:
    def __init__(self):
        self.cash = 100_000_000
        self.debt = 0
        self.customers = 1000
        self.price = 50000
        self.cost = 20000
        self.weight = 1
        self.inventory = 2000
        self.moq = 1000
        
        self.industry_index = 1.0
        self.product_index = 1.0
        self.competition_index = 1.0
        
        self.base_cac = 30000
        self.base_conversion = 0.02
        self.base_churn = 0.05
        
    def market_index(self):
        return self.industry_index * self.product_index * self.competition_index


def simulate_turn(state, marketing_spend, branding, r_and_d, order_multiple):
    
    incoming_units = state.moq * order_multiple
    purchase_cost = state.cost * incoming_units
    state.cash -= purchase_cost
    state.inventory += incoming_units

    cac = state.base_cac * (100 / (100 + marketing_spend/1_000_000))
    new_customers = marketing_spend / cac if cac > 0 else 0
    
    churn = state.base_churn / (100 + branding)
    existing_customers = state.customers * (1 - churn)
    
    total_customers = new_customers + existing_customers

    product_power = (100 + r_and_d) / (1000 + r_and_d/10)
    conversion = state.base_conversion * product_power * state.market_index()
    
    demand = total_customers * conversion
    sales = min(demand, state.inventory)

    revenue = sales * state.price
    
    cost_of_goods = sales * state.cost
    fee = revenue * 0.1
    logistics = sales * (3000 + state.weight * 1000)
    
    total_variable_cost = cost_of_goods + fee + logistics + marketing_spend
    fixed_cost = 2_000_000
    
    profit = revenue - total_variable_cost - fixed_cost

    state.cash += revenue - total_variable_cost - fixed_cost
    state.inventory -= sales
    state.customers = total_customers
    
    return {
        "revenue": revenue,
        "profit": profit,
        "customers": total_customers,
        "inventory": state.inventory,
        "cash": state.cash
    }


def run_game():
    state = GameState()
    
    for day in range(1, 31):
        result = simulate_turn(
            state,
            marketing_spend=5_000_000,
            branding=5,
            r_and_d=10,
            order_multiple=1
        )
        
        print(f"Day {day}")
        print(result)
        print("-" * 40)


if __name__ == "__main__":
    run_game()