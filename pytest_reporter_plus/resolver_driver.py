def resolve_driver(item):
    for name in ("page", "driver", "browser"):
        if name in item.funcargs:
            return item.funcargs[name]

    fallback = getattr(item, "page_for_screenshot", None)
    if fallback:
        return fallback

    # Fallback
    for val in item.funcargs.values():
        if hasattr(val, "screenshot") or hasattr(val, "save_screenshot"):
            return val

    return None


import os

def take_screenshot_generic(path, item, driver):
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, f"{item.name}_failure.png")

    if hasattr(driver, "screenshot"):
        driver.screenshot(path=filename)
    elif hasattr(driver, "save_screenshot"):
        driver.save_screenshot(filename)
    else:
        raise RuntimeError("Driver has no screenshot method")

    return filename