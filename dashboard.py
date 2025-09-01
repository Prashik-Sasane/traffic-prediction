import streamlit as st
import folium
from streamlit_folium import st_folium

# Import services
from services.tomtom_service import geocode_tomtom, route_tomtom
from services.weather_service import weather_onecall
from services.llm_service import ask_llm


# ---------------------------- CONFIG ----------------------------
st.set_page_config(page_title="Delhi Travel Planner", layout="wide")
st.title("🚦 Travel Planner")

# ---------------------------- HELPERS ----------------------------
def human_eta(seconds: int):
    if not seconds:
        return "—"
    m = int(round(seconds / 60.0))
    return f"{m} min" if m < 90 else f"{m//60} h {m%60} min"

def km(meters: int):
    return "—" if not meters else f"{meters/1000:.1f} km"

# ---------------------------- SESSION STATE ----------------------------
for key in ["src", "dst", "route", "weather", "llm", "map"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ---------------------------- LAYOUT ----------------------------
col_left, col_right = st.columns([1, 1], gap="large")

# ---------- LEFT PANEL ----------
with col_left:
    st.subheader("📍 Plan your Trip")

    # Top Inputs
    src_text = st.text_input("Source", value="Connaught Place, New Delhi")
    dst_text = st.text_input("Destination", value="Indira Gandhi International Airport, New Delhi")
    mode = st.selectbox("Mode", ["car", "bicycle", "pedestrian"], index=0)
    use_traffic = st.checkbox("Use live traffic", value=True)

    go = st.button("Calculate Plan", type="primary", use_container_width=True)

    st.markdown("---")
    st.subheader("🤖 Travel Plan")

    if st.session_state.llm:
        st.write(st.session_state.llm)
    else:
        st.info("Travel plan will appear here after you calculate.")

# ---------- RIGHT PANEL ----------
with col_right:
    st.subheader("🗺️ Map View")
    if st.session_state.map:
        st_folium(st.session_state.map, width=700, height=700)
    else:
        st.info("Map will appear here once you calculate a route.")

# ---------------------------- ACTION (on button click) ----------------------------
if go:
    try:
        # 1. Geocode
        src = geocode_tomtom(src_text)
        dst = geocode_tomtom(dst_text)

        if not src or not dst:
            st.error("❌ Could not geocode one of the locations. Try a more specific name.")
        else:
            st.session_state.src = src
            st.session_state.dst = dst

            # 2. Route
            route = route_tomtom(src[0], src[1], dst[0], dst[1], mode=mode, traffic=use_traffic)
            if not route:
                st.error("❌ No route found. Try changing mode or locations.")
            else:
                st.session_state.route = route

                # 3. Weather
                wx = weather_onecall(dst[0], dst[1])
                st.session_state.weather = wx if wx else None

                # 4. LLM Travel Plan
                cur = wx.get("main", {}) if wx else {}
                llm_input = f"""
Route: {src_text} → {dst_text}
ETA: {human_eta(route['time_s'])}, Distance: {km(route['length_m'])}, Delay: {human_eta(route['delay_s'])}
Weather: {cur.get('weather',[{'description':'—'}])[0]['description']}, {cur.get('temp','?')}°C.

Give a short travel advisory with:
1. Time, Distance, Traffic delays
2. Where traffic is expected
3. Weather (temperature, condition)
4. Suggestions: leave early? precautions?
"""
                st.session_state.llm = ask_llm(llm_input)

                # 5. Map
                fmap = folium.Map(location=[(src[0]+dst[0])/2, (src[1]+dst[1])/2], zoom_start=12, control_scale=True)
                folium.Marker(src, popup="Source", icon=folium.Icon(color="green")).add_to(fmap)
                folium.Marker(dst, popup="Destination", icon=folium.Icon(color="red")).add_to(fmap)
                if route.get("points"):
                    folium.PolyLine(route["points"], color="blue", weight=5, opacity=0.8).add_to(fmap)

                st.session_state.map = fmap

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
