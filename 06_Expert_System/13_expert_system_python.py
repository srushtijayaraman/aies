"""Interactive rule-based expert system (Python equivalent of the Prolog lab)."""

def yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer y or n.")

if __name__ == "__main__":
    print("Mini Network Troubleshooting Expert System")
    no_internet = yes_no("Is there no internet connection?")
    if not no_internet:
        print("Advice: Your connection appears to be working. Check the specific app if needed.")
    else:
        red = yes_no("Is the router light red or showing an error?")
        one_device = yes_no("Is the issue limited to only one device?")
        if red:
            print("Advice: Check router power, cables, and the ISP connection.")
        elif one_device:
            print("Advice: Check that device's Wi-Fi settings, airplane mode, and network adapter.")
        else:
            print("Advice: Restart the router; if all devices remain offline, contact your ISP.")
