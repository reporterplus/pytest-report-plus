def resolve_driver(item):
    candidates = item.funcargs

    # 1. Priority check: page, then context
    for name in ("page", "context"):
        obj = candidates.get(name)
        if obj and hasattr(obj, "screenshot"):
            return obj

    # 2. If any object has .screenshot
    for val in candidates.values():
        if hasattr(val, "screenshot"):
            return val

    # 3. Fallback: Selenium-style .get_screenshot_as_file
    for val in candidates.values():
        if hasattr(val, "get_screenshot_as_file"):
            return val

    # 4. Fallback to browser or driver if present
    for name in ("browser", "driver"):
        obj = candidates.get(name)
        if obj:
            return obj

    # 5. Check for custom attribute (e.g., item.page_for_screenshot)
    if hasattr(item, "page_for_screenshot"):
        return item.page_for_screenshot

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