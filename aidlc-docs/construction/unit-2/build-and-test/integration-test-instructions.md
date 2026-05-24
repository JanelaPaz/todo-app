# Unit 2 — Integration Test Instructions

Six `curl`-based scenarios that exercise `reminder_at` end-to-end against a
running backend. Each scenario is independent and can be run in any order.

## Prerequisites

1. Backend running on `http://localhost:8000` (`uvicorn main:app --reload`).
2. `jq` for response inspection (optional but recommended).
3. A cookie jar to keep the auth session.

```bash
COOKIES=$(mktemp)
BASE=http://localhost:8000/api
EMAIL="u2-$(date +%s)@example.com"
USER="u2_$(date +%s)"
PASS="testpassword123"

curl -s -c "$COOKIES" -H 'Content-Type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"username\":\"$USER\",\"password\":\"$PASS\",\"password_confirm\":\"$PASS\"}" \
  "$BASE/auth/register" >/dev/null
```

## Scenario 1 — Create todo with reminder_at

```bash
curl -s -b "$COOKIES" -H 'Content-Type: application/json' \
  -d '{"title":"Pay invoice","reminder_at":"2026-12-01T09:00:00Z"}' \
  "$BASE/todos"
```

**Expect:** `201` and a JSON body where `reminder_at` is preserved.

## Scenario 2 — Create todo without reminder_at

```bash
curl -s -b "$COOKIES" -H 'Content-Type: application/json' \
  -d '{"title":"No reminder"}' \
  "$BASE/todos"
```

**Expect:** `201`, response contains `"reminder_at": null`.

## Scenario 3 — Reject invalid reminder_at

```bash
curl -s -o /dev/null -w '%{http_code}\n' -b "$COOKIES" -H 'Content-Type: application/json' \
  -d '{"title":"Bad reminder","reminder_at":"not-a-date"}' \
  "$BASE/todos"
```

**Expect:** `422`.

## Scenario 4 — Update reminder_at to a new value

Substitute `$ID` with the id returned by Scenario 1.

```bash
curl -s -X PUT -b "$COOKIES" -H 'Content-Type: application/json' \
  -d '{"reminder_at":"2027-01-15T12:00:00+02:00"}' \
  "$BASE/todos/$ID"
```

**Expect:** `200`, `reminder_at` reflects the new offset value.

## Scenario 5 — Clear reminder_at via explicit null

```bash
curl -s -X PUT -b "$COOKIES" -H 'Content-Type: application/json' \
  -d '{"reminder_at":null}' \
  "$BASE/todos/$ID"
```

**Expect:** `200`, `reminder_at` is `null` in the response.

## Scenario 6 — Untouched field is preserved

```bash
curl -s -X PUT -b "$COOKIES" -H 'Content-Type: application/json' \
  -d '{"title":"New title only"}' \
  "$BASE/todos/$ID"
```

**Expect:** `200`, `title` is updated, `reminder_at` retains the value set in
the previous scenario (or `null` if Scenario 5 just ran).

## Cleanup

```bash
rm -f "$COOKIES"
```
