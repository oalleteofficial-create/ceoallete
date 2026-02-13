import streamlit as st
import math

# ===== 초기 상태 설정 =====
if "cash" not in st.session_state:
    st.session_state.cash = 100_000_000
    st.session_state.customers = 1000
    st.session_state.inventory = 2000
    st.session_state.day = 1

price = 50000
cost = 20000
moq = 1000
base_cac = 30000
base_conversion = 0.02
base_churn = 0.05

st.title("🚀 CEO 매출 확장 시뮬레이션")

# ===== 현재 상태 표시 =====
st.subheader(f"📅 Day {st.session_state.day}")
st.write("💰 현금:", int(st.session_state.cash))
st.write("👥 고객수:", int(st.session_state.customers))
st.write("📦 재고:", int(st.session_state.inventory))

# ===== 플레이어 입력 =====
marketing_spend = st.slider("마케팅비", 0, 5_000_000, 500_000, step=100_000)
branding = st.slider("브랜딩 투자", 0, 50, 5)
r_and_d = st.slider("제품개발 투자", 0, 50, 10)
order_multiple = st.slider("입고 배수 (MOQ 단위)", 0, 5, 0)

if st.button("▶ 다음 턴 진행"):

    # ===== 입고 =====
    incoming_units = moq * order_multiple
    purchase_cost = cost * incoming_units
    st.session_state.cash -= purchase_cost
    st.session_state.inventory += incoming_units

    # ===== 고객 계산 =====
    cac = base_cac * (100 / (100 + marketing_spend/1_000_000))
    new_customers = marketing_spend / cac if cac > 0 else 0

    churn = base_churn / (100 + branding)
    existing_customers = st.session_state.customers * (1 - churn)

    total_customers = new_customers + existing_customers

    # ===== 전환 =====
    product_power = (100 + r_and_d) / (1000 + r_and_d/10)
    conversion = base_conversion * product_power

    demand = total_customers * conversion
    sales = min(demand, st.session_state.inventory)

    # ===== 매출 =====
    revenue = sales * price
    cost_of_goods = sales * cost
    fee = revenue * 0.1
    logistics = sales * 4000

    total_variable_cost = cost_of_goods + fee + logistics + marketing_spend
    fixed_cost = 2_000_000

    profit = revenue - total_variable_cost - fixed_cost

    # ===== 현금 업데이트 =====
    st.session_state.cash += revenue - total_variable_cost - fixed_cost

    # ===== 재고 감소 =====
    st.session_state.inventory -= sales

    # ===== 고객 업데이트 =====
    st.session_state.customers = total_customers

    st.success(f"📈 매출: {int(revenue)}")
    st.success(f"📊 이익: {int(profit)}")

    st.session_state.day += 1