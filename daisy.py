import tkinter as tk
import random
import math
from PIL import Image, ImageTk, ImageFilter, ImageDraw

# --- Configuration & Styling ---
WIDTH, HEIGHT = 1000, 700  
DAISY_COUNT = 250         
STAR_COUNT = 800          
HORIZON_Y = 400           

BG_COLOR = "#050508"      
SK_TOP = "#020204"        
SK_BOTTOM = "#1a0f30"     
GRASS_DEEP = "#071a07"    
GRASS_LIGHT = "#123312"   
TEXT_COLOR = "#fffd91"    

class AnimatedNightScene:
    def __init__(self, root):
        self.root = root
        self.root.title("A Beautiful Night - Laying Under the Stars")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.sky_y = 0
        self.stars_drawn = 0
        self.daisies_to_draw = []
        
        # Keep a reference to the image so it doesn't get garbage collected
        self.tk_eyes_img = None 
        
        self.root.after(500, self.animate_sky)

    def animate_sky(self):
        chunk_size = 5
        for _ in range(chunk_size):
            if self.sky_y <= HORIZON_Y:
                ratio = self.sky_y / HORIZON_Y
                r = int(2 + (int(SK_BOTTOM[1:3], 16) - 2) * ratio)
                g = int(2 + (int(SK_BOTTOM[3:5], 16) - 2) * ratio)
                b = int(4 + (int(SK_BOTTOM[5:7], 16) - 4) * ratio)
                color = f'#{r:02x}{g:02x}{b:02x}'
                self.canvas.create_line(0, self.sky_y, WIDTH, self.sky_y, fill=color, width=1)
                self.sky_y += 1
        
        if self.sky_y <= HORIZON_Y:
            self.root.after(10, self.animate_sky)
        else:
            self.blend_eyes_image()
            self.draw_landscape()
            self.root.after(100, self.animate_stars)

    def blend_eyes_image(self):
        """Beautifully smudges and dissolves the eyes image into the night sky."""
        try:
            img_name = "810246178_2224115828156214_1799929967203399057_n.jpg"
            img = Image.open(img_name).convert("RGBA")
            
            # Resize the image to span gracefully across the sky
            target_width = 750
            w_percent = (target_width / float(img.size[0]))
            target_height = int((float(img.size[1]) * float(w_percent)))
            
            # Use Resampling.LANCZOS for high-quality resizing in modern Pillow versions
            # (Fallback to ANTIALIAS for older Pillow versions)
            try:
                resample_filter = Image.Resampling.LANCZOS
            except AttributeError:
                resample_filter = Image.ANTIALIAS
                
            img = img.resize((target_width, target_height), resample_filter)

            # Create a fading mask to smudge/dissolve the hard edges perfectly
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            
            # Draw a solid white ellipse in the middle (smaller than the image to allow for a huge blur)
            margin_x, margin_y = 60, 60
            draw.ellipse((margin_x, margin_y, target_width - margin_x, target_height - margin_y), fill=255)
            
            # Apply an extreme Gaussian blur to create the soft, dissolved edge effect
            mask = mask.filter(ImageFilter.GaussianBlur(40))
            
            # Reduce overall opacity to ~45% so it looks ghostly and ethereal in the sky
            mask = mask.point(lambda p: p * 0.45)
            
            # Apply the mask to the image
            img.putalpha(mask)

            # Display on canvas (placed high in the sky)
            self.tk_eyes_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(WIDTH//2, HORIZON_Y//2 - 20, image=self.tk_eyes_img, anchor="center")
            
        except Exception as e:
            print(f"Note: Could not load '{img_name}'. Make sure it is in the same folder.")
            print(f"Error details: {e}")

    def draw_landscape(self):
        self.canvas.create_polygon(
            0, HORIZON_Y, WIDTH/2, HORIZON_Y - 30, WIDTH, HORIZON_Y, 
            WIDTH, HEIGHT, 0, HEIGHT, fill=GRASS_DEEP, outline=""
        )
        self.canvas.create_polygon(
            0, HORIZON_Y+80, WIDTH, HORIZON_Y+50, WIDTH, HEIGHT, 
            0, HEIGHT, fill=GRASS_LIGHT, outline=""
        )

    def animate_stars(self):
        # The stars draw ON TOP of the dissolved eyes, making it look like a galaxy!
        chunk_size = 20
        for _ in range(chunk_size):
            if self.stars_drawn < STAR_COUNT:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HORIZON_Y)
                size = random.uniform(0.5, 2.0)
                brightness = random.randint(150, 255)
                color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
                self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color)
                self.stars_drawn += 1
        
        if self.stars_drawn < STAR_COUNT:
            self.root.after(20, self.animate_stars)
        else:
            mx, my = 120, 80
            self.canvas.create_oval(mx, my, mx+50, my+50, fill="#ffffdd", outline="")
            self.canvas.create_oval(mx+12, my+3, mx+60, my+50, fill=SK_TOP, outline="") 
            self.root.after(300, self.animate_text)

    def animate_text(self):
        base_font = ("Arial Rounded MT Bold", 70, "bold")
        self.canvas.create_text(
            WIDTH/2, HORIZON_Y - 100, 
            text="I LOVE YOU", fill=TEXT_COLOR, font=base_font
        )
        self.root.after(500, self.draw_anime_couple)

    def draw_anime_couple(self):
        cx, cy = WIDTH / 2, HEIGHT - 140 
        skin_color = "#ffe0bd"
        
        # ==========================================
        # --- GIRL (Left Side) ---
        # ==========================================
        gx, gy = cx - 70, cy
        hair_color = "#151515" 
        
        # Back Hair 
        self.canvas.create_oval(gx-55, gy-50, gx+45, gy+50, fill=hair_color, outline="") 
        self.canvas.create_polygon(gx-45, gy-10, gx-80, gy+80, gx-10, gy+90, fill=hair_color, outline="", smooth=True) 
        self.canvas.create_polygon(gx+20, gy, gx+60, gy+70, gx+10, gy+80, fill=hair_color, outline="", smooth=True)
        
        # Body
        self.canvas.create_oval(gx-45, gy+10, gx+35, gy+90, fill="#f4a4b4", outline="")
        self.canvas.create_polygon(gx-15, gy+10, gx+10, gy+10, gx-5, gy+30, fill="white", outline="")
        self.canvas.create_polygon(gx-25, gy+20, gx+5, gy+25, gx-5, gy+40, fill="#c72c35", outline="")
        self.canvas.create_polygon(gx+15, gy+20, gx-5, gy+25, gx+5, gy+40, fill="#c72c35", outline="")
        self.canvas.create_oval(gx-8, gy+20, gx+2, gy+30, fill="#a11a22", outline="") 
        
        # Face Skin 
        self.canvas.create_oval(gx-35, gy-35, gx+30, gy+30, fill=skin_color, outline="")
        
        # Front Bangs 
        self.canvas.create_polygon(gx-25, gy-40, gx-5, gy-22, gx+15, gy-40, fill=hair_color, outline="", smooth=True)
        self.canvas.create_polygon(gx-5, gy-40, gx+15, gy-20, gx+25, gy-40, fill=hair_color, outline="", smooth=True)
        self.canvas.create_polygon(gx-35, gy-35, gx-20, gy-15, gx-38, gy+5, fill=hair_color, outline="", smooth=True)
        self.canvas.create_polygon(gx+25, gy-35, gx+15, gy-15, gx+35, gy+5, fill=hair_color, outline="", smooth=True)
        self.canvas.create_polygon(gx-38, gy-15, gx-30, gy-20, gx-33, gy-10, fill="#32a852", outline="") 
        
        # Eyes
        self.canvas.create_oval(gx-20, gy-14, gx-6, gy+2, fill="white", outline="")
        self.canvas.create_oval(gx-14, gy-12, gx-6, gy-2, fill="#333", outline="") 
        self.canvas.create_oval(gx-10, gy-10, gx-8, gy-6, fill="white", outline="") 
        self.canvas.create_arc(gx-22, gy-16, gx-4, gy, start=0, extent=120, outline="#111", width=2, style='arc') 

        self.canvas.create_oval(gx+4, gy-14, gx+18, gy+2, fill="white", outline="")
        self.canvas.create_oval(gx+6, gy-12, gx+14, gy-2, fill="#333", outline="") 
        self.canvas.create_oval(gx+10, gy-10, gx+12, gy-6, fill="white", outline="") 
        self.canvas.create_arc(gx+2, gy-16, gx+20, gy, start=60, extent=120, outline="#111", width=2, style='arc') 
        
        # Eyebrows
        self.canvas.create_arc(gx-18, gy-20, gx-8, gy-14, start=45, extent=90, outline=hair_color, width=1.5, style='arc')
        self.canvas.create_arc(gx+8, gy-20, gx+18, gy-14, start=45, extent=90, outline=hair_color, width=1.5, style='arc')

        # Blush & Smile
        self.canvas.create_oval(gx-24, gy, gx-12, gy+8, fill="#ff8a99", outline="", stipple="gray50")
        self.canvas.create_oval(gx+12, gy, gx+24, gy+8, fill="#ff8a99", outline="", stipple="gray50")
        self.canvas.create_arc(gx-8, gy+10, gx+8, gy+18, start=180, extent=180, outline="#8B3A3A", width=2, style='arc')

        # Girl's Text
        self.canvas.create_text(
            gx - 130, gy, 
            text="the most beautifull\nwoman", 
            fill="#ffb3c6", font=("Georgia", 13, "italic"), justify="center"
        )


        # ==========================================
        # --- BOY (Right Side) ---
        # ==========================================
        bx, by = cx + 70, cy
        
        # 1. Back Hair (Made significantly wider and fuller)
        self.canvas.create_oval(bx-55, by-55, bx+55, by+25, fill="#111", outline="") 
        
        # Massive messy hair volume via sweeping polygons on the sides and top
        self.canvas.create_polygon(bx-45, by-30, bx-70, by-50, bx-25, by-55, fill="#111", outline="", smooth=True)
        self.canvas.create_polygon(bx-25, by-55, bx-20, by-85, bx+10, by-60, fill="#111", outline="", smooth=True)
        self.canvas.create_polygon(bx+5, by-60, bx+25, by-85, bx+35, by-50, fill="#111", outline="", smooth=True)
        self.canvas.create_polygon(bx+30, by-50, bx+70, by-45, bx+45, by-20, fill="#111", outline="", smooth=True)
        
        # Body
        self.canvas.create_oval(bx-35, by+10, bx+45, by+90, fill="#1c1c1e", outline="")
        self.canvas.create_polygon(bx-10, by+10, bx+20, by+15, bx+5, by+30, fill="#f0f0f0", outline="")
        self.canvas.create_polygon(bx+25, by+10, bx-5, by+15, bx+5, by+30, fill="#f0f0f0", outline="")
        
        # Face Skin 
        self.canvas.create_oval(bx-30, by-35, bx+35, by+30, fill=skin_color, outline="") 
        
        # Front Bangs overlapping the forehead
        self.canvas.create_polygon(bx-20, by-40, bx-10, by-20, bx, by-40, fill="#111", outline="", smooth=True)
        self.canvas.create_polygon(bx-5, by-40, bx+5, by-15, bx+15, by-40, fill="#111", outline="", smooth=True)
        self.canvas.create_polygon(bx+10, by-40, bx+20, by-22, bx+30, by-40, fill="#111", outline="", smooth=True)
        
        # Sideburns / Side hair framing the face
        self.canvas.create_polygon(bx-35, by-20, bx-35, by, bx-25, by-20, fill="#111", outline="", smooth=True)
        self.canvas.create_polygon(bx+35, by-20, bx+40, by-5, bx+25, by-20, fill="#111", outline="", smooth=True)
        
        # Glasses 
        gl_r = 15
        self.canvas.create_oval(bx-25, by-12, bx-25+gl_r*2, by-12+gl_r*2, outline="#fff", width=2, fill="#dceeff", stipple="gray12")
        self.canvas.create_oval(bx+5, by-12, bx+5+gl_r*2, by-12+gl_r*2, outline="#fff", width=2, fill="#dceeff", stipple="gray12")
        self.canvas.create_line(bx-25+gl_r*2, by+2, bx+5, by+2, fill="#fff", width=2) 
        
        # Eyes
        self.canvas.create_oval(bx-22, by-8, bx-10, by+4, fill="white", outline="")
        self.canvas.create_oval(bx+8, by-8, bx+20, by+4, fill="white", outline="")
        
        # Pupils gazing left
        self.canvas.create_oval(bx-22, by-6, bx-16, by+2, fill="#111", outline="")
        self.canvas.create_oval(bx+8, by-6, bx+14, by+2, fill="#111", outline="")
        
        # Blush & Smile
        self.canvas.create_oval(bx-26, by+6, bx-16, by+12, fill="#ff8a99", outline="", stipple="gray50")
        self.canvas.create_oval(bx+16, by+6, bx+26, by+12, fill="#ff8a99", outline="", stipple="gray50")
        self.canvas.create_arc(bx-10, by+12, bx+10, by+20, start=180, extent=180, outline="#111", width=2, style='arc')

        # Boy's Text
        self.canvas.create_text(
            bx + 140, by, 
            text="the nearest and beautifull\nstar for me ,sara", 
            fill="#dceeff", font=("Georgia", 13, "italic"), justify="center"
        )

        self.prepare_daisies()
        self.root.after(600, self.animate_daisies)

    def prepare_daisies(self):
        for _ in range(DAISY_COUNT):
            dx = random.randint(0, WIDTH)
            dy = random.randint(HORIZON_Y + 20, HEIGHT)
            
            if (WIDTH * 0.2 < dx < WIDTH * 0.8) and (HEIGHT * 0.65 < dy < HEIGHT):
                continue 
            
            depth = (dy - HORIZON_Y) / (HEIGHT - HORIZON_Y)
            size = random.uniform(4, 15) * (0.5 + depth * 0.5)
            self.daisies_to_draw.append((dx, dy, size, depth))
            
        self.daisies_to_draw.sort(key=lambda d: d[1])

    def animate_daisies(self):
        chunk = 3 
        for _ in range(chunk):
            if self.daisies_to_draw:
                dx, dy, size, depth = self.daisies_to_draw.pop(0)
                self.draw_single_daisy(dx, dy, size, depth)
            
        if self.daisies_to_draw:
            self.root.after(15, self.animate_daisies)
        else:
            print("Beautiful Generation Complete!")

    def draw_single_daisy(self, x, y, size, depth):
        brightness = 0.6 + (depth * 0.4)
        c_r, c_g, c_b = int(255*brightness), int(215*brightness), 0
        p_val = int(255 * brightness)
        petal_color = f'#{p_val:02x}{p_val:02x}{p_val:02x}'
        center_color = f'#{c_r:02x}{c_g:02x}{c_b:02x}'
        
        if random.random() < 0.15:
            colors = ["#FFD700", "#FF69B4", "#9370DB"]
            w_color = random.choice(colors)
            pr, pg, pb = int(int(w_color[1:3], 16)*brightness), int(int(w_color[3:5], 16)*brightness), int(int(w_color[5:7], 16)*brightness)
            petal_color = f'#{pr:02x}{pg:02x}{pb:02x}'
            
        petal_len = size * 0.8
        petal_wid = size * 0.3
        
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            self.canvas.create_oval(
                x - petal_wid + (petal_len * math.cos(angle)),
                y - petal_wid + (petal_len * math.sin(angle)),
                x + petal_wid + (petal_len * math.cos(angle)),
                y + petal_wid + (petal_len * math.sin(angle)),
                fill=petal_color, outline=""
            )
            
        c_size = size * 0.4
        self.canvas.create_oval(x-c_size, y-c_size, x+c_size, y+c_size, fill=center_color, outline="")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimatedNightScene(root)
    root.mainloop()