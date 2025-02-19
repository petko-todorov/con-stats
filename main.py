from scraper import scrape_data
from data_handler import save_to_csv, load_from_csv
from vizualizer import visualizer


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


if __name__ == '__main__':
    while True:
        print("1. Scrape data and see graph")
        print("2. See only graph")
        print("3. Exit")

        try:
            choice = int(input("Your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue

        options = {
            1: scrape_and_save,
            2: load_and_visualize,
            3: exit
        }

        options.get(choice, exit)()
