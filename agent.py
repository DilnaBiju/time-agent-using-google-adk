from datetime import datetime
from zoneinfo import ZoneInfo   # built-in in Python 3.9+
from google.adk.agents.llm_agent import Agent

# simple mapping of common city names -> tz database names
TIMEZONE_MAP = {
    "kochi": "Asia/Kolkata",
    "cochin": "Asia/Kolkata",
    "kochii": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "mumbai": "Asia/Kolkata",
    "kolkata": "Asia/Kolkata",
    "chennai": "Asia/Kolkata",
    "bangalore": "Asia/Kolkata",
    "bengaluru": "Asia/Kolkata",
    "new york": "America/New_York",
    "nyc": "America/New_York",
    "london": "Europe/London",
    "tokyo": "Asia/Tokyo",
    "sydney": "Australia/Sydney",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "dubai": "Asia/Dubai"
    # add more as needed
}

def get_current_time(city: str) -> dict:
    """Return the current time for the given city string."""
    try:
        if not city:
            return {"status": "error", "message": "No city provided."}

        key = city.strip().lower()

        # try exact map match, else try to match substring
        tz_name = TIMEZONE_MAP.get(key)
        if not tz_name:
            # substring matching (e.g. user types "Kochi, India")
            for k, v in TIMEZONE_MAP.items():
                if k in key:
                    tz_name = v
                    break

        if not tz_name:
            # fallback to UTC if city not recognized
            tz_name = "UTC"

        now = datetime.now(ZoneInfo(tz_name))
        # format: 2025-11-11 07:45 PM (Timezone)
        pretty = now.strftime("%Y-%m-%d %I:%M %p")
        debug = {"requested": city, "timezone_used": tz_name, "datetime": pretty}
        print("DEBUG get_current_time ->", debug)   # visible in ADK console for debugging

        return {"status": "success", "city": city, "time": pretty, "timezone": tz_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# keep your root_agent registration unchanged, pointing to the tools list:
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Tells current time in cities.",
    instruction="Use the 'get_current_time' tool to answer time queries.",
    tools=[get_current_time],
)
