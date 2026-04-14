# Kulturbiljett API

Base URL: `https://kulturbiljetter.se/api/v3`
Auth: `Authorization: Token <KULTURBILJETT_API_KEY>`

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/events/` | List all events (IDs only) |
| GET | `/events/{event_id}` | Full details for one event |

---

## `GET /events/`

Returns a dict keyed by index (`"0"`, `"1"`, ...). Each item:

| Field | Type | Description |
|---|---|---|
| `event_id` | int | Use to fetch details |
| `organizer_id` | int | ID of the organizer |
| `ETag` | str | Fingerprint for caching (optional to use) |

The list endpoint does **not** return names — you must call `/events/{event_id}` for titles, descriptions, etc.

---

## `GET /events/{event_id}`

### Top-level fields

| Field | Type | Description |
|---|---|---|
| `title` | str | Event name |
| `presentation_short` | str (HTML) | Short description |
| `presentation_long` | str (HTML) | Long description |
| `unixtime_release` | int | When event was published (unix seconds) |
| `price_min` | str | Cheapest ticket in SEK (e.g. `"130.00"`) |
| `price_max` | str | Most expensive ticket in SEK |
| `organizer` | dict | See **organizer** below |
| `images` | dict | Index-keyed URLs (`{"0": "...", "1": "..."}`) |
| `trailers` | dict | Index-keyed video embed URLs |
| `dates` | dict | Index-keyed showings — see **dates** below |
| `locations` | dict | Keyed by `location_id` — see **locations** below |
| `url_checkout` | str | Main buy-tickets link |
| `url_event_page` | str | Public event page |
| `url_organizer_serp` | str | Organizer's listing page |

### `organizer`

| Field | Type | Description |
|---|---|---|
| `organizer_id` | int | |
| `name` | str | Organizer name |
| `logo` | str | Logo image URL |

### `dates.<n>`

One entry per showing/date.

| Field | Type | Description |
|---|---|---|
| `date_id` | int | Unique ID for this showing |
| `location_id` | int | Key into `locations` |
| `unixtime_open` | int | When ticket sales open |
| `unixtime_start` | int | When event starts |
| `date_only` | bool | If true, only the date is meaningful (no time) |
| `url_checkout` | str | Buy link for this specific date |
| `ticket_amount` | int | Total tickets |
| `ticket_available` | int | Tickets still for sale |

### `locations.<location_id>`

| Field | Type | Description |
|---|---|---|
| `location_id` | int | |
| `name` | str | Venue name |
| `street` | str | Street address |
| `vicinity` | str | Neighbourhood / area |
| `city` | str | City |

---

## Example: linking dates to locations

```python
for d in event["dates"].values():
    loc = event["locations"][str(d["location_id"])]
    print(f"{d['unixtime_start']} @ {loc['name']}, {loc['city']}")
```
