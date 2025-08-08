import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import os
import sys
from urllib.parse import quote_plus

# Try to import Pillow (for robust image handling). If missing, notify user.
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ----------------------------
# Config / Paths -> update here if needed
# ----------------------------
ICON_SIZE = (28, 28)  # uniform icon size used for all buttons

# Use the exact paths you supplied (raw strings to avoid backslash escaping)
ICON_PATHS = {
    "YouTube": r"C:\Users\Shambhavi\OneDrive\Desktop\Automation\icons\youtube_3670209.png",
    "Google": r"C:\Users\Shambhavi\OneDrive\Desktop\Automation\icons\google_2965278.png",
    "Wikipedia": r"C:\Users\Shambhavi\OneDrive\Desktop\Automation\icons\apple.png",      # placeholder
    "WhatsApp": r"C:\Users\Shambhavi\OneDrive\Desktop\Automation\icons\social.png",
    "GitHub": r"C:\Users\Shambhavi\OneDrive\Desktop\Automation\icons\github-logo.png",
    "Instagram": r"C:\Users\Shambhavi\OneDrive\Desktop\Automation\icons\instagram.png",
}

THEME = {
    "bg": "#c8f0e8",
    "header": "#0077b6",
    "btn_light": "#90e0ef",
    "btn_hover": "#bfeff6",
    "history_bg": "#e6fbff",
    "title_fg": "#04335a"
}

# ----------------------------
# Helper: Build platform URL from query
# ----------------------------
def build_url(platform, query):
    q = query.strip()
    # If query empty, open the platform's main/home page
    if not q:
        if platform == "YouTube":
            return "https://www.youtube.com/"
        if platform == "Google":
            return "https://www.google.com/"
        if platform == "Wikipedia":
            return "https://en.wikipedia.org/"
        if platform == "WhatsApp":
            return "https://web.whatsapp.com/"
        if platform == "GitHub":
            return "https://github.com/"
        if platform == "Instagram":
            return "https://www.instagram.com/"
        return None

    # Otherwise, build search-specific URLs
    if platform == "YouTube":
        return "https://www.youtube.com/results?search_query=" + quote_plus(q)
    if platform == "Google":
        return "https://www.google.com/search?q=" + quote_plus(q)
    if platform == "Wikipedia":
        return "https://en.wikipedia.org/wiki/" + q.replace(" ", "_")
    if platform == "WhatsApp":
        return "https://web.whatsapp.com/search?q=" + quote_plus(q)
    if platform == "GitHub":
        return "https://github.com/search?q=" + quote_plus(q)
    if platform == "Instagram":
        uname = q.lstrip("@").split()[0]
        return f"https://www.instagram.com/{quote_plus(uname)}"
    return None


