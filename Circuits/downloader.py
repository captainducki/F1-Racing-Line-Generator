import os
import fastf1
import pandas as pd
 
CIRCUITS = {
    "silverstone": ("British Grand Prix",       2023),
    "spa":         ("Belgian Grand Prix",        2023),
    "suzuka":      ("Japanese Grand Prix",       2023),
    "jeddah":      ("Saudi Arabian Grand Prix",  2023),
    "bahrain":     ("Bahrain Grand Prix",        2023),
    "interlagos": ("São Paulo Grand Prix", 2023),  # last held 2017 but it is still in FastF1
}
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
 
 
def download_circuit(name: str, event_name: str, year: int) -> None:
    print(f"  Downloading {name.capitalize()}...")
 
    session = fastf1.get_session(year, event_name, "Q")
    session.load()
 
    circuit_info = session.get_circuit_info()
    corners = circuit_info.corners
 
    lap = session.laps.pick_fastest()
    tel = lap.get_telemetry()
 
    xy = tel[["X", "Y"]].dropna().reset_index(drop=True)
 
    output_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
    xy.to_csv(output_path, index=False, header=False)
 
    print(f"  Saved {len(xy)} points → {output_path}")
 
 
def main():
    print("Racing Line Generator — Circuit Downloader")
    print("=" * 50)
 
    cache_dir = os.path.join(OUTPUT_DIR, ".fastf1_cache")
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)
 
    success = []
    failed = []
 
    for name, (event_name, year) in CIRCUITS.items():
        try:
            download_circuit(name, event_name, year)
            success.append(name)
        except Exception as e:
            print(f"  FAILED {name}: {e}")
            failed.append(name)
 
    print("=" * 50)
    print(f"Done. {len(success)} succeeded, {len(failed)} failed.")
 
    if failed:
        print(f"Failed circuits: {', '.join(failed)}")
        print("Check the event name spelling or try a different year.")
 
 
if __name__ == "__main__":
    main()
 
