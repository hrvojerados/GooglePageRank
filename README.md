# GooglePageRank
## Demonstracija - Vikidia stranice
*Vikidia* je web sjedište nalik na *Wikipediu*, ali namijenjena djeci od 8 do 13 godina. Koristimo ju za demonstraciju jer ima raznovrsnih i dobro linkovima povezanih članaka,
ali za je razliku od Wikipedije dovoljno mala za brzo pretraživanje primitivnim crawlerom.
### Priprema
Online Vikidia koristi metode zaštite od pretraživanja crawlerima pa se ne može jednostavno iskoristiti za demonstraciju. Zato koristimo vlastitu kopiju postavljenu na lokalni server pomoću Kiwixa koji možemo instalirati pomoću: `sudo apt install kiwix-tools` ili drugih package managera.

Skinuti `.zim` sliku Vikidije s https://download.kiwix.org/zim/vikidia. Korištena je verzija `vikidia_en_all_maxi_2023-09.zim`. Moguće je pokrenuti druge verzije (valjda) uz promjenu `BASE_URL` u wiki_crawler.py

Pokrenuti kiwix server: `kiwix-serve -p 8080 *.zim`. Sada se može pristupiti Vikidia stranicama offline na localhost:8080.
### Pokretanje
Pokrenuti `python wiki_crawler3.py dat_veze.txt dat_riječi.txt`. Crawler prolazi po stranicama i sprema veze (listu susjedstva) među stranicama u dat_veze.txt i ključne riječi za svaku stranicu u dat_riječi.txt. Ovo je prilično neskalabilno rješenje, ali svrha mu je samo demonstrirati što PageRank radi i njegov odnos s personalizacijskim vektorom.
## Demonstracija - mini web
Mini web se sastoji od nekoliko malih rucno napravljenih offline stranica. Ideja je pokazati prednost korištenja PageRanka nad čistim preferencijskim vektorom. 