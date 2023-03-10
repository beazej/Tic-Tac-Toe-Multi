# Tic-Tac-Toe-Multi
## Gra multiplayer na podstawie Kółko i Krzyżyk
### Wymagania:
Python 3 oraz biblioteka Pygame.

### Opis
Jest to gra online, korzystająca z struktury klient-serwer.
Na ten moment jest to wersja z małą planszą dla dwóch graczy.

### Instrukcja
```
python3 server.py
python3 client.py
python3 client.py
```
Na początku graczowi wyświetla się ekran początkowy. W momencie kliknięcia, klient łączy się z serwerem. Zanim połączy się drugi gracz, pierwszemu wyświetla się informacja o czekaniu na drugiego gracza. Po połączeniu gracze mogą wybrać swój znak i kolor. Kolor wybierany jest za pomocą suwaka dla każdego z trzech składników modelu RGB. Można zarówno użyć przycisków "-" i "+" jak kliknąć w miejsce na suwaku.
Gdy gracz jest pewny swojej decyzji klika w przycisk "T" i oczekuje na potwierdzenie drugiego gracza. Zanim ten potwierdzi swój wybór, poprzedni gracz może wrócić do wyboru znaku i koloru. Gdy oboje potwierdzą rozpoczyna się rozrywka.
Zasady rozrywki są takie sam jak w "Kółko i krzyżyk".
Gracze mogą odbyć dowolną ilość meczy.
Z prawej strony wyświetla się informacja, który znak i kolor jest wybrany przez danego gracza. W momencie wyboru gracz zdecydowany jest zaznaczony na niebiesko. W momencie rozrywki gracz, który ma zrobić ruch jest zaznaczony na czerwono.
