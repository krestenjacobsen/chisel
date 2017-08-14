Turbo p&aring; Terminalen - ssh To My Mac
22-03-2017


[TL;DR](http://en.wikipedia.org/wiki/Wikipedia:Too_long;_didn't_read) - Jeg har lavet et lille [script](), der tillader at man ssh'er tilbage til sin Mac uden at rode med routere, portforwarding ol. Alt det kræver er at Back To My Mac er aktiveret på begge maskiner.

<img src="http://static.logiskhave.dk.s3-website.eu-central-1.amazonaws.com/20170322-icloud-icon-ssh.png" alt="iCloud+SSH" style="width: 200px;">

Nogle gange har jeg brug for at kunne forbinde til min hjemme-mac og har hidtil gjort det via 'screen sharing' via 'Back To My Mac'. Det virker egentligt også fint, men som oftest har jeg slet ikke brug for den grafiske brugergrænseflade som skærmdeling giver mig. Jeg har bare brug for en terminal-adgang. Derfor ville jeg faktisl helst ssh'e mig ind til min maskine. Men jeg gider ikke rigtig rode med 'port forwarding' og åbne (mere) op til mit hjemmenetværk i min router. Så jeg kom til at tænke på, om man mon ikke kunne udnytte Back To My Mac-forbindelsen til dette formål. Og jo, efter 10 sekunder på [duckduckgo](https://duckduckgo.com/?q=Remote+SSH+using+Back+To+My+Mac) fandt jeg [svaret](http://onethingwell.org/post/27835796928/remote-ssh-bact-to-my-mac). :)

Herefter skrev jeg mit eget lille script, som håndterer det tunge arbejde med at identificere iCloud-id'et og forbinde korrekt.

Kør det sådan her:

    ./sshtomymac.sh [navn-på-mac]

eller bare:

    ./sshtomymac.sh

---

Scriptet:

<script src="https://gist.github.com/krestenjacobsen/6db8f8a9a9a48482a85c1b08ffdccbed.js"></script>