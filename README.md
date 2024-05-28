# ZADANIA REKRUTACYJNE


>1. Dodaj do modelu **Persons** nowe pole age przechowujące **integery*.
Stwórz podstronę na której będzie się znajdował formularz z możliwością wyboru imienia. 
Dostępne do wyboru powinny być tylko imiona które posiadamy w modelu **Persons** (bez duplikatów). 
Po zatwierdzeniu formularza, pobierz dane za pośrednictwem api z adresu https://api.agify.io/?name=[imię]  i zapisz dane dla każdej osoby z danym imieniem. 
Wyświetl tabelę z kolumnami „imię”, „nazwisko”, „wiek”, posortowaną po wieku rosnąco omijając osoby bez wieku.

>2. Rozwiąż problem nadmiarowych zapytań w widoku skills.


>3. Zarejestruj w adminie modele z aplikacji Persons, tak aby filtrowanie i wyszukiwanie w django adminie było łatwiejsze.


>4. Napisz komendę która wyeksportuje do pliku csv dane osób wraz z ich umiejętnościami oraz pozycjami. <br />
    Lp. | imię | nazwisko | umiejętności po przecinku | pozycja 

#### Dużym plusem będzie napisanie testów jednostkowych do zaimplementowancyh zmian (rekomendowane użycie pytest).
