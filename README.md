# data_exploration_project 
Descriere generala: Acest proiect imbina trei seturi de date provenind din surse diferite (facebook, google si website), care contin infomatii despre companii. Scopul este de a curata si standardiza datele, de a folosi potrivirea fuzzy pentru numele companiilor si de a genera un set final de date cu informatii imbinate si curatate 

Pasii urmariti 
1) Citireq fisierelor CSV:
   Am citit datele din cele trei surse diferite: Facebook, Google si Website
2) Curatarea si standardizarea numelor companiilor :
  Am creat o functie pentru a standardiza numele companiilor, transformand toate numele in litere mici si eliminand spatiile suplimentare
3) Potrivirea fuzzy a numelor companiilor
  Am folosit fuzzywuzzy pentru  potrivi numele similare ale companiilor din diferite surse. Aceasta metoda ne a ajutat sa gasim companiile care au mici variatii in scriere intre seturile de date
4) Imbinarea seturilor de date:
   Am imbinat datele folosind numele companiilor care s-au potrivit in mod fuzzy intre sursele de date, generand un set complet de date
5) Rezolvarea conflictelor
   Pentru datele conflictuale, cum ar fi numerele de telefon, am implementat o functie de rezolvare care selecteaza valoarea cea mai frecventa dintre cele disponibile
6) Curatarea Datelor
   Am eliminat coloanele redundante si care nu mai erau necesare dupa imbinare
7) Salvarea datelor finale:
   Setul final de date a fost salvat intr-un fisier CSV

   STRUCTURA FISIERELOR
   data_exploration.py: Scriptul Python care implementeaza procesul de curatare, imbinare si rezolvare a conflictelor
   final_merged_dataset.csv: Setul de date generat, dupa ce au fost imbinate datele din cele trei surse, inainte de curatare finala
   final_merged_cleaned_dataset.csv: Setul de date final curatat,fara coloane redundante 
