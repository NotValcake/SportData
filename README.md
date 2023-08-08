# SportData
Repo for my Database course final project.

# Obbiettivo del progetto

L'obbiettivo del progetto è quello di sviluppare un'applicazione che possa agevolare l'organizzazione e la gestione del capitale umano e materiale per le piccole associazioni sportive. Il problema della gestione delle risorse sorge dal fatto che questo tipo di organizzazioni tipicamente si trova a gestire gruppi relativamente numerosi di persone (dalle decine al centinaio di individui) e le complicate relazioni tra esse, disponendo di mezzi limitati a causa dell'elevato costo di strumenti più sofisticati. Bisogna inoltre tenere conto che chi si trova ad amministrare tali associazioni, lo fa come forma di volontariato, pertanto non dispone di conoscenze tecniche specifiche e non è propenso ad investire in questo genere di tecnologie, spesso sottovalutate e ritenute superflue.
La sfida è quindi creare un tool che semplifichi la gestione di associazioni sportive in modo intuitivo ed economico.

## Strumenti utilizzati

Per la realizzazione di un'applicazione web che rispondesse alle esigenze del progetto sono stati impiegati:

- DBMS: SQLite
- Linguaggi di programmazione: Python con framework Flask, HTML con Bootstrap
- DB Browser for SQLite come interfaccia grafica

# Requisiti della base di dati

## Raccolta dei requisiti

I requisiti della base di dati sono stati raccolti sulla base dell'esperienza personale, avendo osservato il funzionamento di una simile organizzazione. Per dettagliare meglio alcuni aspetti, tuttavia, sono state effettuate interviste che hanno permesso di definire in modo più preciso le informazioni rilevanti da conoscere per un atleta.

## Requisiti

Di fondamentale importanza per un'associazione sportiva sono, ovviamente, gli sportivi stessi. Possiamo distinguere due principali categorie di _atleta_: gli atleti seniores sono coloro che hanno raggiunto l'età adatta a giocare nella prima squadra, mentre gli atleti appartenenti alle categorie giovanili saranno chiamati _juniores_. Le due categorie di atleti hanno caratteristiche comuni come numero di cartellino (che identifica univocamente un giocatore), nome, cognome, numero di telefono, indirizzo e-mail, residenza, dati biometrici, ruolo e risultati ottenuti durante i test fisici. Per gli atleti juniores, inoltre, è importante indicare la categoria di appartenenza (under 18, under 10...), mentre i giocatori seniores possono essere in possesso di un contratto e quindi di uno stipendio da giocatore.
Il programma deve tenere traccia dei certificati di idoneità alla pratica sportiva(visite mediche) e del loro stato (valido o scaduto, data di scadenza, i certificati hanno validità annuale), inoltre, per semplificare la gestione degli infortuni, è importante segnalare l'eventuale stato di infortunio, in modo che il medico della squadra possa essere messo tempestivamente a conoscenza dello stato di salute degli atleti.
Oltre agli atleti ci sono altri membri dello staff di fondamentale importanza, è stato già citato il medico, ogni squadra poi ha un allenatore, anch'esso identificato dal numero di tessera, e di cui interessa sapere nome, cognome, numero di telefono, indirizzo e-mail e salario e la categoria allenata.
Infine abbiamo volontari e accompagnatori che supportano le altre figure del club, la differenza tra i due è che gli accompagnatori devono essere in possesso di un numero di tesseramento che li identifica, mentre i volontari no, i volontari saranno quindi identificati tramite codice fiscale, di entrambi poi si vuole sapere nome, cognome, numero di telefono e indirizzo e-mail.
L'attività delle associazioni si svolge attraverso eventi, che avranno un numero identificativo, una data, un'ora e un luogo, potranno essere di tre tipi: allenamento, partita o eventi sociali e l'applicazione dovrebbe permettere di registrare le presenze dei membri dell'associazione all'evento.
Infine l'associazione interagisce con altre aziende attraverso le sponsorizzazioni, ciascuna azienda sponsor sarà identificata dalla relativa partita IVA, nome, recapiti telefonici e e-mail, andrà registrata la data di inizio e di fine della sponsorizzazione.
