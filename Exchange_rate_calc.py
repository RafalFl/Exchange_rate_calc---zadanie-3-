import requests
from datetime import datetime
import csv
from decimal import Decimal

# Funkcja pobierająca kursy walut z API NBP
def pobierz_kurs_waluty(waluta, data):
    """Pobiera kurs waluty z API NBP na podaną datę."""
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{waluta}/{data}/?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return Decimal(str(data['rates'][0]['mid']))
    elif response.status_code == 404:
        raise ValueError(f"Nie znaleziono kursu dla waluty {waluta} na datę {data}.")
    else:
        raise Exception(f"Błąd podczas pobierania kursu waluty: HTTP {response.status_code}")


# Funkcja obliczająca różnice kursowe
def oblicz_roznice_kursowa(kwota_faktury, waluta_faktury, data_faktury, kwota_platnosci, waluta_platnosci, data_platnosci):
    """Oblicza różnicę kursową na podstawie kwot i dat."""
    if waluta_faktury != 'PLN':
        kurs_faktury = pobierz_kurs_waluty(waluta_faktury, data_faktury)
    else:
        kurs_faktury = 1
    if waluta_platnosci != 'PLN':
        kurs_platnosci = pobierz_kurs_waluty(waluta_platnosci, data_platnosci)
    else:
        kurs_platnosci = 1

    kwota_faktury_pln = kwota_faktury * kurs_faktury
    kwota_platnosci_pln = kwota_platnosci * kurs_platnosci

    return kwota_platnosci_pln - kwota_faktury_pln

# Przykład zapisu danych do pliku CSV
def zapisz_dane_do_csv(nazwa_pliku, dane):
    """Zapisuje dane do pliku CSV."""
    with open(nazwa_pliku, 'a', newline='') as plik:
        writer = csv.writer(plik)
        writer.writerow(dane)

# Przykładowe dane faktury
dane_faktury = ['130', 'EUR', '2024-02-13']
dane_platnosci = ['150', 'EUR', '2023-02-13']

# Obliczenie różnicy kursowej
roznica_kursowa = oblicz_roznice_kursowa(Decimal(dane_faktury[0]), dane_faktury[1], dane_faktury[2],
                                         Decimal(dane_platnosci[0]), dane_platnosci[1], dane_platnosci[2])

# Zapis danych i wyników do pliku CSV
zapisz_dane_do_csv('dane_faktury_i_platnosci.csv', dane_faktury + dane_platnosci + [roznica_kursowa])
print(f"Zapisano dane do pliku dane_faktury_i_platnosci.csv. Różnica kursowa wynosi {roznica_kursowa} PLN.")
