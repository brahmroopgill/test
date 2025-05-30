import streamlit as st

st.set_page_config(page_title="Retirement & Legacy Planner", layout="centered")

st.title("Retirement and Legacy Planning Calculator")

# Input Section
curr_age = st.number_input("Current Age", min_value=18, max_value=100, value=25)
ret_age = st.number_input("Age of Financial Independence (Retirement Age)", min_value=curr_age+1, max_value=100, value=60)
life_exp = st.number_input("Life Expectancy", min_value=ret_age, max_value=120, value=100)

inflation = st.number_input("Expected Inflation Rate (% p.a.)", min_value=0.0, max_value=20.0, value=6.0, format="%.2f")
pre_ret_return = st.number_input("Return Before Financial Independence (% p.a.)", min_value=0.0, max_value=30.0, value=15.0, format="%.2f")
post_ret_return = st.number_input("Return After Financial Independence (% p.a.)", min_value=0.0, max_value=20.0, value=10.0, format="%.2f")
existing_return = st.number_input("Return on Existing Investments (% p.a.)", min_value=0.0, max_value=30.0, value=12.0, format="%.2f")

monthly_exp = st.number_input("Current Monthly Expenses (Rs.)", min_value=0, value=30000, step=1000)
current_inv = st.number_input("Current Investments (Rs.)", min_value=0, value=100000, step=1000)

legacy_amt = st.number_input("Inheritance to be left behind (Rs.)", min_value=0, value=10000000, step=1000)

if st.button("💡 Calculate"):

    years_to_ret = ret_age - curr_age
    years_after_ret = life_exp - ret_age

    # Project annual expenses at retirement with inflation
    annual_expense_retirement = monthly_exp * 12 * ((1 + inflation / 100) ** years_to_ret)

    # Net return after inflation during retirement for corpus calculation
    net_ret_rate = (1 + post_ret_return / 100) / (1 + inflation / 100) - 1

    # Corpus needed to cover expenses post-retirement
    if net_ret_rate > 0:
        corpus_required = annual_expense_retirement * ((1 - (1 + net_ret_rate) ** -years_after_ret) / net_ret_rate)
    else:
        corpus_required = annual_expense_retirement * years_after_ret

    # Future value of current investments
    future_value_existing = current_inv * (1 + existing_return / 100) ** years_to_ret

    # Remaining corpus to be accumulated via SIP/lumpsum
    corpus_to_accumulate = max(corpus_required - future_value_existing, 0)

    # Legacy lumpsum + SIP calculations
    legacy_lumpsum = legacy_amt / ((1 + pre_ret_return / 100) ** years_to_ret)

    monthly_rate = (1 + pre_ret_return / 100) ** (1 / 12) - 1
    months = years_to_ret * 12

    if monthly_rate > 0:
        legacy_sip = legacy_amt * monthly_rate / (((1 + monthly_rate) ** months - 1) * (1 + monthly_rate))
    else:
        legacy_sip = legacy_amt / months if months > 0 else 0

    # SIP calculation to accumulate corpus_to_accumulate
    if monthly_rate > 0 and corpus_to_accumulate > 0:
        sip = corpus_to_accumulate * monthly_rate / (((1 + monthly_rate) ** months - 1) * (1 + monthly_rate))
    else:
        sip = corpus_to_accumulate / months if months > 0 else 0

    # Lumpsum calculation to accumulate corpus_to_accumulate
    lumpsum = corpus_to_accumulate / ((1 + pre_ret_return / 100) ** years_to_ret) if years_to_ret > 0 else corpus_to_accumulate

    # Totals
    total_sip = sip + legacy_sip
    total_lumpsum = lumpsum + legacy_lumpsum

    # Display summary
    st.markdown("---")
    st.subheader("📋 Retirement Plan Summary")

    st.markdown(
        f"Your current expenses of Rs. **{monthly_exp * 12:,.0f}** will be Rs. **{annual_expense_retirement:,.0f}** "
        f"at an inflation (%) of **{inflation:.2f}** after **{years_to_ret}** years.\n\n"
        f"To meet these expenses and maintain your current standard of living, you will need to accumulate a corpus of Rs. "
        f"**{corpus_required:,.0f}**\n\n"
        f"Your current investments of Rs. **{current_inv:,.0f}** growing at **{existing_return}%** p.a. will grow to Rs. **{future_value_existing:,.0f}** by then.\n\n"
        f"So, you need to invest:\n"
        f"- A lumpsum amount of Rs. **{lumpsum:,.0f}**\n"
        f"- Or start an SIP of Rs. **{sip:,.0f}** per month for the next **{years_to_ret}** years at **{pre_ret_return}%** CAGR\n\n"
        f"To leave an inheritance of Rs. **{legacy_amt:,.0f}**, you can invest:\n"
        f"- An additional lumpsum of Rs. **{legacy_lumpsum:,.0f}**\n"
        f"- Or an additional SIP of Rs. **{legacy_sip:,.0f}** per month\n\n"
        f"**Total Monthly SIP:** Rs. **{total_sip:,.0f}**\n"
        f"**Total Lumpsum:** Rs. **{total_lumpsum:,.0f}**"
    )
