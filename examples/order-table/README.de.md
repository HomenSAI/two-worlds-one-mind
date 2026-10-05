# Durchgerechnetes Beispiel: von einem Stapel Auftragsbestätigungen zu einer geprüften Tabelle

[Inhalt](../../README.de.md) · [English](README.md) · [Praxisleitfaden](../../book/de/08-field-guide.md)

**Worum es geht.** Ein vollständiger Durchgang durch die Checklisten des
[Praxisleitfadens](../../book/de/08-field-guide.md): Absichtskarte, Randbedingungen, Definition von
„fertig“, Vorgehen, ein Fehlschlag, die Korrektur, die Prüfung und das Fazit. Es ist ein
**Lehrbeispiel**. Es ist kein Fall aus dem Werdegang des Autors und **kein Beleg für
[EXP-001](../../experiments/EXP-001.de.md)** (den lokalen Inferenzserver) oder für das geplante
Archiv-Experiment EXP-003.

**Synthetische Daten.** Die zwölf Dateien in [`data/`](data/) sind für dieses Beispiel erfunden. Sie
enthalten keine echten Aufträge, Kunden, Verträge oder personenbezogenen Daten, und jede sagt das in ihrer
ersten Zeile. (Die Dateien sind englisch beschriftet, mit einer deutschen Variante der Bezeichnungen —
wie in gemischten Archiven üblich.) Jedes Ergebnis unten wurde durch tatsächliches Ausführen der Skripte
in diesem Ordner erzeugt (Python 3, nur Standardbibliothek).

Selbst ausführen, vom Hauptverzeichnis des Repositorys aus:

```bash
python3 examples/order-table/run_example.py
```

## 1. Die Aufgabe

Eine kleine Firma hat einen Ordner mit Textdateien, eine pro Auftragsbestätigung. Ein Kollege braucht eine
Tabelle: Auftragsnummer, Jahr, Betrag und Währung. Von Hand dauert das einen Nachmittag und lädt zu
Tippfehlern ein, deshalb wird die Arbeit einem Skript übergeben (von einem Menschen geschrieben oder von einem
KI-Assistenten — die Methode ist dieselbe).

## 2. Die ausgefüllte Absichtskarte

```text
ABSICHTSKARTE
-------------
Was will ich?                  Eine Tabelle mit einer Zeile pro Auftragsdatei: Auftragsnummer, Jahr, Betrag, Währung.
Warum?                         Der Kollege kann die Aufträge sortieren und summieren, ohne 12 Dateien zu öffnen.
Für wen?                       Einen Kollegen, der die Zahlen in einem Bericht verwendet.
Wie sieht „fertig“ aus?        check_result.py meldet PASS: jede Datei einmal; jede Zelle gleich dem Lösungsschlüssel;
                               keine geratenen Werte; die Summe der bestätigten EUR-Beträge stimmt.
Was darf NICHT passieren?      Eine falsche Zahl, die richtig aussieht. Ein stilles Raten. Währungen umrechnen.
Was weiß ich schon?            Die Dateien sind Text. Bezeichnungen wechseln („Total“, „Gesamtbetrag“). Zahlenformate
                               unterscheiden sich zwischen den Dateien (12,450.00 und 8.900,50 und 3 200).
Was ist unsicher?              Welche Formate wirklich vorkommen; was zu tun ist, wenn eine Zahl zwei Lesarten hat.
Wie werde ich es prüfen?       Mit einem von Hand aus den 12 Dateien erstellten Lösungsschlüssel (expected.csv) und
                               einem Skript, das die Tabelle damit vergleicht. Ich kann alle 12 Dateien selbst lesen.
```

## 3. Randbedingungen und Definition von „fertig“

- **Randbedingung:** Die Daten bleiben auf diesem Rechner; nichts wird irgendwohin gesendet. (Die Skripte
  nutzen kein Netzwerk und keine externen Pakete.)
- **Randbedingung:** Beträge behalten ihre eigene Währung; keine Umrechnung.
- **Randbedingung:** Ist ein Wert nicht sicher, bleibt die Zelle leer, und die Zeile wird mit `review` und
  einem Grund markiert. Ein Mensch entscheidet; das Skript rät nicht.

Die Abnahmekriterien stehen in [`check_result.py`](check_result.py) und wurden vor der Extraktion geschrieben:

| ID | Kriterium |
|----|-----------|
| C1 | Jede Eingabedatei erscheint genau einmal in der Tabelle. |
| C2 | Ein nicht sicherer Wert wird nie geraten (leere Zelle, Status `review`). |
| C3 | Jede Zelle entspricht dem Lösungsschlüssel [`expected.csv`](expected.csv), einschließlich der Frage, welche Zeilen geprüft werden müssen. |
| C4 | Die Summe der bestätigten EUR-Beträge entspricht der Summe des Schlüssels (81.452,60 EUR). |

