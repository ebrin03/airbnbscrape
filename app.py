import pyairbnb
#]import csv
#from datetime import datetime
from collections.abc import MutableMapping
#from openpyxl import Workbook
from flask import Flask, request

def do_data(
    currency="GBP",
    check_in="2025-09-10",
    check_out="2025-09-14",
    ne_lat=47.55,
    ne_long=19.10,
    sw_lat=47.48,
    sw_long=19.02,
    zoom_value=2,
    price_min=0,
    price_max=0,
    place_type="Entire home/apt",
    amenities=[],
    free_cancellation=False,
    language="en",
    proxy_url="",
):
    # === FLATTENING FUNCTION ===
    def flatten_json(y, parent_key="", sep="_"):
        items = []
        for k, v in y.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                if all(isinstance(i, (str, int, float, bool)) or i is None for i in v):
                    items.append((new_key, ", ".join(map(str, v))))
                else:
                    items.append((new_key, "[list]"))
            else:
                items.append((new_key, v))
        return dict(items)

    # === SEARCH PARAMETERS ===

    # === SEARCH ===
    print("Searching Airbnb listings...")
    search_results = pyairbnb.search_all(
        check_in=check_in,
        check_out=check_out,
        ne_lat=ne_lat,
        ne_long=ne_long,
        sw_lat=sw_lat,
        sw_long=sw_long,
        zoom_value=zoom_value,
        price_min=price_min,
        price_max=price_max,
        place_type=place_type,
        amenities=amenities,
        free_cancellation=free_cancellation,
        currency=currency,
        language=language,
        proxy_url=proxy_url,
    )
    print(f"Found {len(search_results)} listings.")

    # === ADD URL TO LISTINGS + COLLECT IMAGE DATA ===
    image_rows = []
    for listing in search_results:
        if "room_id" in listing:
            listing["listing_url"] = (
                f"https://www.airbnb.com/rooms/{listing['room_id']}"
            )
            if "images" in listing and isinstance(listing["images"], list):
                for image in listing["images"]:
                    if "url" in image:
                        image_rows.append(
                            {"room_id": listing["room_id"], "image_url": image["url"]}
                        )

    # === FLATTEN LISTINGS ===
    flat_results = [flatten_json(listing) for listing in search_results]

    print(flat_results)

    return flat_results, image_rows


from flask import Flask

app = Flask(__name__)

@app.route("/data")
def hello_world():
    currency = request.args.get("currency")
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")
    ne_lat = request.args.get("ne_lat")
    ne_long = request.args.get("ne_long")
    sw_lat = request.args.get("sw_lat")
    sw_long = request.args.get("sw_long")
    zoom_value = request.args.get("zoom_value")
    price_min = request.args.get("price_min")
    price_max = request.args.get("price_max")
    place_type = request.args.get("place_type")
    amenities = request.args.get("amenities")
    free_cancellation = request.args.get("free_cancellation")
    language = request.args.get("language")
    proxy_url = request.args.get("proxy_url")
    flat_results, image_rows = do_data(
        currency=currency,
        check_in=check_in,
        check_out=check_out,
        ne_lat=ne_lat,
        ne_long=ne_long,
        sw_lat=sw_lat,
        sw_long=sw_long,
        zoom_value=zoom_value,
        price_min=price_min,
        price_max=price_max,
        place_type=place_type,
        amenities=amenities,
        free_cancellation=free_cancellation,
        language=language,
        proxy_url=proxy_url,
        flat_results=flat_results,
    )
    return {"results": flat_results, "images": image_rows}
