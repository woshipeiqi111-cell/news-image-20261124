# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/woshipeiqi111-cell/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/woshipeiqi111-cell/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One-page newspaper front page summarising the world news of
**Tuesday, 24 November 2026** — built for the make.fun competition
`news-image-20261124`.

## What it shows

Six stories that defined the day, plus a markets panel and an "also today"
strip:

1. **Huang is back at Nvidia** — Nvidia's board reinstates Jensen Huang as
   CEO after pressure from President Trump; shares jump 31% in a day, their
   best since 2003, and the S&P 500 gains 4.7%.
2. **Ukraine sinks Russian warship off Libya** — seven sea drones sink the
   corvette *Merkury* in Benghazi harbour; a weapons cargo ship is also hit,
   Kyiv says.
3. **Iran claims three tankers hit mines in Hormuz** — Tehran says the
   tankers caught fire; the claim is unverified and the US has not responded.
4. **China names Shenzhou-24 crew** — Tang Hongbo, Wu Yi and Pakistan's
   Muhammad Zeeshan Ali, the first foreign astronaut to visit Tiangong.
   Launch: 25 November, 08:18 Beijing time.
5. **Israeli strike kills Hamas security chief** — Naeem Abu Nahel and six
   others killed in Gaza City, medics and police say.
6. **Two US states sue Musk over Grok images** — Virginia and Oregon accuse
   SpaceX of stripping safeguards from Grok's image tool.

Markets panel: S&P 500 +4.7%, Nasdaq +6.4%, Nvidia +31%. Also today:
Zaporizhzhia strike kills 2 and wounds 40; EU 22nd sanctions package on
Russia; Spain amnesties Puigdemont.

## How it was made

The poster is composed offline by `build_poster.py` from six editorial
illustrations (in `assets/`, generated without text) plus real rendered text,
so every word on the page is crisp and exactly as written. The finished
1024×1024 PNG is baked into this repository as `entry.png`.

## Run

```bash
# Node 22, no dependencies, no network
node main.ts        # writes /output/entry.png (byte-identical every run)
```

## Sources

Reuters, AP, WSJ, Al Jazeera, Xinhua, SCMP — all facts reported on
24 November 2026. Unverified claims are labelled as claims on the page
(e.g. the Hormuz tanker incident). See `RESULT.md` for the per-fact source
list.

## License

MIT — see `LICENSE`.
