import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date


st.set_page_config(page_title="My Expense Tracker", page_icon="💰")
st.title("💰 My Personal Expense Tracker")
st.write("Track your daily expenses easily!")


if 'expenses' not in st.session_state:
    st.session_state.expenses = []


categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]

es
st.header("➕ Add New Expense")

with st.form("add_expense"):
    
    col1, col2 = st.columns(2)
    
    with col1:
        expense_date = st.date_input("Date", value=date.today())
        category = st.selectbox("Category", categories)
    
    with col2:
        description = st.text_input("What did you buy?", placeholder="e.g., Lunch at cafe")
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
    
    if st.form_submit_button("Add Expense", type="primary"):
        if description and amount > 0:
            
            new_expense = {
                'date': expense_date,
                'category': category,
                'description': description,
                'amount': amount
            }
          
            st.session_state.expenses.append(new_expense)
            st.success(f"✅ Added: ${amount:.2f} for {description}")
        else:
            st.error("Please fill in all fields with valid values!")


st.subheader("⚡ Quick Add")
quick_buttons = st.columns(4)

with quick_buttons[0]:
    if st.button("☕ Coffee $5"):
        st.session_state.expenses.append({
            'date': date.today(),
            'category': 'Food',
            'description': 'Coffee',
            'amount': 5.0
        })
        st.success("Added Coffee!")

with quick_buttons[1]:
    if st.button("🚌 Bus $3"):
        st.session_state.expenses.append({
            'date': date.today(),
            'category': 'Transport',
            'description': 'Bus fare',
            'amount': 3.0
        })
        st.success("Added Bus fare!")

with quick_buttons[2]:
    if st.button("🍕 Lunch $12"):
        st.session_state.expenses.append({
            'date': date.today(),
            'category': 'Food',
            'description': 'Lunch',
            'amount': 12.0
        })
        st.success("Added Lunch!")

with quick_buttons[3]:
    if st.button("🛒 Groceries $25"):
        st.session_state.expenses.append({
            'date': date.today(),
            'category': 'Shopping',
            'description': 'Groceries',
            'amount': 25.0
        })
        st.success("Added Groceries!")


st.divider()


st.header("📋 Your Expenses")

if st.session_state.expenses:
    
    df = pd.DataFrame(st.session_state.expenses)
    
    
    total_spent = df['amount'].sum()
    num_expenses = len(df)
    avg_expense = df['amount'].mean()
    
    
    metric_cols = st.columns(3)
    with metric_cols[0]:
        st.metric("💰 Total Spent", f"${total_spent:.2f}")
    with metric_cols[1]:
        st.metric("📊 Number of Expenses", num_expenses)
    with metric_cols[2]:
        st.metric("📈 Average Expense", f"${avg_expense:.2f}")
    
   
    st.subheader("Expense Details")
    
    
    display_df = df.copy()
    display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:.2f}")
    display_df['date'] = display_df['date'].astype(str)
    
    
    display_df = display_df.rename(columns={
        'date': 'Date',
        'category': 'Category',
        'description': 'Description',
        'amount': 'Amount'
    })
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
   
    st.subheader("📊 Spending by Category")
    
    category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    
  
    fig = px.pie(
        values=category_totals.values,
        names=category_totals.index,
        title="Where Your Money Goes",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
   
    if len(df) > 1:
        st.subheader("📈 Daily Spending")
        
        daily_spending = df.groupby('date')['amount'].sum().reset_index()
        daily_spending = daily_spending.sort_values('date')
        
        fig_line = px.line(
            daily_spending,
            x='date',
            y='amount',
            title='Daily Spending Trend',
            markers=True
        )
        fig_line.update_traces(line_color='#ff6b6b', line_width=3, marker_size=8)
        st.plotly_chart(fig_line, use_container_width=True)
    
  
    st.subheader("💾 Export Your Data")
    if st.button("📥 Download as CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV File",
            data=csv,
            file_name=f"my_expenses_{date.today()}.csv",
            mime="text/csv"
        )
        st.success("Click 'Download CSV File' to save your expenses!")

else:
    
    st.info("📝 No expenses added yet. Use the form above to add your first expense!")
    st.write("💡 **Tips:**")
    st.write("- Use the quick buttons for common expenses")
    st.write("- Choose the right category for better tracking")
    st.write("- Add expenses daily for best results")


with st.sidebar:
    st.header("ℹ️ App Info")
    st.write("This simple app helps you track daily expenses.")
    
    if st.session_state.expenses:
        st.write(f"📊 **Stats:**")
        st.write(f"- Total expenses: {len(st.session_state.expenses)}")
        st.write(f"- Most used category: {pd.DataFrame(st.session_state.expenses)['category'].mode().iloc[0] if st.session_state.expenses else 'None'}")
    
    st.write("---")
    st.write("💡 **How to use:**")
    st.write("1. Enter expense details in the form")
    st.write("2. Click 'Add Expense'")
    st.write("3. View your spending patterns below")
    st.write("4. Export data when needed")
    
    if st.session_state.expenses:
        st.write("---")
        if st.button("🗑️ Clear All Data", type="secondary"):
            st.session_state.expenses = []
            st.success("All data cleared!")
            st.experimental_rerun()
