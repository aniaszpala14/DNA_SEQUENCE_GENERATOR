# cel programu -> Generowanie losowej sekwencji DNA po przyjęciu od użytkownika dlugosci sekwencji, id sekwencji, opisu sekwencji oraz imienia.
# Wstawienie do wygenerowanej sekwencji w losowym miejscu podanego imienia i zapis jej do pliku w formacie FASTA oraz wyświetlenie satatystyk
# zawartości nukleodytów bez uwzględniania imienia.

# kontekst zastosowania -> program ma zastosowanie w bioinformatyce. Daje możliwość zapoznania się z zapisem formatu FASTA jak i podstawowymi analizami sekwencji DNA.

import random  # Do generowania losowej sekwencji

def generate_random_dna(length):    # funkcja generująca losową sekwencję DNA
    return ''.join(random.choices('ACGT', k=length))    # generowanie sekwencji z liter A, C, G, T o zadanej długości

def insert_name(sequence, name):    # funkcja do wstawienia imienia użytkownika w losowe miejsce sekwencji
    insert_pos = random.randint(0, len(sequence))   # losowa pozycja do wstawienia imienia
    return sequence[:insert_pos] + name + sequence[insert_pos:]    # wstawienie imienia w to losowe miejsce

def calculate_statistics(sequence): # funkcja odpowiadajaca za obliczanie statystyk sekwencji
    counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'} # zliczanie wystąpień każdego nukleotydu
    total = len(sequence) # całkowita długość sekwencji
    percentages = {nuc: round((count / total) * 100, 1) for nuc, count in counts.items()} # obliczanie procentowego udziału każdego nukleotydu
    cg_ratio = round(((counts['C'] + counts['G']) / (counts['A'] + counts['T'])) * 100, 1) if (counts['A'] + counts['T']) > 0 else 0 # obliczanie stosunku CG do AT
    return percentages, cg_ratio # zwracanie statystyk i stosunku CG

def validate_input_len():   # funkcja walidujaca dane wejściowe - dlugosc sekwencji
    while True:   # petla
        try:   # sprawdzenie czy input jest liczba
            length = int(input("Podaj długość sekwencji: "))    # pobieranie inputow od użytkownika - dlugosc sekwencji
            if length > 0:  # sprawdzenie czy dlugosc jest wieksza od 0
                return length   # zwracanie dlugosci
            else:   # jesli nie
                print("dlugosc musi byc wieksza niz 0") # komunikat o bledzie
        except ValueError:   # jesli input nie jest liczba
            print("dlugosc musi byc liczba") # komunikat o bledzie


def validate_input_id():    # funkcja walidujaca dane wejściowe - id sekwencji
    import re   # importowanie biblioteki re do walidacji id
    while True:  # petla
        seq_id = input("Podaj ID sekwencji: ")  # pobieranie inputow od użytkownika - id sekwencji
        if re.match(r'^[A-Za-z0-9_-]+$', seq_id):      # sprawdzenie czy id sklada sie z liter, cyfr, podkreśleń lub myślinków
            return seq_id   # zwracanie id
        else: # jesli nie
            print("ID powinno skladac sie z tylko liter, cyfr, podkreśleń/myślinków bez znaków białych innych specjalnych") # komunikat o bledzie


def validate_input_name():  # funkcja walidujaca dane wejściowe - imie
    while True: # petla
        name = input("Podaj imię: ") # pobieranie inputow od użytkownika - imie
        if name.isalpha():  # sprawdzenie czy imie sklada sie tylko z liter
            return name # zwracanie imienia
        else: # jesli nie
            print("imie może zawierać tylko litery")   # komunikat o bledzie


def validate_input_description():   # funkcja walidujaca dane wejściowe - opis sekwencji
    while True: # petla
        description = input("Podaj opis sekwencji: ") # pobieranie inputow od użytkownika - opis sekwencji
        if len(description.strip()) == 0: # sprawdzenie czy opis nie jest pusty
            print("Opis musi miec wiecej niz 0 znakow") # komunikat o bledzie
        else: # jesli nie
            return description  # zwracanie opisu sekwencji


