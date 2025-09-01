import http.server
import socketserver
import cgi

PORT = 8000

# Global variables
message = ""
bg_color = "#f5f5f5"  # default background

class Handler(http.server.CGIHTTPRequestHandler):
    def do_GET(self):
        global message, bg_color
        if "?" in self.path:
            query = self.path.split("?")[1]
            params = cgi.parse_qs(query)
            mood = params.get("mood", [""])[0]

            if mood == "happy":
                message = "😊 Great! Have a wonderful day!"
                bg_color = "#fff9c4"  # light yellow
            elif mood == "sad":
                message = "😔 Take rest, things will get better!"
                bg_color = "#bbdefb"  # light blue
            elif mood == "angry":
                message = "😡 Take a deep breath and calm down!"
                bg_color = "#ffcdd2"  # light red/pink

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = f"""
        <html>
        <head>
            <title>Mood Tracker</title>
            <style>
                body {{
                    font-family: Arial;
                    text-align: center;
                    padding: 50px;
                    background: {bg_color};
                    transition: background 0.5s;
                }}
                h1 {{ font-size: 36px; }}
                button {{
                    font-size: 50px;
                    margin: 15px;
                    padding: 10px 20px;
                    cursor: pointer;
                    border: none;
                    background: transparent;
                }}
                #message {{
                    margin-top: 30px;
                    font-size: 24px;
                    color: #333;
                }}
                p {{
                    margin-top: 50px;
                    font-size: 14px;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <h1>How are you feeling today?</h1>
            <a href="?mood=happy"><button>😊</button></a>
            <a href="?mood=sad"><button>😔</button></a>
            <a href="?mood=angry"><button>😡</button></a>
            <div id="message">{message}</div>
            <p>Created by Atharv Awate</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()