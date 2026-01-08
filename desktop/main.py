import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

def get_system_font() -> str | None:
    search_paths = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\seguiemj.ttf",
        r"/Library/Fonts/Arial.ttf",
        r"/System/Library/Fonts/Helvetica.ttc",
        r"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "arial.ttf",
    ]
    for path in search_paths:
        if os.path.exists(path):
            return path
    return None

class WatermarkApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Watermark Studio")
        self.root.geometry("1250x900")
        self.root.minsize(900, 700)

        self._set_app_icon()

        self._resize_timer = None

        self.colors = {
            "bg_main": "#1e1e1e",
            "bg_sidebar": "#2b2b2b",
            "bg_input_area": "#333333",
            "fg_text": "#ffffff",
            "fg_sub": "#aaaaaa",
            "accent": "#007acc",
            "accent_hover": "#0098ff",
            "input_bg": "#3c3c3c",
            "danger": "#d9534f",
            "danger_hover": "#c9302c"
        }

        self.base_image: Image.Image | None = None
        self.original_filename: str | None = None
        self.watermark_logo: Image.Image | None = None
        self.processed_image: Image.Image | None = None
        self.tk_image_ref: ImageTk.PhotoImage | None = None
        self.font_path: str | None = get_system_font()
        self.text_color: tuple[int, int, int] = (255, 255, 255)

        self.mode_var = tk.StringVar(value="text")
        self.text_content = tk.StringVar(value="© Copyright")
        self.position_var = tk.StringVar(value="Bottom Right")
        self.size_var = tk.DoubleVar(value=5.0)
        self.opacity_var = tk.DoubleVar(value=90.0)

        self._setup_styles()
        self._build_layout()
        self._update_toggle_visuals()
        self._toggle_input_mode()

        self.root.bind("<Configure>", self._on_resize_debounced)

    def _set_app_icon(self) -> None:
        icon_path = "logo-icon.png"
        try:
            if os.path.exists(icon_path):
                icon_image = Image.open(icon_path)
                self.app_icon = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(False, self.app_icon)
        except Exception:
            pass

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=self.colors["bg_sidebar"])
        style.configure("Main.TFrame", background=self.colors["bg_main"])
        style.configure("ToolGroup.TFrame", background=self.colors["bg_input_area"])

        style.configure(
            "TLabel",
            background=self.colors["bg_sidebar"],
            foreground=self.colors["fg_text"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Header.TLabel",
            background=self.colors["bg_sidebar"],
            foreground=self.colors["accent"],
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "Sub.TLabel",
            background=self.colors["bg_input_area"],
            foreground=self.colors["fg_sub"],
            font=("Segoe UI", 9),
        )

        style.configure(
            "Action.TButton",
            background=self.colors["accent"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        style.map("Action.TButton", background=[("active", self.colors["accent_hover"])])

        style.configure(
            "Danger.TButton",
            background=self.colors["bg_sidebar"],
            foreground=self.colors["danger"],
            font=("Segoe UI", 9),
            borderwidth=1,
            bordercolor=self.colors["danger"]
        )
        style.map(
            "Danger.TButton",
            background=[("active", self.colors["danger"])],
            foreground=[("active", "white")],
            bordercolor=[("active", self.colors["danger"])]
        )

        style.configure(
            "Control.TButton",
            background=self.colors["input_bg"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            width=3
        )
        style.map("Control.TButton", background=[("active", self.colors["accent"])])

        style.configure(
            "ToggleOff.TButton",
            background=self.colors["input_bg"],
            foreground=self.colors["fg_sub"],
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.map("ToggleOff.TButton", background=[("active", "#4a4a4a")])

        style.configure(
            "ToggleOn.TButton",
            background=self.colors["accent"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        style.map("ToggleOn.TButton", background=[("active", self.colors["accent"])])

        style.configure(
            "Modern.TEntry",
            fieldbackground="#444444",
            foreground="white",
            insertcolor="white",
            borderwidth=0,
            padding=10,
        )

        self.root.configure(bg=self.colors["bg_main"])

    def _build_layout(self) -> None:
        sidebar_container = tk.Frame(
            self.root,
            bg=self.colors["bg_sidebar"],
            width=340,
        )
        sidebar_container.pack(side="left", fill="y")
        sidebar_container.pack_propagate(False)

        sidebar = ttk.Frame(sidebar_container, padding=20)
        sidebar.pack(fill="both", expand=True)

        tk.Label(
            sidebar,
            text="WATERMARK STUDIO",
            bg=self.colors["bg_sidebar"],
            fg="white",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", pady=(0, 25))

        ttk.Label(sidebar, text="SOURCE IMAGE", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Button(
            sidebar,
            text="📂 Open Image",
            style="Action.TButton",
            command=self.load_base_image,
        ).pack(fill="x", ipady=5)

        ttk.Frame(sidebar, height=10).pack()

        ttk.Button(
            sidebar,
            text="✕ Remove Image",
            style="Danger.TButton",
            command=self.remove_base_image,
        ).pack(fill="x", pady=(0, 20))

        ttk.Label(sidebar, text="WATERMARK TYPE", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        toggle_frame = ttk.Frame(sidebar)
        toggle_frame.pack(fill="x", pady=(0, 20))
        toggle_frame.columnconfigure(0, weight=1)
        toggle_frame.columnconfigure(1, weight=1)

        self.btn_text_mode = ttk.Button(
            toggle_frame,
            text="Text Mode",
            command=lambda: self._set_mode("text")
        )
        self.btn_text_mode.grid(row=0, column=0, sticky="ew", padx=(0, 2))

        self.btn_logo_mode = ttk.Button(
            toggle_frame,
            text="Logo Mode",
            command=lambda: self._set_mode("logo")
        )
        self.btn_logo_mode.grid(row=0, column=1, sticky="ew", padx=(2, 0))

        self.content_container = ttk.Frame(sidebar)
        self.content_container.pack(fill="x", pady=(0, 20))

        self.text_tools = ttk.Frame(self.content_container, style="ToolGroup.TFrame", padding=15)
        ttk.Label(self.text_tools, text="ENTER TEXT", style="Sub.TLabel").pack(anchor="w", pady=(0, 5))

        self.entry_text = ttk.Entry(
            self.text_tools,
            textvariable=self.text_content,
            style="Modern.TEntry",
            font=("Segoe UI", 11)
        )
        self.entry_text.bind("<KeyRelease>", lambda e: self.refresh_preview())
        self.entry_text.pack(fill="x", pady=(0, 10), ipady=8)

        ttk.Button(
            self.text_tools,
            text="🎨 Change Color",
            style="ToggleOff.TButton",
            command=self.pick_color,
        ).pack(fill="x", ipady=3)

        self.logo_tools = ttk.Frame(self.content_container, style="ToolGroup.TFrame", padding=15)
        self.lbl_logo_status = ttk.Label(self.logo_tools, text="No logo selected", style="Sub.TLabel")
        self.lbl_logo_status.pack(anchor="center", pady=(0, 10))

        ttk.Button(
            self.logo_tools,
            text="📂 Load Logo File",
            style="ToggleOff.TButton",
            command=self.load_logo,
        ).pack(fill="x", ipady=5)

        ttk.Label(sidebar, text="SETTINGS", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Label(sidebar, text="Position").pack(anchor="w")
        pos_opts = ["Bottom Right", "Bottom Left", "Top Right", "Top Left", "Center"]
        combo = ttk.Combobox(
            sidebar,
            textvariable=self.position_var,
            values=pos_opts,
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo.pack(fill="x", pady=(5, 15), ipady=3)
        combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_preview())

        self._create_smart_slider(sidebar, "Size Scale (%)", self.size_var, 1, 100)
        self._create_smart_slider(sidebar, "Opacity (%)", self.opacity_var, 0, 100)

        ttk.Frame(sidebar).pack(fill="both", expand=True)

        ttk.Button(
            sidebar,
            text="💾 Save Result",
            style="Action.TButton",
            command=self.save_result,
        ).pack(fill="x", pady=10, ipady=5)

        display_area = ttk.Frame(self.root, style="Main.TFrame")
        display_area.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(
            display_area,
            bg=self.colors["bg_main"],
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)

        self._draw_canvas_placeholder()

    def _create_smart_slider(self, parent, title, variable, min_val, max_val):
        container = ttk.Frame(parent)
        container.pack(fill="x", pady=(0, 15))

        label_frame = ttk.Frame(container)
        label_frame.pack(fill="x", pady=(0, 5))

        title_lbl = ttk.Label(label_frame, text=f"{title}:", style="TLabel")
        title_lbl.pack(side="left")

        val_lbl = ttk.Label(label_frame, text=f"{int(variable.get())}", style="TLabel")
        val_lbl.pack(side="right")

        def on_var_change(*args):
            val_lbl.config(text=f"{int(variable.get())}")

        variable.trace_add("write", on_var_change)

        ctrl_frame = ttk.Frame(container)
        ctrl_frame.pack(fill="x")

        def adjust(delta):
            new_val = variable.get() + delta
            if min_val <= new_val <= max_val:
                variable.set(new_val)
                self.refresh_preview()

        btn_minus = ttk.Button(
            ctrl_frame,
            text="-",
            style="Control.TButton",
            command=lambda: adjust(-1)
        )
        btn_minus.pack(side="left")

        scale = ttk.Scale(
            ctrl_frame,
            from_=min_val,
            to=max_val,
            variable=variable,
            orient="horizontal",
            command=lambda _: self.refresh_preview()
        )
        scale.pack(side="left", fill="x", expand=True, padx=5)

        btn_plus = ttk.Button(
            ctrl_frame,
            text="+",
            style="Control.TButton",
            command=lambda: adjust(1)
        )
        btn_plus.pack(side="right")

    def _draw_canvas_placeholder(self) -> None:
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10: w = 800
        if h < 10: h = 600

        self.canvas.create_text(
            w // 2,
            h // 2,
            text="Open an image to start",
            fill="#444444",
            font=("Segoe UI", 20, "bold"),
            tags="placeholder"
        )

    def _set_mode(self, mode: str) -> None:
        self.mode_var.set(mode)
        self._update_toggle_visuals()
        self._toggle_input_mode()

    def _update_toggle_visuals(self) -> None:
        mode = self.mode_var.get()
        if mode == "text":
            self.btn_text_mode.configure(style="ToggleOn.TButton")
            self.btn_logo_mode.configure(style="ToggleOff.TButton")
        else:
            self.btn_text_mode.configure(style="ToggleOff.TButton")
            self.btn_logo_mode.configure(style="ToggleOn.TButton")

    def _toggle_input_mode(self) -> None:
        if self.mode_var.get() == "text":
            self.logo_tools.pack_forget()
            self.text_tools.pack(fill="x")
        else:
            self.text_tools.pack_forget()
            self.logo_tools.pack(fill="x")
        self.refresh_preview()

    def pick_color(self) -> None:
        color = colorchooser.askcolor(title="Select Watermark Color")
        if color and color[0]:
            self.text_color = tuple(map(int, color[0]))
            self.refresh_preview()

    def load_base_image(self) -> None:
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")],
        )
        if not path:
            return
        try:
            self.base_image = Image.open(path).convert("RGBA")
            self.original_filename = os.path.basename(path)
            self.refresh_preview()
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to load image:\n{exc}")

    def remove_base_image(self) -> None:
        if not self.base_image:
            return
        confirm = messagebox.askyesno(
            "Confirm Removal",
            "Are you sure you want to remove the current image?\nUnsaved changes will be lost."
        )
        if confirm:
            self.base_image = None
            self.processed_image = None
            self.tk_image_ref = None
            self.original_filename = None
            self._draw_canvas_placeholder()

    def load_logo(self) -> None:
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png;*.jpg;*.jpeg")],
        )
        if not path:
            return
        try:
            self.watermark_logo = Image.open(path).convert("RGBA")
            self.lbl_logo_status.config(
                text=os.path.basename(path),
                foreground=self.colors["accent"],
            )
            self.refresh_preview()
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to load logo:\n{exc}")

    def refresh_preview(self) -> None:
        if not self.base_image:
            return

        working_image = self.base_image.copy()
        width, height = working_image.size

        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        scale_percent = self.size_var.get() / 100.0
        opacity_value = int((self.opacity_var.get() / 100.0) * 255)
        padding = int(min(width, height) * 0.03)

        w_obj = 0
        h_obj = 0

        if self.mode_var.get() == "text":
            text_str = self.text_content.get()
            font_size = int(min(width, height) * scale_percent)
            font_size = max(10, font_size)

            try:
                if self.font_path:
                    font = ImageFont.truetype(self.font_path, font_size)
                else:
                    try:
                        font = ImageFont.load_default(size=font_size)
                    except TypeError:
                        font = ImageFont.load_default()
            except OSError:
                font = ImageFont.load_default()

            try:
                bbox = draw.textbbox((0, 0), text_str, font=font)
                w_obj = bbox[2] - bbox[0]
                h_obj = bbox[3] - bbox[1]
            except AttributeError:
                w_obj, h_obj = draw.textsize(text_str, font=font)

            def draw_action(x: int, y: int) -> None:
                fill_color = self.text_color + (opacity_value,)
                draw.text((x, y), text_str, font=font, fill=fill_color)

        else:
            if not self.watermark_logo:
                self.processed_image = working_image
                self._update_canvas()
                return

            target_h = int(min(width, height) * scale_percent)
            target_h = max(10, target_h)

            aspect_ratio = self.watermark_logo.width / self.watermark_logo.height
            target_w = int(target_h * aspect_ratio)

            resized_logo = self.watermark_logo.resize(
                (target_w, target_h),
                Image.Resampling.LANCZOS,
            )

            r, g, b, a = resized_logo.split()
            a = a.point(lambda p: p * (opacity_value / 255.0))
            resized_logo.putalpha(a)

            w_obj = target_w
            h_obj = target_h

            def draw_action(x: int, y: int) -> None:
                overlay.paste(resized_logo, (x, y), resized_logo)

        position_choice = self.position_var.get()
        if position_choice == "Bottom Right":
            pos_x = width - w_obj - padding
            pos_y = height - h_obj - padding
        elif position_choice == "Bottom Left":
            pos_x = padding
            pos_y = height - h_obj - padding
        elif position_choice == "Top Right":
            pos_x = width - w_obj - padding
            pos_y = padding
        elif position_choice == "Top Left":
            pos_x = padding
            pos_y = padding
        else:
            pos_x = (width - w_obj) // 2
            pos_y = (height - h_obj) // 2

        draw_action(int(pos_x), int(pos_y))

        self.processed_image = Image.alpha_composite(working_image, overlay)
        self._update_canvas()

    def _update_canvas(self) -> None:
        if not self.processed_image:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 10 or canvas_height < 10:
            canvas_width, canvas_height = 800, 600

        img_w, img_h = self.processed_image.size
        scale = min(canvas_width / img_w, canvas_height / img_h, 1.0)

        display_w = int(img_w * scale)
        display_h = int(img_h * scale)

        thumbnail = self.processed_image.resize(
            (display_w, display_h),
            Image.Resampling.BICUBIC,
        )

        self.tk_image_ref = ImageTk.PhotoImage(thumbnail)
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            anchor="center",
            image=self.tk_image_ref,
        )

    def _on_resize_debounced(self, event: tk.Event) -> None:
        if event.widget is self.root:
            if self._resize_timer:
                self.root.after_cancel(self._resize_timer)
            self._resize_timer = self.root.after(100, self._handle_resize_event)

    def _handle_resize_event(self) -> None:
        if self.processed_image:
            self._update_canvas()
        else:
            self._draw_canvas_placeholder()

    def save_result(self) -> None:
        if not self.processed_image:
            return

        default_name = "watermarked_image.png"
        if self.original_filename:
            name, ext = os.path.splitext(self.original_filename)
            default_name = f"{name}_watermarked.png"

        path = filedialog.asksaveasfilename(
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")],
        )
        if not path:
            return

        try:
            if path.lower().endswith((".jpg", ".jpeg")):
                bg = Image.new("RGB", self.processed_image.size, (255, 255, 255))
                bg.paste(self.processed_image, mask=self.processed_image.split()[3])
                bg.save(path, quality=95)
            else:
                self.processed_image.save(path)
            messagebox.showinfo("Success", "Image saved successfully.")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not save file:\n{exc}")

if __name__ == "__main__":
    main_window = tk.Tk()
    app = WatermarkApp(main_window)
    main_window.mainloop()
