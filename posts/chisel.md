Chisel
25-09-2013


**tl**;**dr** - Jeg har skiftet det underliggende system, jeg bygger denne side med, ud fra Octopress til Chisel og er glad for det.

![Screenshot af Terminal.app](/static/20130927_screenshot.png "Terminal.app afvikler Chisel")

I min søgen efter det ultimative blogsetup, er jeg nu faldet over [Chisel][], som er endnu en "static site generator" lige som mine tidligere sider .

Der var et par ting, der tiltalte mig ved Chisel og især følgende betyder meget for valget om at gå væk fra [Octopress][]. Chisel er nemlig:

- Skrevet i python, som jeg nogenlunde forstår.   
- Relativt overskuelig kode ([113 linier][chisel-kode])   
- Har et minimum afhængigheder, hvilket gør Chisel mobil[^1].
- Parser markdown, som jeg elsker at skrive i.

Siden her er dog ikke en "bare bones" chisel, men [Chyetanya Kuntés udvidelse][ckunte-chisel] på 169 linier python-kode. Det er der nogle fornuftige tilføjelser, som jeg synes var værd at tage med[^2] - og derudover havde han lavet et fint layout, som jeg kunne arbejde ud fra.

For at få det til at spille har jeg dog inden go-live måtte kigge på det evigt frygtede datoformat -- for jeg gider ikke lave en fin side blot for ikke at kunne generere danske datoer.[^3]

### Danske datoer

For at få danske datoer til at virke, måtte jeg dels lave denne rettelse i chisel.py:

    TIME_FORMAT = "%B %d, %Y"

*Engelsk format (eks. May 22, 2013)*

    TIME_FORMAT = "%d. %B, %Y"

*Dansk format (eks. 22. May, 2013)*

Men rykker jo ligesom bare rundt på formatet og ændrer ikke sproget. For at gøre det, skal man gøre chisel.py-scriptet opmærksomt på, at man vil afvige fra standardsproget, engelsk, ved at bruge pythons indbyggede lokalisations metode "locale" således:

    import locale
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")

 *Dansk format og dansk sprog (eks. 22. maj, 2013)*

Hvis man som jeg blot skrev "da_DK" i sproget virker det fint på Mac, men giver en fejl på Linux. Linux (Debian i mit tilfælde) er noget mere kræsent og skal have den præcise angivelse; altså med den korrekte ".UTF-8" endelse på. Det krævede lidt grå hår, før jeg fandt [en tråd på Stack Overflow][stack-overflow], som bragte mig i den rigtige retning -- jeg er som bekendt ikke programmør. ;-)

### Update
D. 28/9-2013 - [MathJax][] er fjernet for at gøre siden hurtigere; jeg skriver ikke matematiske formler, så det tjener ingen funktion.

[^1]: Jeg har fået nøjagtigt samme script til at køre på Linux og Mac, hvilket er vigtigt for mig, da jeg gerne vil kunne generere og hoste sitet på min Linux host og udvikle på det på mine Macs.  

[^2]: Eks. RSS og kortere URL'er, men der er også andre ting med. Se evt. mere på [ckunte.net/log][ckunte].

[^3]: En ting der i øvrigt også afholder mig fra en masse hostede blog-systemer som eksempelvis [Tumblr][].

[Chisel]: https://github.com/dz/chisel
[chisel-kode]: https://github.com/dz/chisel/blob/master/chisel.py
[ckunte-chisel]: https://github.com/ckunte/chisel/blob/master/chisel.py
[Octopress]: http://octopress.org
[Tumblr]: http://www.tumblr.com
[stack-overflow]: http://stackoverflow.com/questions/1259971/os-locale-support-for-use-in-python
[ckunte]: http://ckunte.net/log/2012/chisel
[MathJax]: http://www.mathjax.org