# ----------------------------
# Helper: load and normalize icon (Pillow) or fallback
# ----------------------------
ICON_SIZE = (32, 32)
def load_icon(path, size=ICON_SIZE):
    """Return a Tk PhotoImage. If loading fails, return a generated placeholder."""
    # If PIL available, use it for proper resizing and alpha handling
    if PIL_AVAILABLE and path and os.path.exists(path):
        try:
            img = Image.open(path).convert("RGBA")
            img = img.resize(size, Image.LANCZOS)  # exact resize, no padding
            shadow = Image.new("RGBA", (size[0]+4, size[1]+4), (0, 0, 0, 0))
            shadow.paste(img, (2, 2), img)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"[icon] Error loading {path}: {e}", file=sys.stderr)
            # create canvas of desired size and paste centered thumbnail
            img.thumbnail(size, getattr(Image, "LANCZOS", Image.ANTIALIAS))
            canvas = Image.new("RGBA", size, (0, 0, 0, 0))
            x = (size[0] - img.width) // 2
            y = (size[1] - img.height) // 2
            canvas.paste(img, (x, y), img)
            return ImageTk.PhotoImage(canvas)
        except Exception as e:
            print(f"[icon] Error loading {path}: {e}", file=sys.stderr)

    # Fallback: try Tkinter PhotoImage (less robust) if file exists
    try:
        if os.path.exists(path):
            img = tk.PhotoImage(file=path)
            img = img.subsample(max(1, img.width() // size[0]), max(1, img.height() // size[1]))
            return img
    except Exception as e:
        print(f"[icon] tk.PhotoImage failed for {path}: {e}", file=sys.stderr)

    # Final fallback: generate a simple placeholder image with first letter
    if PIL_AVAILABLE:
      img = Image.new("RGBA", size, (130, 180, 200, 255))
      draw = ImageDraw.Draw(img)
      font = ImageFont.load_default()
      initial = os.path.splitext(os.path.basename(path))[0][:1].upper() if path else "?"
      w, h = draw.textsize(initial, font=font)
      draw.text(((size[0]-w)/2, (size[1]-h)/2), initial, fill=(255,255,255,255), font=font)
      return ImageTk.PhotoImage(img)
    else:
        return tk.PhotoImage(width=size[0], height=size[1])

# ----------------------------
# UI: main window
# ----------------------------
root = tk.Tk()
root.title("Your Professional Assistant")
root.geometry("560x600")
root.configure(bg=THEME["bg"])
root.resizable(False, False)

# header canvas (simple colored bar with title)
header = tk.Canvas(root, width=560, height=64, highlightthickness=0)
header.pack(fill="x")
header.create_rectangle(0, 0, 560, 64, fill=THEME["header"], outline="")
header.create_text(280, 32, text="🔎 Your Assistant", fill="white", font=("Helvetica", 18, "bold"))

# search entry
frm_top = tk.Frame(root, bg=THEME["bg"])
frm_top.pack(padx=14, pady=12, fill="x")

lbl = tk.Label(frm_top, text="Enter your search term:", bg=THEME["bg"], fg=THEME["title_fg"], font=("Helvetica", 12, "bold"))
lbl.pack(anchor="w")
entry = tk.Entry(frm_top, font=("Helvetica", 12))
entry.pack(fill="x", pady=8)
entry.focus()

# ----------------------------
# Buttons area (2 columns)
# ----------------------------
btn_frame = tk.Frame(root, bg=THEME["bg"])
btn_frame.pack(padx=14, pady=6, fill="both", expand=False)

# define platforms in desired order (label, icon_path, color)
platforms = [
    ("YouTube", ICON_PATHS.get("YouTube"), "#f94144"),
    ("Google", ICON_PATHS.get("Google"), "#4da8da"),
    ("Wikipedia", ICON_PATHS.get("Wikipedia"), "#2b9348"),
    ("WhatsApp", ICON_PATHS.get("WhatsApp"), "#40916c"),
    ("GitHub", ICON_PATHS.get("GitHub"), "#2d6a4f"),
    ("Instagram", ICON_PATHS.get("Instagram"), "#7b2cbf"),
]

# keep image references so they don't get garbage-collected
_images = []
_buttons = []

def on_enter(e):
    w = e.widget
    w._orig_bg = w.cget("bg")
    w.configure(bg=THEME["btn_hover"])

def on_leave(e):
    w = e.widget
    if hasattr(w, "_orig_bg"):
        w.configure(bg=w._orig_bg)

def do_search(platform_name):
    q = entry.get().strip()
    if not q:
        messagebox.showwarning("Input Error", "Please enter a search term.")
        return
    url = build_url(platform_name, q)
    if url:
        webbrowser.open(url)
        # add to history
        history_list.insert(0, f"{platform_name}: {q}")
    else:
        messagebox.showerror("Error", "Unable to build URL for platform.")

# create grid buttons 2 columns
cols = 2
for idx, (label, path, color) in enumerate(platforms):
    icon = load_icon(path)
    _images.append(icon)  # keep reference

    btn = tk.Button(
        btn_frame,
        text=" " + label,
        image=icon,
        compound="left",
        anchor="w",
        padx=6,
        pady=4,
        font=("Helvetica", 11, "bold"),
        bg=color,
        fg="white",
        relief="flat",
        height=40,
        command=lambda name=label: do_search(name)
    )
    r = idx // cols
    c = idx % cols
    btn.grid(row=r, column=c, sticky="ew", padx=6, pady=6)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    _buttons.append(btn)

# make columns expand equally
for c in range(cols):
    btn_frame.grid_columnconfigure(c, weight=1)

# ----------------------------
# History panel (with scrollbar)
# ----------------------------
hist_label = tk.Label(root, text="Search History", bg=THEME["bg"], fg=THEME["title_fg"], font=("Helvetica", 12, "bold"))
hist_label.pack(anchor="w", padx=14, pady=(10, 0))

hist_frame = tk.Frame(root, bg=THEME["bg"])
hist_frame.pack(padx=14, pady=6, fill="both", expand=True)

scroll = ttk.Scrollbar(hist_frame, orient="vertical")
history_list = tk.Listbox(hist_frame, yscrollcommand=scroll.set, bg=THEME["history_bg"], font=("Helvetica", 10))
scroll.config(command=history_list.yview)
scroll.pack(side="right", fill="y")
history_list.pack(side="left", fill="both", expand=True)

# footer row (exit + clear history)
frm_footer = tk.Frame(root, bg=THEME["bg"])
frm_footer.pack(fill="x", padx=14, pady=8)

def clear_history():
    history_list.delete(0, tk.END)

tk.Button(frm_footer, text="Clear History", command=clear_history, bg="#ffb703", fg="black", padx=8, pady=6).pack(side="left")
tk.Button(frm_footer, text="Exit", command=root.destroy, bg="#ef233c", fg="white", padx=8, pady=6).pack(side="right")

# Enter key defaults to Google search
root.bind("<Return>", lambda e: do_search("Google"))

# If Pillow isn't available, tell the user (icons may still work with tk.PhotoImage but resizing won't)
if not PIL_AVAILABLE:
    messagebox.showinfo("Pillow not installed", "Pillow (PIL) is not installed. Icons will still try to load but resizing or placeholders may not render perfectly.\n\nInstall Pillow for best results:\n\npip install pillow")

root.mainloop()
