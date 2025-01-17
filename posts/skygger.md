Skygger p&aring; billeder
05-10-2013


**tl**;**dr** - Jeg bruger ImageMagick via kommandolinien til at lægge skygger på mine billeder i stedet for et dyrt billedbehandlingsprogram.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

Jeg vil gerne have skygge på de billeder, der ikke fylder hele sidens bredde her på loggen for lige som at ramme dem lidt ind. Men jeg vil meget nødigt købe et dyrt billedbehandlingsprogram til kun det. I den forbindelse var jeg derfor i stedet forbi gratis og opensource software, men fælles for dem alle er, at de ikke kun løser mit problem, men installerer et fuldt billedbehandlingsprogram, hvilket er en anelse overkill lige her.

I stedet faldt jeg i min søgen over ImageMagick, som jeg egentligt kun har tænkt på som serversoftware til at beskære og ændre størrelse på billeder automatisk. Men netop muligheden for at automatisere handlinger er genial - og da jeg så også fik googlet mig frem til hvordan jeg kunne bruge det til at lægge skygger på med passede det jo som fod i hose.

### Installation ###

ImageMagick kan godt virke forvirrende. Og det er det. Installationen kan dog gøres nem ved at hente en installationspakke fra [Cactuslab](http://cactuslab.com/imagemagick/) eller hvis man har Mac Ports installeret

    sudo port install ImageMagick

### Brug ###

Når man skal lægge skygge på en billede gør man det via Terminal.app således:

    convert billede_uden_skygge.png \( +clone -background black -shadow 80x20+0+15 \) +swap -background transparent -layers merge +repage billede_med_skygge.png

Det vil tage "billede_uden_skygge.png" lægge skygge på og gemme det som "billede_med_skygge.png". Nemt og smart (og scriptbart).

Hvis skyggerne skal fjernes igen kan ImageMagick også klare det. Bare kør nedenstående mod dit billede med skygge:

    convert billede_med_skygge.png -crop +40+25 -crop -40-55 billede_uden_skygge.png

### Alternativ ###

Vil man bare undgå skygger på sine screenshots kan man slå dem fra ved at fyre følgende af i teminal:

    defaults write com.apple.screencapture disable-shadow -bool true

Og derefter:

    killall SystemUIServer