def main():   # glowna funkcja wywolujaca dzialanie programu
    while True: # pętla do generowania wielu sekwencji

        # ORGINAL:
        # length = int(input("Podaj długość sekwencji: "))
        # seq_id = input("Podaj ID sekwencji: ")
        # description = input("Podaj opis sekwencji: ")
        # name = input("Podaj imię: ")
        # MODIFIED:  (dodałam walidacje danych)
        length = validate_input_len()   # pobieranie inputow od użytkownika - dlugosc sekwencji
        seq_id = validate_input_id()    # pobieranie inputow od użytkownika - id sekwencji
        description = validate_input_description()  # pobieranie inputow od użytkownika - opis sekwencji
        name = validate_input_name()    # pobieranie inputow od użytkownika - imie

        # ORIGINAL:
        # dna_sequence = ''.join(random.choices('ACGT', k=length))
        # MODIFIED:   (dodałam metode obsługującąca generowanie sekwencji w przyszlosci bedzie mozna jej ponownie uzyc zamiast powtarzac kod tez lepsza czytelnosc)
        dna_sequence = generate_random_dna(length)  # wywolanie funkcji generującej losową sekwencję

        dna_with_name = insert_name(dna_sequence, name) # wstawienie imienia  w losowym miejscu

        # zapis do pliku fasta
        filename = f"{seq_id}.fasta"    # nazwa pliku z id sekwencji
        with open(filename, 'w') as fasta_file:     # otwarcie pliku do zapisu
            fasta_file.write(f">{seq_id} {description}\n")  # zapisanie ID i opisu
            fasta_file.write(dna_with_name + '\n')  # zapisanie sekwencji DNA

        print(f"Sekwencja została zapisana do pliku {filename}") # komunikat o zapisaniu sekwencji

        stats, cg_ratio = calculate_statistics(dna_sequence)    # wywołanie funkcji obliczającej statystyki sekwencji

        # wypisanie statystyk
        print("Statystyki sekwencji:")  # wypisanie komunikatui o tym co bedzie wyswietlane
        for nuc in 'ACGT': # iteracja po nukleotydach
            print(f"{nuc}: {stats[nuc]}%")  # wypisanie statystyk dla każdego nukleotydu
        print(f"%CG: {stats['C'] + stats['G']}") # wypisanie stosunku CG

        # ORIGINAL: (bez while True i sprawdzenia czy chcesz kontynuowac)
        # def main():
        #   length = int(input("Podaj długość sekwencji: "))
        #   seq_id = input("Podaj ID sekwencji: ")
        #   description = input("Podaj opis sekwencji: ")
        #   name = input("Podaj imię: ")
        #   dna_sequence = ''.join(random.choices('ACGT', k=length))
        #   dna_with_name = insert_name(dna_sequence, name)
        #   filename = f"{seq_id}.fasta"
        #   with open(filename, 'w') as fasta_file:
        #       fasta_file.write(f">{seq_id} {description}\n")
        #       fasta_file.write(dna_with_name + '\n')
        #   print(f"Sekwencja została zapisana do pliku {filename}")
        #   stats, cg_ratio = calculate_statistics(dna_sequence)
        #   print("Statystyki sekwencji:")
        #   for nuc in 'ACGT':  # iteracja po nukleotydach
        #       print(f"{nuc}: {stats[nuc]}%")
        #   print(f"%CG: {stats['C'] + stats['G']}")

        # MODIFIED: (dodalam mozliwosc generowania wielu poprzez petle)
        again = input("Czy chcesz dalej generowac? (Tak - t): ").lower()    # zapytanie użytkownika czy chce wygenerować kolejną sekwencję
        if again != 't': # jeśli nie chce
            print("Zakończono program.") # komunikat o zakończeniu
            break # przerwanie pętli


if __name__ == "__main__":  # sprawdzenie czy skrypt jest uruchamiany bezpośrednio
    main()  # wywołanie funkcji main

