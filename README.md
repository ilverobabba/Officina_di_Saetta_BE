# Officina di Saetta — Frontend

Interfaccia web per il configuratore di automobili **Officina di Saetta**, costruita con **Just DOM**, **Vite** e **Tailwind CSS + DaisyUI**.

---

## Tecnologie

| Tecnologia | Versione |
|---|---|
| Just DOM | ^2.1.0 |
| @just-dom/router | ^1.0.0 |
| @just-dom/signals | ^1.0.0 |
| @just-dom/lucide | ^1.1.0 |
| Vite | ^8.0 |
| Tailwind CSS | v4 |
| DaisyUI | ^5.5 |

---

## Struttura del progetto

```
Officina_di_Saetta_FE/
├── index.html
├── vite.config.js
├── package.json
├── .env.example
├── .env.local               # Variabili d'ambiente locali (non committare)
├── public/
│   ├── favicon.svg
│   └── icons.svg
└── src/
    ├── main.js              # Entry point — definizione delle route
    ├── jd.config.js         # Configurazione plugin Just DOM
    ├── api.js               # Client HTTP verso il backend
    ├── auth.js              # Gestione sessione utente (localStorage)
    ├── style.css
    ├── components/
    │   ├── delete-dialog.js       # Dialog di conferma eliminazione
    │   └── preventivo-form.js     # Form dati cliente nel configuratore
    ├── layouts/
    │   └── navbar-layout.js       # Layout con barra di navigazione
    └── pages/
        ├── home-page.js            # Homepage con catalogo modelli
        ├── modelli-page.js         # Lista modelli
        ├── modello-detail-page.js  # Dettaglio singolo modello
        ├── configura-scelta-page.js # Selezione modello da configurare
        ├── configura-page.js       # Configuratore multi-step
        ├── preventivi-page.js      # Lista preventivi
        ├── preventivo-page.js      # Dettaglio preventivo
        ├── login-page.js           # Pagina di login
        └── registrati-page.js      # Pagina di registrazione
```

---

## Prerequisiti

- Node.js 18+
- npm
- Backend attivo su `http://localhost:5001` (o URL configurato)

---

## Installazione

1. Entra nella cartella del progetto:
   ```bash
   cd Officina_di_Saetta_FE
   ```

2. Installa le dipendenze:
   ```bash
   npm install
   ```

3. Configura la variabile d'ambiente:
   ```bash
   cp .env.example .env.local
   ```
   Poi modifica `.env.local`:
   ```env
   VITE_API_URL=http://localhost:5001
   ```

---

## Avvio

```bash
npm run dev
```

L'app sarà disponibile su `http://localhost:5173` (porta default di Vite).

### Altri comandi

```bash
npm run build    # Build di produzione
npm run preview  # Anteprima della build produzione
```

---

## Routing

Le route sono definite in `src/main.js` e usano `@just-dom/router`:

| Path | Componente | Descrizione |
|------|-----------|-------------|
| `/` | `HomePage` | Catalogo modelli in evidenza |
| `/modelli` | `ModelliPage` | Lista completa dei modelli |
| `/modelli/:id` | `ModelloDetailPage` | Dettaglio modello con motorizzazione e optional |
| `/configura` | `ConfiguraSceltaPage` | Selezione del modello da configurare |
| `/configura/:id` | `ConfiguraPage` | Configuratore multi-step |
| `/preventivi` | `PreventiviPage` | Lista preventivi dell'utente |
| `/preventivi/:id` | `PreventivoPage` | Dettaglio preventivo |
| `/login` | `LoginPage` | Login |
| `/registrati` | `RegistratiPage` | Registrazione nuovo cliente |

Tutte le route sono racchiuse nel layout `NavbarLayout` che mostra la barra di navigazione con accesso rapido al profilo e al logout.

---

## Autenticazione

La sessione è gestita interamente nel browser tramite `localStorage`:

- **Token JWT** → salvato con chiave `officina_token`
- **Dati utente** → salvati in JSON con chiave `officina_user`

Le funzioni di utilità sono in `src/auth.js`:

```js
getUser()     // restituisce l'utente dalla sessione
setUser(user) // salva l'utente
isLoggedIn()  // controlla se l'utente è autenticato
isAdmin()     // controlla se il ruolo è "admin"
logout()      // rimuove token e dati utente
```

Il token viene incluso automaticamente in ogni richiesta API nell'header:
```
Authorization: Bearer <token>
```

---

## Client API (`src/api.js`)

Il file `api.js` centralizza tutte le chiamate al backend e normalizza i dati prima di restituirli al frontend. Le funzioni esportate sono:

**Autenticazione**
- `login(email, password)` — esegue il login e salva il token
- `register({ email, password, first_name, last_name, phone })` — registra un cliente
- `getMe()` — recupera il profilo dell'utente loggato

**Modelli**
- `getModelli()` — lista di tutti i modelli
- `getModello(id)` — dettaglio singolo modello

**Optional**
- `getAllOptional()` — lista di tutti gli optional
- `getOptionalDelModello(modelloId)` — optional di un modello specifico

**Configurazioni**
- `creaConfigurazione({ nome, modello_id, motorizzazione_id, optional_ids, totale })` — crea una configurazione

**Preventivi**
- `getPreventivi()` — lista preventivi (arricchita con i dati della configurazione)
- `getPreventivo(id)` — dettaglio preventivo
- `creaPreventivo({ ... })` — crea configurazione e genera preventivo in un'unica chiamata
- `aggiornaStatoPreventivo(id, stato)` — aggiorna stato (`inviato` / `accettato` / `rifiutato`)
- `eliminaPreventivo(id)` — elimina preventivo (solo admin)

---

## Variabili d'ambiente

| Variabile | Descrizione | Esempio |
|-----------|-------------|---------|
| `VITE_API_URL` | URL base del backend | `http://localhost:5001` |

> Vite espone solo le variabili con prefisso `VITE_` al codice client.