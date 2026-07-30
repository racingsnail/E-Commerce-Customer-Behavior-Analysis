import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# ==========================================
# 1. DATA LOADING & INITIAL INSPECTION
# ==========================================

# Load the dataset
df = pd.read_csv("ecommerce_customer_behavior_dataset.csv")

print("=== DATA OVERVIEW ===")
print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")

print("\nMissing Values:")
print(df.isna().sum())

print("\nBasic Statistics:")
print(df.describe())

# ==========================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================

print("\n=== CATEGORICAL FEATURES ===")
print("\nProduct Categories:")
print(df["Product_Category"].value_counts())

print("\nPayment Methods:")
print(df["Payment_Method"].value_counts())

print("\nDevice Types:")
print(df["Device_Type"].value_counts())

print("\nReturning Customers:")
print(df["Is_Returning_Customer"].value_counts())

# Return rate share by product categories (percentage)
return_rate = (
    pd.crosstab(
        df["Product_Category"], df["Is_Returning_Customer"], normalize="index"
    )
    * 100
)
print("\nReturn Rate by Product Category (%):")
print(return_rate)

# Comparing Total Amount between returning and new customers
returning_customers = df[df["Is_Returning_Customer"] == True]
new_customers = df[df["Is_Returning_Customer"] == False]

print("\nTotal Amount - Returning Customers:")
print(returning_customers["Total_Amount"].describe())

print("\nTotal Amount - New Customers:")
print(new_customers["Total_Amount"].describe())

# Comparing Customer Ratings between returning and new customers
print("\nCustomer Rating - Returning Customers:")
print(returning_customers["Customer_Rating"].describe())

print("\nCustomer Rating - New Customers:")
print(new_customers["Customer_Rating"].describe())

# Average rating grouped by delivery time
print("\nAverage Rating by Delivery Time (Days):")
print(df.groupby("Delivery_Time_Days")["Customer_Rating"].mean())

# ==========================================
# 3. VISUALIZATION
# ==========================================

# 3.1. Orders by Product Category
plt.figure(figsize=(9, 5))
df["Product_Category"].value_counts().sort_values().plot(
    kind="bar", color="skyblue"
)
plt.title("Orders by Product Category", fontsize=14, pad=15)
plt.xlabel("Product Category", fontsize=12)
plt.ylabel("Number of Orders", fontsize=12)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("images/product_category.png", dpi=300)
plt.show()

# 3.2. Average Order Value (AOV) by Category
plt.figure(figsize=(9, 5))
df.groupby("Product_Category")["Total_Amount"].mean().sort_values().plot(
    kind="bar", color="salmon"
)
plt.title("Average Order Value by Category", fontsize=14, pad=15)
plt.xlabel("Product Category", fontsize=12)
plt.ylabel("Average Order Value", fontsize=12)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("images/average_order_value.png", dpi=300)
plt.show()

# 3.3. Average Customer Rating by Delivery Time
plt.figure(figsize=(8, 5))
df.groupby("Delivery_Time_Days")["Customer_Rating"].mean().plot(
    marker="o", color="teal", linewidth=2
)
plt.title("Average Customer Rating by Delivery Time", fontsize=14, pad=15)
plt.xlabel("Delivery Time (Days)", fontsize=12)
plt.ylabel("Average Rating", fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("images/delivery_rating.png", dpi=300)
plt.show()

# ==========================================
# 4. HYPOTHESIS TESTING
# ==========================================

print("\n=== HYPOTHESIS TESTING ===")

# Hypothesis 1: AOV between new and returning customers
print("\n--- Hypothesis 1 ---")
print("H0: The average order value of new and returning customers does not differ.")
ret_amt = df[df["Is_Returning_Customer"]]["Total_Amount"]
new_amt = df[~df["Is_Returning_Customer"]]["Total_Amount"]
u_stat, p_val = stats.mannwhitneyu(ret_amt, new_amt)
print(f"U = {u_stat:.2f}")
print(f"p-value = {p_val:.4f}")
if p_val < 0.05:
    print("Result: Reject H0")
else:
    print("Result: Fail to reject H0")

# Hypothesis 2: Ratings between new and returning customers
print("\n--- Hypothesis 2 ---")
print("H0: Ratings given by new and returning customers do not differ.")
ret_rat = df[df["Is_Returning_Customer"]]["Customer_Rating"]
new_rat = df[~df["Is_Returning_Customer"]]["Customer_Rating"]
u_stat, p_val = stats.mannwhitneyu(ret_rat, new_rat)
print(f"U = {u_stat:.2f}")
print(f"p-value = {p_val:.4f}")
if p_val < 0.05:
    print("Result: Reject H0")
else:
    print("Result: Fail to reject H0")

# Hypothesis 3: Association between product category and customer return status
print("\n--- Hypothesis 3 ---")
print("H0: Product category is not associated with customer return status.")
contingency_table = pd.crosstab(
    df["Product_Category"], df["Is_Returning_Customer"]
)
chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)
print(f"Chi2 = {chi2:.2f}")
print(f"p-value = {p_val:.4f}")
if p_val < 0.05:
    print("Result: Reject H0")
else:
    print("Result: Fail to reject H0")

# Hypothesis 4: Relationship between delivery time and customer rating
print("\n--- Hypothesis 4 ---")
print("H0: There is no relationship between delivery time and customer rating.")
rho, p_val = stats.spearmanr(df["Delivery_Time_Days"], df["Customer_Rating"])
print(f"Spearman rho = {rho:.4f}")
print(f"p-value = {p_val:.4f}")
if p_val < 0.05:
    print("Result: Reject H0")
else:
    print("Result: Fail to reject H0")
