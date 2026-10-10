# Victorum-Enhanced -> Ante Bellum modpack: raport scalenia

Stan: pierwsze scalenie "na sucho" (bez bazowego moda Ante Bellum i bez możliwości uruchomienia gry w tym środowisku).
Nic poniżej nie zostało przetestowane w grze. Sprawdzono tylko składnię (balans nawiasów) i spójność odwołań.

## Zasady, które przyjęto

| Obszar | Decyzja |
|---|---|
| Mapa (`map/`), historia prowincji/krajów, grafiki mapy | zostają z Antebellum, nic z Victorum nie jest kopiowane |
| Mechaniki: `common/`, `decisions/`, `events/`, `missions/`, `interface/`, `localisation/`, `customizable_localization/` | kopiowane z Victorum (`common/bookmarks/` pominięte, bo zależą od historii) |
| Ten sam plik w obu modach (452, z czego ~120 w katalogach mechanik) | **Victorum wygrywa** na poziomie bloków; bloki istniejące tylko w Antebellum są dopisywane na końcu |
| Blok istnieje w obu, ale Antebellum ma w nim własne elementy | elementy Antebellum (nowe reformy, przywileje, hooki w on_actions, przyciski GUI itd.) są **wstrzykiwane** do wersji Victorum (808 wstrzyknięć) |
| Ten sam klucz w *różnych* plikach (31 przypadków, np. `POL_ideas`, `declarewar`, `can_exploit_tax`) | Victorum wygrywa, wersja Antebellum jest usunięta z jego pliku, a jej własne elementy wstrzyknięte do bloku Victorum |
| Kolizje tagów (`CTG`, `PU3`, `RSL`) | Antebellum zachowuje swoje (Kartagina, Punic3, Latinsphere Revolt); tagi Victorum przemianowane na `XCA`, `XCB`, `XCC` (skrypty, lokalizacja, flagi) |
| Drzewka misji dla tego samego tagu i slotu (705 serii) | Seria Victorum dostaje `NOT = { potential serii Antebellum }`, więc dla krajów z drzewem Antebellum działa ono, a Victorum tylko tam, gdzie Antebellum nie ma drzewa |
| `common/defines/01_tlw.lua` | przemianowany na `zz_01_tlw.lua`, żeby ładował się po `defines.lua` Victorum (inaczej Victorum mógłby je nadpisać) |

## Dopasowanie do mapy Antebellum

Mapa Antebellum ma prowincje 1-5210 (te same ID co w Victorum, sprawdzone po nazwach w 221 z 234 plików historii), Victorum ma 1-8911.
Wszystkie odwołania do prowincji 5211-8911 w skryptach zostały zneutralizowane:

- 1281 warunków (`owns`, `province_id`, `NNNN = { ... }` w triggerze itd.) zamienionych na `always = no`
- 4192 efekty (`add_permanent_claim`, `NNNN = { ... }` w efekcie, `goto`, `set_capital`...) usunięte
- 7326 ID usuniętych z list (`provinces`, `members`, `path`, `holy_sites`) i wpisów `province_names`
- 4 węzły handlowe usunięte, bo ich `location` nie istnieje na mapie: `aegean_trade`, `canton`, `namibia_trade`, `philippines` (+8 połączeń `outgoing` do nich)
- 138 wielkich projektów (`great_projects`) z `start` poza mapą usuniętych (odwołania do nich w skryptach mogą wpisać się w log błędów)

Zmienione miejsca oznaczone są komentarzem `# [VU] ... not on Ante Bellum map` (tam, gdzie komentarz nie zepsułby linii).
Obszary/regiony (`area`, `region`) z Victorum, których nie ma w mapie Antebellum, nie mogły być sprawdzone (brak `map/area.txt` w repo); ich skutkiem będą co najwyżej wpisy w logu błędów.
Trzynaście prowincji ma w Antebellum inne nazwy niż w Victorum przy tym samym ID (np. 959/960 Cayuga/Onondaga); nie były przemapowywane.

## Poprawki z grotaclasBugfixes

- Victorum: 188 sekcji plików z patchy nałożone (dokładny kontekst, bez fuzz), 86 konfliktów i 45 brakujących plików opisane w `bugfixes_status_victorum.md`
- Antebellum: 10 sekcji nałożone; 301 dotyczy plików, które są w bazowym modzie Ante Bellum (nie ma ich w tym repo). Po dodaniu bazy trzeba puścić `tools/merge/applyfix.py` ponownie
- Pierwsza wersja używała fuzzu i wstawiła część hunków w złe bloki; po review została przerobiona (commit "Redo grotaclas Bugfixes").
- Pliki Victorum po poprawkach trafiły do Antebellum (Victorum wygrywa), więc ich poprawki są już w wyniku

## Co jest ryzykiem (i czego nie da się dziś sprawdzić)

1. **Brak bazy Ante Bellum.** Pliki Victorum o nazwach takich jak w bazie nadpiszą bazę (np. `common/tradenodes/00_tradenodes.txt`, `common/defines/defines.lua`, `common/ideas/00_country_ideas.txt`). Po dodaniu bazy trzeba uruchomić `tools/merge/merge.py` ze ścieżką do bazy jako "A", żeby ten sam algorytm zrobił scalenie z bazą, i `tools/merge/dups.py`, żeby wyłapać kolizje kluczy i tagów.
2. **Mapa-zależne dane z Victorum** (`tradenodes`, `colonial_regions`, `trade_companies`) zostały przycięte, nie przeprojektowane. Sieć handlu będzie wymagała przeglądu w grze.
3. **Interfejs**: okna GUI scalone po nazwie, Victorum wygrywa; elementy Antebellum dopisane do okien Victorum, ale ich rozmieszczenie nie było oglądane (możliwe nakładanie przycisków).
4. **Grafiki**: skopiowano tekstury odwoływane przez pliki `.gfx` Victorum o prefiksach `vu_`, `me_`, `GME_`, `zzz_expanded` itd. (427 plików) oraz flagi krajów Victorum (1519). Tekstury waniliowe i pozostałe ikony nie były kopiowane.
5. **Lokalizacja**: w `loadingtips_l_english.yml` (wspólny plik) Victorum wygrywa; poza nim ok. 100 kluczy ma różny tekst w różnych plikach obu modów (np. `punic`), rozstrzyga kolejność ładowania plików, nic nie usuwano.
6. Seria misji Victorum, której `potential` nie zawiera `tag = ...`, nie jest bramkowana.

## Narzędzia

`tools/merge/*.py` (ścieżki zahardkodowane na `/home/user/...` do zmiany):
`cw.py` parser skryptów, `remap.py` neutralizacja prowincji, `merge.py` całe scalenie, `applyfix.py` patche bugfixes,
`check_lost.py` / `dups.py` / `validate.py` / `leftover.py` / `missions_overlap.py` kontrole.
