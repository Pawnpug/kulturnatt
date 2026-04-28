# swipe algo

## basic check måste stämma för att gå vidare
* ålderspannet stämmer överens för båda
* kön
* visa ej blockade användare

## poängsättning för swipealgo, per matchande attribut
1. event = 80
2. låtar/filmer = 10 
3. artister / regisörer 7 
4. genre (musik/film) 5
poäng sätts alltid mellan två personer, aldrig ett fast
visas sorterat på poäng, högst först, lägst sist

## redan visade profiler
* sätt flagga för att profiler har visats

## nya användare
* kräv minst en kategori ifylld
* för att matcha krävs detta
* ålder, kön, namn

## när körs algon
* vid sparning av profil
* ändrad event-tab sen gå till annan tab

## swipeat nej-lista (nej och unmatchade)
* en separat soreterad lista
* frågar användaren om de vill se
* samma swipeAlgo på nej-lista
* triggas när användaren väljer att visa den / om användaren själv ändrar inställningar

## best-match highlight
* baseras på hur många delade, kategori / totalt score 

## sätt att få ner hur mycket resurser denna rankning kräver
* cronjobb fungerar ej, för långsamt och onödigt om ingen har gjort ändringar
* kalkylera endast om på: den user som ändrar, och de users som har denne i sin lista sen tidigare (går igenom alla basic checks)