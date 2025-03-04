import pandas as pd
import os

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "stats.csv")


def save_to_csv(stats):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    data_list = []
    for nation, victory_points in stats.items():
        for day, vp in enumerate(victory_points, start=1):
            data_list.append({"Nation": nation, "Day": day, "VP": vp})

    new_df = pd.DataFrame(data_list)

    while True:
        print("1. Update existing CSV file")
        print("2. Create new CSV file")
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            if os.path.exists(CSV_FILE) and os.stat(CSV_FILE).st_size > 0:
                existing_df = pd.read_csv(CSV_FILE)

                existing_df = existing_df[~existing_df["Nation"].isin(new_df["Nation"])]

                updated_df = pd.concat([existing_df, new_df]).sort_values(by=["Nation", "Day"])
            else:
                updated_df = new_df
            updated_df.to_csv(CSV_FILE, index=False)
            break
        elif choice == "2":
            new_df.to_csv(CSV_FILE, index=False)
            break
        else:
            print("Invalid choice. Exiting...")
            continue


def load_from_csv():
    if os.path.exists(CSV_FILE):
        if os.stat(CSV_FILE).st_size == 0:
            return pd.DataFrame(columns=["Nation", "Day", "VP"])
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Nation", "Day", "VP"])
