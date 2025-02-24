from scraper import scrape_data
from data_handler import save_to_csv, load_from_csv
from visualizer import visualizer
from kd_stats import scrape_kd_stats, save_kd_stats_to_csv, visualize_kd_stats


def scrape_and_save():
    stats = scrape_data()
    save_to_csv(stats)
    load_and_visualize()


def load_and_visualize():
    data = load_from_csv()
    if data.empty:
        print("No data found. Please scrape data first.")
        return
    visualizer(data)


def scrape_kd_stats_and_visualize():
    kd_stats = scrape_kd_stats()
    save_kd_stats_to_csv(kd_stats)
    visualize_kd_stats()


if __name__ == '__main__':
    while True:
        print("1. Scrape victory points per day data and see graph")
        print("2. Show only the victory points graph")
        print("3. Scrape kd stats and see graph")
        print("4. Show only KD graph (The information may be outdated)")
        print("5. Exit")

        try:
            choice = int(input("Your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        options = {
            1: scrape_and_save,
            2: load_and_visualize,
            3: scrape_kd_stats_and_visualize,
            4: visualize_kd_stats,
            5: exit
        }

        options.get(choice, exit)()