## 4. Vorgehen

1. Alle zwölf Dateien lesen und den Lösungsschlüssel von Hand schreiben (`expected.csv`). Vier Dateien lassen
   sich nicht sicher auflösen: `order-004` und `order-010` (ein Betrag wie `1.250` oder `7.500` kann 1,25
   oder 1.250 bedeuten — und 7,5 oder 7.500), `order-005` (noch kein Betrag) und `order-012` (das Datum
   `14.3.22` hat ein zweistelliges Jahr).
2. Die Abnahmeprüfung schreiben (`check_result.py`).
3. Die erste Version der Extraktion ([`extract_v1.py`](extract_v1.py)) schreiben und ausführen.

## 5. Der Fehlschlag

Versuch 1 ist absichtlich die Art schnelles Skript, die man als Erstes bekommt. Sein Ergebnis, kopiert aus
[`results/check_v1.txt`](results/check_v1.txt):

```text
C3 order-002.txt: amount = '8.9005', expected '8900.50'
C2 order-004.txt: amount = '1.25', expected ''
C2 order-004.txt: status = 'ok', expected 'review'
C2 order-005.txt: status = 'ok', expected 'review'
C3 order-008.txt: amount = '45.0', expected '45000.00'
C3 order-009.txt: currency = '', expected 'JPY'
C2 order-010.txt: amount = '7.5', expected ''
C3 order-011.txt: amount = '210.0', expected '2.10'
C2 order-012.txt: status = 'ok', expected 'review'
C4 sum of confirmed EUR: 27827.6505 vs key 81452.60
RESULT: FAIL (18 failure(s))
```

(Die vollständige Datei listet alle 18 Zeilen.) Sehen Sie, was für Fehler das sind. Das Skript ist nicht
abgestürzt. Es hat eine ordentliche Tabelle erzeugt, in der aus dem deutschen Zahlenformat eine falsche Zahl
wurde (8.900,50 → 8.9005) und in der mehrdeutige oder fehlende Werte zu selbstsicheren Zahlen wurden. Das
ist die gefährliche Art von Fehler: Er sieht aus wie Erfolg. Erst die Prüfung gegen den Schlüssel zeigt ihn.

## 6. Die Korrektur

[`extract_v2.py`](extract_v2.py) ändert den Ansatz, nicht nur einen regulären Ausdruck:

- Zahlenformate werden nach ausdrücklichen Regeln gelesen (Tausender- und Dezimaltrennzeichen in allen
  vorkommenden Formaten);
- der Betrag wird aus der Summenzeile mit seinem Währungskennzeichen genommen, und der Bruttobetrag wird dem
  Nettobetrag vorgezogen;
- eine Zahl mit zwei möglichen Lesarten, ein fehlender Betrag oder ein zweistelliges Jahr wird **nicht
  geraten**: Die Zelle bleibt leer, und die Zeile erhält `review` und einen Grund.

## 7. Prüfung

Ergebnis von `python3 examples/order-table/run_example.py` (auch in [`results/`](results/) gespeichert):

```text
--- attempt 1: RESULT: FAIL (18 failure(s))
--- attempt 2: RESULT: PASS (0 failure(s))
EXAMPLE OK
```

Die endgültige Tabelle ist [`results/table_v2.csv`](results/table_v2.csv): Acht Zeilen sind bestätigt, vier
Zeilen sind mit `review` und ihren Gründen markiert.

## 8. Fazit

- Die Methode hat die Arbeit getan, nicht das Skript: **Ein Lösungsschlüssel und schriftliche Kriterien
  existierten vor dem Code**, deshalb konnte das erste, falsche Ergebnis als falsch erkannt werden.
- „Fertig“ hieß nicht „das Skript lief“. Es hieß „die Prüfung ist bestanden“, und die Prüfung enthielt die
  Frage *Was darf nicht passieren* aus der Absichtskarte.
- Vier Zeilen gehen an einen Menschen zurück. Sie zurückzugeben ist für diese Zeilen das richtige Ergebnis,
  kein Mangel.
- **Grenzen dieses Beispiels.** Zwölf erfundene Dateien, ein vom Autor gewählter Satz von Formaten, ein
  Schlüssel, der von derselben Person erstellt wurde, die die Prüfung schrieb. Die Prüfung beweist, dass die
  Skripte *diesen* Schlüssel an *diesen* Daten treffen; sie beweist nicht, dass das Skript ein echtes Archiv
  bewältigen würde. Dafür bräuchte man echte Stichproben, ein zweites Augenpaar und einen größeren Test.
