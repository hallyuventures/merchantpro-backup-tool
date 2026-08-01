# MerchantPro Backup Tool & K-Goodies Label Tool

Un set de instrumente Python pentru backup local al produselor MerchantPro, auditarea etichetelor și generarea, previzualizarea și tipărirea etichetelor K-Food și K-Beauty.

Proiectul este optimizat pentru imprimanta **Brother QL-600**, cu rolă continuă de **62 mm**.

## Funcționalități

### Backup MerchantPro

- citește exporturile Excel MerchantPro;
- descarcă imaginile produselor;
- extrage imaginile din descrierile HTML;
- salvează fiecare produs într-un folder separat;
- generează câte un fișier `product.json` pentru fiecare produs;
- validează datele și semnalează informațiile lipsă.

### Audit etichete

`generate_all_labels.py`:

- caută toate fișierele `product.json` din backup;
- încearcă să genereze o etichetă pentru fiecare produs;
- creează preview-uri în folderul `_labels`;
- generează rapoarte de erori și avertismente.

Acest script este destinat auditului tehnic în masă. Etichetele finale pentru tipărire se configurează produs cu produs în aplicația grafică.

### Aplicația de etichetare

`label_app.py` oferă:

- încărcarea produsului după ID;
- afișarea denumirii și furnizorului;
- selectarea operatorului responsabil/importatorului;
- selectarea distribuitorului din România;
- preselectarea distribuitorului pe baza furnizorului;
- salvarea asocierilor în `data/product_operators.json`;
- adăugarea operatorilor și distribuitorilor din interfață;
- generarea preview-ului;
- tipărirea directă pe Brother QL-600.

### Dimensionarea etichetei

Sunt disponibile două moduri:

#### Font fix → lungime automată

Utilizatorul stabilește dimensiunile fonturilor, iar aplicația calculează automat lungimea etichetei.

#### Lungime fixă → font automat

Utilizatorul stabilește lungimea fizică a etichetei, iar aplicația caută automat cea mai mare dimensiune de font care permite încadrarea completă a conținutului.

Motorul gestionează dinamic:

- titluri și cantități lungi;
- ingrediente și alergeni;
- valori nutriționale;
- mod de preparare;
- mod de utilizare;
- informații suplimentare;
- operator/importator și distribuitor;
- wrapping în tabelul nutrițional.

## Cerințe

- Windows 10 sau Windows 11 pentru tipărirea directă;
- Python 3.14 sau o versiune compatibilă;
- driver instalat pentru Brother QL-600;
- rolă continuă de 62 mm.

Instalarea dependențelor:

```cmd
py -m pip install -r requirements.txt
```

Verificarea dependențelor:

```cmd
py -m pip check
```

## Pornirea aplicației

Din rădăcina proiectului:

```cmd
py .\label_app.py
```

Flux recomandat:

1. selectează folderul de backup;
2. introdu ID-ul produsului;
3. verifică operatorul/importatorul;
4. verifică distribuitorul;
5. salvează asocierea;
6. selectează modul de dimensionare;
7. generează preview-ul;
8. tipărește eticheta.

Înainte de tipărire trebuie generat un preview. Butonul de tipărire folosește ultimul PNG generat pentru produsul curent.

## Generarea auditului pentru toate produsele

```cmd
py .\generate_all_labels.py
```

Scriptul solicită selectarea folderului de backup și generează preview-urile în folderul `_labels`.

Pot fi create:

```text
label_errors.txt
label_warnings.txt
```

## Backup MerchantPro

Aplicația principală de backup se rulează astfel:

```cmd
py .\src\app.py
```

Backup-ul rezultat conține foldere individuale pentru produse și fișiere `product.json`.

Folderele de backup sunt ignorate de Git și nu trebuie publicate în repository.

## Date juridice

Operatorii, importatorii și distribuitorii sunt salvați în:

```text
data/operators.json
```

Asocierile dintre produse și operatori/distribuitori sunt salvate în:

```text
data/product_operators.json
```

La tipărire:

- dacă operatorul/importatorul și distribuitorul sunt firme diferite, apar separat;
- dacă este aceeași firmă, aplicația generează o formulare combinată.

Datele trebuie verificate pe ambalaj înainte de tipărirea etichetei finale.

## Structura proiectului

```text
merchantpro-backup-tool/
├── data/
│   ├── operators.json
│   └── product_operators.json
├── docs/
├── output/
├── sample_data/
│   └── product.json
├── src/
│   ├── label/
│   │   ├── blocks/
│   │   ├── context.py
│   │   ├── engine.py
│   │   ├── layout.py
│   │   ├── nutrition_parser.py
│   │   ├── printer.py
│   │   ├── style.py
│   │   └── windows_printer.py
│   ├── app.py
│   ├── operator_registry.py
│   ├── product.py
│   ├── product_factory.py
│   ├── product_json_loader.py
│   ├── product_operator_registry.py
│   ├── product_serializer.py
│   └── product_validator.py
├── tests/
├── generate_all_labels.py
├── label_app.py
├── requirements.txt
└── README.md
```

## Teste

Testele se rulează din rădăcina proiectului ca module:

```cmd
py -m tests.test_label_engine
py -m tests.test_nutrition_parser
py -m tests.test_operator_registry
py -m tests.test_product_operator_registry
```

Testul de tipărire directă necesită calea către un PNG existent:

```cmd
py -m tests.test_direct_print "backup\_label_preview\424.png"
```

Atenție: această comandă trimite efectiv eticheta către imprimantă.

## Imprimantă și dimensiuni

Configurarea curentă este optimizată pentru:

```text
Brother QL-600
Rolă continuă: 62 mm
DPI: 300
Zonă imprimabilă nominală: aproximativ 59 mm
```

Lungimea selectată în aplicație reprezintă lungimea fizică totală a etichetei tăiate.

Diferențe de aproximativ 1 mm pot apărea din toleranța mecanismului, driverului și măsurării manuale.

## Limitări

- tipărirea directă folosește `pywin32` și este disponibilă numai pe Windows;
- numele imprimantei este configurat implicit ca `Brother QL-600`;
- datele juridice trebuie verificate înainte de utilizarea comercială;
- auditul în masă nu înlocuiește verificarea individuală a etichetei pe ambalaj.

## Versiune

### v1.0.0

Prima versiune stabilă include:

- backup complet produse și imagini;
- `product.json` per produs;
- audit în masă;
- interfață pentru etichete;
- registre pentru operatori și distribuitori;
- font fix cu lungime automată;
- lungime fixă cu font automat;
- tabel nutrițional adaptiv;
- preview;
- tipărire directă pe Brother QL-600;
- teste și structură de proiect curățată.

## Licență

Licența nu este încă definită. Adaugă un fișier `LICENSE` înainte de distribuirea publică, dacă proiectul urmează să fie reutilizat de terți.
