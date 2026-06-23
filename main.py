import pandas as pd
import sqlite3 
import os

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS transactions (
#     Id INTEGER PRIMARY KEY,
#     Datetime DATETIME,
#     Source TEXT,
#     Amount DECIMAL,
#     Description TEXT,
#     Type TEXT,
#     Balance DECIMAL,
#     Month INTEGER
#     )
# """)

Top5Spend = ("""
SELECT Datetime,
       Description,
       Amount
FROM transactions
ORDER BY Amount ASC
LIMIT 5
""")

TOp5Descriptions= ("""
SELECT Description, COUNT(Description) as spend FROM transactions GROUP BY Description ORDER BY spend DESC LIMIT 5
""")

TotalMonthSpend = ("""
SELECT SUM(Amount) , Month FROM transactions GROUP BY Month
""")

clearTransactions = "DELETE FROM transactions"



def parseDescription(description):
    for index, char in enumerate(description):
        if char == ":":
            return description[index+ 2:]
    return description


Data = pd.read_csv("transactions_300.csv")

compressed = Data[["Posting Date","Transaction Type","Amount","Description","Type","Balance"]].copy()
compressed = compressed.rename(columns={"Posting Date": "Datetime"})
compressed["Datetime"] = pd.to_datetime(compressed["Datetime"])
compressed["Description"] = compressed["Description"].apply(parseDescription)
compressed["Month"] = compressed["Datetime"].dt.month
#print first 5 rows
# print(compressed[0:5])

compressed.to_sql("transactions", conn, if_exists="replace", index=False)

# results = pd.read_sql(TotalMonthSpend, conn)
# print(results)


#Terminal interaction
def clear_terminal():
    os.system("clear")

def show_menu():
    clear_terminal()
    print("-" * 30)
    print("Option 1: Top 5 Amount spent in the last 3 months")
    print("\n")
    print("Option 2: Top 5 Categories spent on in the last 3 months")
    print("\n")
    print("Option 3: Total spend by month")
    print("\n")
    print("Option 4: Clear transactions")
    print("\n")
    print("Option 5: Exit")
    print("\n")
    print("-" * 30)


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            print(pd.read_sql(Top5Spend, conn))
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            print(pd.read_sql(TOp5Descriptions, conn))
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            print(pd.read_sql(TotalMonthSpend, conn))
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            print(cursor.execute(clearTransactions))
            input("\nPress Enter to return to menu...")
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("\n[!] Invalid option. Please try again.")
            input("\nPress Enter to try again...")

if __name__ == "__main__":
    main()

conn.commit()
conn.close()

