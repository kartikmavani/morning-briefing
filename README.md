# 🌅 Morning Briefing AI

A fully local AI-powered podcast generator that fetches news for topics you care about and reads them aloud to you every morning — privately, using **no cloud AI services**.

---

## ✨ Functional Overview

1. **Topic Input**: You define a comma-separated list of interest topics (e.g., *"AI, Gold, War, Australia"*).
2. **Web Search**: For each topic, a LangChain ReAct agent autonomously calls the [Tavily](https://tavily.com) web search API to retrieve fresh articles from the last 24 hours.
3. **Podcast Scripting**: The LLM (`Qwen3:8b` running locally via Ollama) summarises the news in natural podcast format, hosted by *Kartik*.
4. **Audio Synthesis**: The finished podcast script is fed directly into macOS's built-in neural TTS engine (`say`), producing a high-quality `.aiff` audio file per topic in the `output/` folder.

---

## 🔧 Prerequisites

Before running the project, ensure the following are installed on your machine:

| Tool | Purpose | Install |
|---|---|---|
| **Python 3.10+** | Runtime | [python.org](https://python.org) |
| **uv** | Package & virtual env manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Docker Desktop** | Runs the local PostgreSQL database | [docker.com](https://docker.com) |
| **Ollama** | Runs the local LLM | [ollama.com](https://ollama.com) |
| **Tavily API Key** | News web search | [app.tavily.com](https://app.tavily.com) (free tier available) |
| **macOS** | Required for native `say` TTS command | — |

---

## 🚀 Setup

### 1. Pull the LLM
```bash
ollama pull qwen3:8b
```

### 2. Clone & Install
```bash
git clone <repo-url>
cd morning-briefing

# Install all Python dependencies
make setup
```

### 3. Configure Environment
Copy the example environment file and fill in your values:
```bash
cp example.env .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/morning_briefing
DB_POOL_MIN_SIZE=1
DB_POOL_MAX_SIZE=20
MODEL_NAME=ollama:qwen3:8b
TAVILY_API_KEY=tvly-your-api-key-here
```

### 4. Run
```bash
make run
```

This command will:
- Boot the local PostgreSQL database via Docker
- Execute the Morning Briefing pipeline
- Generate `.aiff` podcast files in the `output/` folder

---

## 🛠 Makefile Commands

| Command | Description |
|---|---|
| `make setup` | Install Python dependencies via `uv` |
| `make run` | Start the database and run the briefing pipeline |
| `make test` | Run the full unit test suite |
| `make db-up` | Start the PostgreSQL Docker container |
| `make db-down` | Stop the PostgreSQL Docker container |
| `make clean` | Teardown Docker and delete the `.venv` |

---

## 🏛 Architecture

### Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Package Manager | `uv` | Fast Python package & env management |
| LLM Orchestration | `LangChain` + `LangGraph` | Agent execution, tool calling, memory |
| Local LLM | `Ollama` (`qwen3:8b`) | Offline news summarisation |
| Web Search | `Tavily API` | Real-time news retrieval |
| Database | `PostgreSQL` (via Docker) | LangGraph checkpoint persistence |
| Audio | macOS `say` CLI (NSSpeechSynthesizer) | Offline podcast audio generation |
| DI Framework | `dependency-injector` | IoC container for service singletons |
| Configuration | `pydantic-settings` | Type-safe `.env` variable loading |

### Project Structure

```
morning-briefing/
├── main.py                   # CLI entrypoint & orchestration loop
├── config/
│   └── settings.py           # Pydantic typed env config
├── core/
│   └── container.py          # IoC DI container (all singletons)
├── service/
│   ├── DatabaseService.py    # Postgres pool + LangGraph checkpointer
│   ├── LlmService.py         # Ollama LLM + ReAct news agent
│   ├── TaviliyService.py     # Tavily web search tool
│   └── AudioService.py       # macOS TTS speech synthesizer
├── tests/                    # PyTest unit test suite
├── docker-compose.yml        # Local PostgreSQL container definition
├── Makefile                  # Developer workflow commands
└── output/                   # Generated .aiff podcast audio files
```

### Dependency Injection Flow

```
AppSettings (pydantic .env)
    │
    ├──► DatabaseService (Postgres pool + LangGraph checkpointer)
    │         └──► LlmService (Ollama model + LangChain ReAct agent)
    │
    ├──► TavilyService (news search tool → injected into LlmService)
    │
    └──► AudioService (macOS say CLI → zero external dependencies)
```

All services are registered as **singletons** in `core/container.py` and are instantiated exactly once per application lifecycle.

---

## 🧪 Testing

```bash
make test
```

The test suite uses `pytest` + `pytest-mock` to mock all external I/O — no real database connections, no LLM calls, no web requests and no audio output during CI/CD.

| Test File | What It Covers |
|---|---|
| `test_database_service.py` | Connection pool setup, LangGraph checkpointer init |
| `test_llm_service.py` | LLM model creation, tool binding, `get_news()` output extraction |
| `test_tavily_service.py` | Client initialisation, search API call structure |
| `test_audio_service.py` | macOS `say` subprocess invocation isolation |
| `test_container.py` | Global IoC container dependency resolution |

---
## 📟 Sample Output
```
2026-03-22 17:35:19,528 - __main__ - INFO - Fetching news for topic: Gold and Silver
2026-03-22 17:35:21,480 - httpx - INFO - HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"
2026-03-22 17:35:32,120 - service.TaviliyService - INFO - Searching for news about Gold and Silver from 2026-03-21 to 2026-03-22
2026-03-22 17:35:50,147 - httpx - INFO - HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"
2026-03-22 17:36:30,103 - service.LlmService - INFO - Final Agent Output for {'messages': [HumanMessage(content='Search news from web about "Gold and Silver" from start date : "2026-03-21" to end date : "2026-03-22"', additional_kwargs={}, response_metadata={}, id='af3a5bd7-a321-4aa3-881c-a04ad72d9002')]}: {'messages': [HumanMessage(content='Search news from web about "Gold and Silver" from start date : "2026-03-21" to end date : "2026-03-22"', additional_kwargs={}, response_metadata={}, id='af3a5bd7-a321-4aa3-881c-a04ad72d9002'), AIMessage(content='', additional_kwargs={}, response_metadata={'model': 'qwen3:8b', 'created_at': '2026-03-22T06:35:32.117393Z', 'done': True, 'done_reason': 'stop', 'total_duration': 12572291833, 'load_duration': 74987208, 'prompt_eval_count': 236, 'prompt_eval_duration': 1752069209, 'eval_count': 204, 'eval_duration': 10690361092, 'logprobs': None, 'model_name': 'qwen3:8b', 'model_provider': 'ollama'}, id='lc_run--019d1441-5677-7902-9095-8dce1871da5e-0', tool_calls=[{'name': 'search_news_from_web', 'args': {'query': 'Gold and Silver', 'start_date': '2026-03-21', 'end_date': '2026-03-22'}, 'id': 'dda4abe1-49e5-42ad-a307-ee4cfac0d806', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 236, 'output_tokens': 204, 'total_tokens': 440}), ToolMessage(content='{"query": "Gold and Silver", "follow_up_questions": null, "answer": null, "images": [], "results": [{"url": "https://simplywall.st/stocks/us/materials/nyse-au/anglogold-ashanti/news/anglogold-ashanti-nyseau-valuation-check-after-mining-stock", "title": "AngloGold Ashanti (NYSE:AU) Valuation Check After Mining Stock Sell-Off On Weak Gold Silver And Copper Prices - simplywall.st", "score": 0.94458723, "published_date": "Sat, 21 Mar 2026 16:13:40 GMT", "content": "United States\\n /\\n Metals and Mining\\n /\\n NYSE:AU\\n\\n# AngloGold Ashanti (NYSE:AU) Valuation Check After Mining Stock Sell-Off On Weak Gold Silver And Copper Prices\\n\\nSimply Wall St\\n\\nAdvertisement\\n\\n## AngloGold Ashanti stock reaction to commodity sell-off\\n\\nMining stocks sold off after gold and silver hit six week lows and copper touched a three month low, and AngloGold Ashanti (NYSE:AU) dropped more than 7%, standing out among the session’s weakest S&P 500 names.\\n\\nSee our latest analysis for AngloGold Ashanti. [...] With AngloGold Ashanti trading well below recent analyst price targets and a model-based intrinsic estimate, yet coming off a steep short term slide, you need to ask whether this is a genuine opportunity or whether the market already reflects expectations for future growth.\\n\\n## Most Popular Narrative: 18.4% Undervalued\\n\\nThe most followed narrative puts AngloGold Ashanti’s fair value at $98, comfortably above the last close of $79.99. This frames the recent pullback against a higher long term anchor.\\n\\n> Organic production growth from brownfield projects (Obuasi ramp-up, Cuiabá, Siguiri, Geita, and upcoming Nevada developments) is set to increase output volumes and extend mine life, driving future revenue and earnings growth over the next decade.\\n\\nRead the complete narrative. [...] See our latest analysis for AngloGold Ashanti.\\n\\nThat sharp one day share price decline sits on top of a 15.7% 7 day and 26.2% 30 day share price fall, yet the 1 year total shareholder return of about 136% and 5 year total shareholder return above 3x indicate that longer term momentum has been strong even as recent sentiment has cooled.\\n\\nIf this sell off has you looking across the gold space, it may be worth scanning other producers using our screener of 28 elite gold producer stocks for potential ideas beyond AngloGold Ashanti.", "raw_content": null}, {"url": "https://www.mining.com/chart-billions-wiped-of-mining-stocks-as-gold-silver-copper-prices-plummet/", "title": "CHART: Billions wiped of mining stocks as gold, silver, copper prices plummet - Mining.com", "score": 0.920218, "published_date": "Sat, 21 Mar 2026 03:05:32 GMT", "content": "Copper ended the day down 4.0% and was last worth 5.30 per pound ($11,690 a tonne), down 7.4% for the week. Gold, silver and copper entered a technical bear market with gold down more than $1,100 or just over 20% from its January 29 record, silver dropping 44% and copper giving up just shy of 20% or more than $2,800 per tonne from its all-time high struck at the same time.\\n\\nGold, silver and platinum stocks were hardest hit with Newmont (NYSE:NEM) now trading 26.3% below levels seen just before the start of the Iran war at the end of February after Friday’s heavy selling which saw 30.7 million shares traded. [...] Gold (and copper and silver) bears are out. Image: The Scott\\n\\nStock losses for world’s biggest mining companies near 30% since war’s start as copper enters bear market, silver falls 40% from high and gold suffers worst week in decades.\\n\\nGold futures in New York fell by $225 an ounce from opening levels to last trade at $4,492 an ounce by late afternoon, a 3.5% decline on the day and more than 11% for the week. As usual silver’s swings were wilder with the precious metal exchanging hands for $67.81 in after hours trade, a 6.9% drop from the start of trading on Friday. [...] Barrick Mining (NYSE:B) is down 26.8% over the same period with 29.1 million shares exchanging hands on Friday. Newmont is now worth $104 billion in New York down from a peak of $143 billion at the end of January while Barrick’s market worth is down $27 billion since then for a $62 billion market cap on Friday.\\n\\nIt was reported this week that Teck Resources holds a royalty on Barrick’s Fourmile gold project in Nevada that could generate billions of dollars and impact the valuation of Barrick’s planned North American mine spinoff.\\n\\nShares in Anglogold Ashanti (NYSE:AU) are down an eye-watering 37.4% so far in March for a market value of $40 billion while Gold Fields (NYSE:GFI) has lost 33.6% to $35 billion. Kinross Gold’s slide reached 28.3% for a market cap of $32 billion.", "raw_content": null}, {"url": "https://www.mining.com/joint-venture/jv-article-novo-resources-boosts-gold-ounces-goal-in-victoria/", "title": "JV article: Novo Resources boosts gold ounces goal in Victoria - Mining.com", "score": 0.8267118, "published_date": "Sat, 21 Mar 2026 03:55:46 GMT", "content": "Silver Futures $ 69.664 / ozt  -4.35%\\n\\nAluminum Futures $ 3126.75 / ton  -1.30%\\n\\nMicro Gold Futures $ 4574.9 / ozt  -1.69%\\n\\nMicro Silver Futures $ 69.664 / ozt  -4.44%\\n\\nPlatinum $ 1970.5 / ozt  -0.10%\\n\\nGold Futures $ 4574.9 / ozt  -1.70%\\n\\nCopper $ 5.3745 / lb  -2.72%\\n\\nBrent Crude Oil $ 112.19 / bbl  4.20%\\n\\nPalladium $ 1445.2 / ozt  -1.32%\\n\\nCrude Oil $ 98.32 / bbl  3.49%\\n\\nNatural Gas $ 3.095 / Btu  -0.80%\\n\\nSilver Futures $ 69.664 / ozt  -4.35%\\n\\nAluminum Futures $ 3126.75 / ton  -1.30%\\n\\nMicro Gold Futures $ 4574.9 / ozt  -1.69%\\n\\nMicro Silver Futures $ 69.664 / ozt  -4.44%\\n\\nPlatinum $ 1970.5 / ozt  -0.10%\\n\\nGold Futures $ 4574.9 / ozt  -1.70%\\n\\nCopper $ 5.3745 / lb  -2.72%\\n\\nBrent Crude Oil $ 112.19 / bbl  4.20%\\n\\nPalladium $ 1445.2 / ozt  -1.32%\\n\\nCrude Oil $ 98.32 / bbl  3.49% [...] Novo Resources (ASX, TSX: NVO) has increased the exploration target for its Belltopper gold project in southern Australia and kicked-off preparations for inaugural drilling work at its gold, silver and antimony project in the west.\\n\\nThe company has released an exploration target of 460,000 to 880,000 oz. gold at Belltopper in Victoria, one of the company’s most advanced assets. The update is a 40% increase over its 2024 estimate based on drilling at four of seven priority areas there and the inclusion of a new area of interest. At Wyloo in the Pilbara region, Novo’s soil and rock chip sampling has identified a 200-hectare area for its drilling program, slated to begin in April. [...] ## Targets ready\\n\\nEarly results at Wyloo have been encouraging, Spreadborough said. Soil sampling has found a strong multi-element deposit and seven rock chip samples last year yielded peak assay results of 387 grams silver per tonne, 0.38% antimony, 5% lead, 1.6% zinc, 2.4% copper and 0.52 gram gold. Recent exploration has provided several targets ready to drill.\\n\\nNovo will undertake a heritage survey at the project in March to provide access for the April drilling of about 1,500 metres. The work will test the polymetallic vein and a large fault zone immediately south of the main target area.", "raw_content": null}, {"url": "https://www.bitget.com/amp/news/detail/12560605288368", "title": "Carlyle Commodities\' prospects depend on the Silver Pony transaction as their exploration phase concludes - Bitget", "score": 0.50781184, "published_date": "Sat, 21 Mar 2026 06:00:57 GMT", "content": "### Newton Gold Project Sale: The Turning Point\\n\\nThe pivotal moment for Carlyle came with the finalized sale of the Newton Gold Project to Axcap Ventures in June 2025. This transaction removed the company’s most significant asset—an inferred resource exceeding 840,000 ounces of gold—from its portfolio. With no exploration projects remaining, Carlyle’s prospects now depend on its ability to attract new investment. The company’s immediate focus is a proposed deal with Silver Pony Resources, supported by a private placement. To date, Carlyle has raised a cumulative $4.25 million through several funding rounds to back this new direction.\\n\\n### Market Profile and Strategic Shift [...] Carlyle Commodities has undergone a major transformation, shifting away from its roots as an exploration-driven mining company to focus primarily on raising and managing capital. This strategic redirection was highlighted by the recent departure of the company’s Vice President of Exploration—a move that reflects a broader change in direction rather than an isolated management adjustment. With the sale of its main asset, Carlyle is now centered on securing external funding to ensure its financial survival.\\n\\n### Newton Gold Project Sale: The Turning Point [...] Disclaimer: The content of this article solely reflects the author\'s opinion and does not represent the platform in any capacity. This article is not intended to serve as a reference for making investment decisions.\\n\\nUnderstand the market, then trade.\\n\\nBitget offers one-stop trading for cryptocurrencies, stocks, and gold.\\n\\nTrade now！\\n\\n## You may also like\\n\\nA Company Solely Focused on XRP Is About to Go Public\\n\\nTimesTabloid\\n•\\n2026/03/21 07:42\\n\\nThe 2 Best Consumer Staples Stocks to Consider Purchasing Today\\n\\n101 finance\\n•\\n2026/03/21 07:42\\n\\nChainlink Enhances Smart Contracts with Improved Access to Real-World Data\\n\\n101 finance\\n•\\n2026/03/21 07:40\\n\\nTenon Medical’s SImmetry+ Alpha Launch Could Validate Surge or Trigger Sell-Off\\n\\n101 finance\\n•\\n2026/03/21 07:39\\n\\n## Trending news\\n\\nMore\\n\\n1", "raw_content": null}, {"url": "https://www.tipranks.com/news/private-companies/uniti-ai-targets-growing-tech-adoption-in-self-storage-market", "title": "Uniti AI Targets Growing Tech Adoption in Self-Storage Market - TipRanks", "score": 0.033971995, "published_date": "Sat, 21 Mar 2026 06:03:04 GMT", "content": "Inflation RateUnemployment Rate\\n\\nClass Actions\\n\\nStock ScreenerETF Screener\\n\\nPopularPenny Stock ScreenerTechnical Analysis Screener\\n\\nDividend CenterBest Dividend Stocks\\n\\nPopularBest High Yield Dividend StocksDividend AristocratsDividend Stock Comparison\\n\\nNewDividend CalculatorDividend Returns ComparisonDividend Calendar\\n\\nMy ExpertsTop AnalystsTop Financial BloggersTop-Performing Corporate InsidersTop Hedge Fund ManagersTop Research FirmsTop Individual Investors\\n\\nNewsletter CenterSmart InvestorSmart Dividends\\n\\nNew\\n\\nTrending News\\n\\n[Premium\\n\\nStock Market Review: SPY, QQQ Tumble on Rate Hike Scenario as U.S.-Iran War Reaches 3-Week Mark\\n\\nEddie Pan11h ago\\n\\nDIAQQQ](/news/stock-market-review-spy-qqq-tumble-on-rate-hike-scenario-as-u-s-iran-war-reaches-3-week-mark \\"DIA | QQQ | SPY\\")\\n\\n[Premium [...] Trump Dashboard\\n\\nNew\\n\\nDividend Calculator\\n\\nOptions Profit Calculator\\n\\nDollar Cost Averaging\\n\\nCompound Interest Calculator\\n\\nMortgage Calculator\\n\\nAuto Loan Calculator\\n\\nStudent Loan Calculator\\n\\n401k Retirement Calculator\\n\\nEarnings Calendar\\n\\nDividend Calendar\\n\\nEconomic Calendar\\n\\nIPO Calendar\\n\\nStock Splits\\n\\nStock Buybacks\\n\\nFDA Calendar\\n\\nMarket Holidays\\n\\nDividend Center\\n\\nBest Dividend Stocks\\n\\nPopular\\n\\nBest High Yield Dividend Stocks\\n\\nDividend Aristocrats\\n\\nDividend Stock Comparison\\n\\nNew\\n\\nDividend Calculator\\n\\nDividend Returns Comparison\\n\\nDividend Calendar\\n\\nTop Analysts\\n\\nTop Financial Bloggers\\n\\nTop-Performing Corporate Insiders\\n\\nTop Hedge Fund Managers\\n\\nTop Research Firms\\n\\nTop Individual Investors\\n\\nTop Gainers\\n\\nTop Losers\\n\\nMost Active\\n\\nPremarket\\n\\nAfter-hours\\n\\nPrivate Companies", "raw_content": null}], "response_time": 0.7, "request_id": "7201ec3e-3054-48f2-9d48-339fd81f9e3d"}', name='search_news_from_web', id='d4d5a0c3-1bce-45b2-9800-62ef65969bce', tool_call_id='dda4abe1-49e5-42ad-a307-ee4cfac0d806'), AIMessage(content='**Podcast Summary: Gold and Silver Market Movements (March 21-22, 2026)**  \n*Hosted by Kartik*  \n\n**Intro:**  \nWelcome to today’s episode! We’re diving into the latest developments in the gold and silver markets, with insights from March 21-22, 2026.  \n\n**Segment 1: AngloGold Ashanti Plummets Amid Commodity Sell-Off**  \nAngloGold Ashanti (NYSE:AU) saw its stock drop over 7% on weak gold and silver prices, part of a broader mining sector sell-off. The decline follows a 15.7% weekly drop, though long-term returns remain strong. Analysts note the stock is undervalued, with a fair value estimate of $98.  \n\n**Segment 2: Mining Stocks Lose Billions as Prices Plummet**  \nGold, silver, and copper prices hit six-week and three-month lows, wiping billions from mining stocks. Gold fell below $1,900, silver dipped below $22, and copper hit a three-month low. The U.S.-Iran war tensions and rate hike fears exacerbated the downturn.  \n\n**Segment 3: Novo Resources Boosts Gold Exploration Targets**  \nIn Australia, Novo Resources (ASX: NVO) raised its gold exploration target at the Belltopper project to 460,000–880,000 ounces. The company plans drilling in April, with promising soil and rock chip samples showing multi-metal deposits.  \n\n**Segment 4: Carlyle Commodities Relying on Silver Pony Deal**  \nCarlyle Commodities, after selling its Newton Gold Project, now focuses on raising capital via a proposed deal with Silver Pony Resources. The company has secured $4.25 million in funding to sustain operations.  \n\n**Outro:**  \nThat’s it for today! The gold and silver markets remain volatile, with both short-term dips and long-term opportunities. Stay tuned for more updates!  \n\n*End of Episode.*', additional_kwargs={}, response_metadata={'model': 'qwen3:8b', 'created_at': '2026-03-22T06:36:30.087825Z', 'done': True, 'done_reason': 'stop', 'total_duration': 56931064709, 'load_duration': 70495667, 'prompt_eval_count': 3625, 'prompt_eval_duration': 16787354333, 'eval_count': 702, 'eval_duration': 39873696248, 'logprobs': None, 'model_name': 'qwen3:8b', 'model_provider': 'ollama'}, id='lc_run--019d1441-8ba3-72f0-916d-28fc98190582-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 3625, 'output_tokens': 702, 'total_tokens': 4327})]}
2026-03-22 17:36:30,105 - __main__ - INFO - Final Agent Output for Gold and Silver: **Podcast Summary: Gold and Silver Market Movements (March 21-22, 2026)**  
*Hosted by Kartik*  

**Intro:**  
Welcome to today’s episode! We’re diving into the latest developments in the gold and silver markets, with insights from March 21-22, 2026.  

**Segment 1: AngloGold Ashanti Plummets Amid Commodity Sell-Off**  
AngloGold Ashanti (NYSE:AU) saw its stock drop over 7% on weak gold and silver prices, part of a broader mining sector sell-off. The decline follows a 15.7% weekly drop, though long-term returns remain strong. Analysts note the stock is undervalued, with a fair value estimate of $98.  

**Segment 2: Mining Stocks Lose Billions as Prices Plummet**  
Gold, silver, and copper prices hit six-week and three-month lows, wiping billions from mining stocks. Gold fell below $1,900, silver dipped below $22, and copper hit a three-month low. The U.S.-Iran war tensions and rate hike fears exacerbated the downturn.  

**Segment 3: Novo Resources Boosts Gold Exploration Targets**  
In Australia, Novo Resources (ASX: NVO) raised its gold exploration target at the Belltopper project to 460,000–880,000 ounces. The company plans drilling in April, with promising soil and rock chip samples showing multi-metal deposits.  

**Segment 4: Carlyle Commodities Relying on Silver Pony Deal**  
Carlyle Commodities, after selling its Newton Gold Project, now focuses on raising capital via a proposed deal with Silver Pony Resources. The company has secured $4.25 million in funding to sustain operations.  

**Outro:**  
That’s it for today! The gold and silver markets remain volatile, with both short-term dips and long-term opportunities. Stay tuned for more updates!  

*End of Episode.*
2026-03-22 17:36:30,105 - service.AudioService - INFO - Synthesizing script to output/gold_and_silver_briefing.aiff...
2026-03-22 17:36:48,551 - service.AudioService - INFO - ✅ Podcast generated successfully: output/gold_and_silver_briefing.aiff
```

## 📄 License

MIT
