# The Vault — A Terminal Banking System

A modular Python banking application with bcrypt-secured authentication, a peer-to-peer transfer system, credit scoring, and a probabilistic investment engine — built entirely without external banking libraries or a database backend.

---

## Overview

The Vault is a terminal-based banking simulator that models the core operations of a retail bank: account creation, balance management, lending, and peer transfers. Every piece of financial state — balances, loan obligations, investment positions, credit scores, and transaction messages — is persisted across sessions using Python's `pickle` module, stored in a single binary file (`users.dat`).

The project is intentionally self-contained. There are no third-party financial APIs, no SQL database, and no web layer. The goal was to implement real banking logic — interest deduction, creditworthiness gating, transfer verification — using only Python's standard library plus `bcrypt` for password security.

---

## Architecture

```
the-vault/
├── Main.py              # Entry point — login/signup flow, main menu routing
├── Verification.py      # Authentication — sign-up, login, password change, bcrypt
├── Banking.py           # Financial engine — deposits, withdrawals, transfers, loans, hedge funds
├── Settings.py          # Account management — details, deletion, persistence (save/load)
├── Check_of_password.py # Utility script — proves passwords are stored as hashes, not plain text
└── users.dat            # Persistent binary store — all user state (auto-generated)
```

---

## Data Structure

All user data lives in a single in-memory dictionary, keyed by username, and serialized to `users.dat` on every state-changing operation. Each user entry is structured as:

```python
users[username] = [
    hashed_password,   # bcrypt hash (bytes)
    balance,           # float — current account balance
    [                  # account details list:
        name,          #   [0] display name
        age,           #   [1] age (integer)
        cibil_score,   #   [2] credit score (starts at 0, adjusts with loan behavior)
        loan,          #   [3] outstanding loan balance with interest pre-added
        hedge_fund     #   [4] amount currently invested in hedge fund
    ],
    messages           # list of strings — incoming transfer notifications
]
```

This flat structure means every module reads and writes from a consistent, predictable shape. Each function receives `users` and `name`, mutates the relevant slice, and returns the updated dictionary — which is then written back to disk by `Settings.save()`.

---

## Key Features

### bcrypt Authentication
Passwords are never stored in plain text. On sign-up, a unique salt is generated per user via `bcrypt.gensalt()` and the password is hashed with `bcrypt.hashpw()`. On every login and sensitive operation (withdrawal, transfer, loan, deletion), the entered password is re-verified against the stored hash using `bcrypt.checkpw()`. The `Check_of_password.py` script exists specifically to demonstrate this — dumping `users.dat` to the terminal shows only raw hash bytes, never readable passwords.

### Persistent Storage via Pickle
`Settings.save()` is called after every transaction that mutates state. The entire `users` dictionary is serialized to `users.dat` in binary format. On startup, `Main.py` deserializes it back. This means account balances, loan balances, investment positions, and message queues all survive between sessions with no database required.

### Hedge Fund Investment Engine
Users can deposit funds into a simulated investment vehicle. Each time a user logs in, `Banking.grow()` runs a random outcome against their active position using a weighted probability table:

| Roll (1–100) | Outcome | Change |
|---|---|---|
| 1 – 60 | Common Hike | +7% to +27% |
| 61 – 75 | Normal Dip | −1% to −30% |
| 76 – 85 | Moderate Hike | +27% to +47% |
| 86 – 90 | Major Dip | −30% to −50% |
| 91 – 95 | Big Hike | +47% to +70% |
| 96 – 100 | Ultra Hike | +70% to +100% |

The fund cannot go below zero — a floor is enforced on all dip calculations. Users can deposit into or withdraw from the fund at any time via a verified transaction.

### Credit System (Cibil Score & Loans)
Loan eligibility is gated by two conditions: no existing loan and a non-negative Cibil score. Eligible users can borrow up to **30% of their current balance**, with **10% interest pre-added** to the principal at the point of borrowing.

On every login, `Banking.deduct()` automatically charges **10% of the outstanding loan** as an installment payment. If the user cannot cover the installment, their Cibil score drops by 10 points, recording the default. Successful full repayment restores 10 Cibil points. A negative Cibil score permanently blocks future loan applications until the score recovers.

### Peer-to-Peer Transfers
`Banking.CashTransfer()` moves funds directly between two usernames. The flow requires:
1. The receiver's username must exist in `users`.
2. The transfer amount must be positive and within the sender's balance.
3. The sender must re-verify their password mid-transaction (a second `bcrypt.checkpw()` call).

On success, the transfer amount is deducted from the sender and credited to the receiver. A notification message is appended to the receiver's message queue (`users[receiver][3]`), which is displayed and cleared the next time the receiver logs in.

### Account Deletion Guardrails
An account can only be deleted if three conditions are simultaneously true: balance is zero, outstanding loan is zero, and hedge fund position is zero. This prevents users from abandoning accounts with pending financial obligations. Deletion removes the entry from the `users` dictionary entirely and saves the updated store to disk.

---

## Security

- **Passwords hashed with bcrypt** — unique salt per user, never stored as plain text.
- **Re-verification on sensitive actions** — withdrawals, deposits, transfers, loans, password changes, and account deletion each require a fresh password check before proceeding.
- **No credentials in source** — there are no hardcoded secrets. The only sensitive file is `users.dat`, which should be excluded from version control.

> **Note:** Add `users.dat` to your `.gitignore` before pushing. This file contains real user state including hashed passwords and financial data.

```
# .gitignore
users.dat
__pycache__/
*.pyc
.DS_Store
```

---

## Setup

**Prerequisites:** Python 3.9+

```bash
# 1. Clone the repo
git clone https://github.com/your-username/the-vault.git
cd the-vault

# 2. Install dependencies
pip install bcrypt

# 3. Initialize the data store
python -c "import pickle; open('users.dat','wb').write(pickle.dumps({}))"

# 4. Run
python Main.py
```

On first run, select **Sign Up** to create an account. `users.dat` will be created automatically if it does not exist.

To verify that passwords are stored securely and not readable in plain text, run:

```bash
python Check_of_password.py
```

---

## Module Reference

| File | Responsibility |
|---|---|
| `Main.py` | Top-level menu routing. Loads `users.dat` on startup. Delegates all logic to other modules. |
| `Verification.py` | Sign-up validation (age gate ≥18), bcrypt hashing, login, password change, transfer message delivery. |
| `Banking.py` | All financial operations: deposit, withdraw, transfer, hedge fund, loan application, loan deduction, repayment. |
| `Settings.py` | Account detail display, detail updates, account deletion (with balance/loan guard), `pickle` save utility. |
| `Check_of_password.py` | Development utility — prints raw contents of `users.dat` to demonstrate hashed storage. |

---

## Academic Context

This project was built as a school assignment. Certain technical choices — specifically the use of `pickle` for data persistence — were made to satisfy course requirements rather than as a production recommendation. At the time, SQL had not yet been covered in the curriculum. The Roadmap below reflects what a natural evolution of this project would look like outside of those constraints.

---

## Roadmap

- [ ] Replace `pickle` with SQLite for safer, queryable persistence
- [ ] Add a transaction history log per user
- [ ] Implement compound interest on loans (currently flat 10% per login)
- [ ] Add an admin mode to view system-wide balances and flag defaulted accounts
- [ ] Port to a Flask web interface with session management

---

## License

MIT
