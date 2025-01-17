Hvad er SHA-1 (og hvorfor er det vigtigt)?
04-03-2017
https://www.keycdn.com/support/sha1-vs-sha256/

![SHATTERED](/static/20170306_shattered.png)
> SHA, which stands for secure hash algorithm, is a cryptographic hashing algorithm used to determine the integrity of a particular piece of data. Variations of this algorithm are often used by SSL certificate authorities to sign certificates. This algorithm help ensures that your website’s data is not modified or tampered with. It does so by generating **unique hash values** from any particular file / variation of a file. Based on these hash values, it can be determined whether or not the file has been altered by comparing the **expected hash value to the hash value received**.

Eller: For at afgøre om en fil er den man forventer, sammenligner man den unikke hashværdi af filen man har hentet, med den oplyste hashværdi fra afsenderen.

Balladen opstår så, når nogen [genererer identiske hashværdier for forskellige filer](https://shattered.io). Så kan man nemlig ikke længere stole på, at dokumentet[^1] man modtager er det samme som det afsenderen sendte...

[^1]: Et dokument skal i denne sammenhæng forstås bredt, som en hvilken som helst sekvens af data; eks. en hjemmeside.
