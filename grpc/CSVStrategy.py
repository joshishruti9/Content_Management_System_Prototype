import csv
from StrategyInterface import strategy_interface

class csv_strategy(strategy_interface):
    def export(documents):
        print("hello")
        with open("export.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Id","Title", "Author", "Tags", "Content"])
            print(f'documents:{documents.id}')
            for document in documents:
                print(f'document:{document}')
                writer.writerow([document.id,document.title,document.author,','.join(document.tags),document.content])