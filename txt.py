import webbrowser

def open_web_page(url):
    webbrowser.open(url)

if __name__ == "__main__":
    url = "https://www.example.com"
    open_web_page(url)

    # Note: Capturing information about people who visit a website requires server-side code.
    # The current script only opens a web page in the browser; it cannot capture visitor info.
    # To capture visitor info, you need to implement tracking on the website itself (e.g., using analytics or server logs).
    print("To capture visitor information, implement tracking on the website using server-side code or analytics tools.")
