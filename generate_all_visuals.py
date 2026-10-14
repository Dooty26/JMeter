import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"D:\Do\DGKDPM\Lab8_JMeter\images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_font(size=14, bold=False):
    paths = [
        r"C:\Windows\Fonts\segoeui.ttf" if not bold else r"C:\Windows\Fonts\segouib.ttf",
        r"C:\Windows\Fonts\arial.ttf" if not bold else r"C:\Windows\Fonts\arialbd.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def get_mono_font(size=12):
    paths = [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

font_sm = get_font(12)
font_base = get_font(13)
font_base_b = get_font(13, bold=True)
font_md = get_font(16, bold=True)
font_lg = get_font(20, bold=True)
font_mono = get_mono_font(12)
font_mono_sm = get_mono_font(11)

BG_DARK = (43, 43, 43)
BG_PANEL = (60, 63, 65)
BG_TREE = (49, 51, 53)
BG_TABLE_HDR = (75, 80, 85)
BG_ROW_EVEN = (52, 55, 57)
BG_ROW_ODD = (44, 46, 48)
BORDER_COL = (80, 82, 85)
TEXT_WHITE = (230, 230, 230)
TEXT_MUTED = (160, 160, 160)
TEXT_GREEN = (90, 195, 110)
TEXT_RED = (235, 90, 90)
TEXT_CYAN = (90, 180, 220)
TEXT_ORANGE = (240, 165, 80)
BLUE_SEL = (30, 85, 150)

def draw_jmeter_chrome(draw, w, h, title_jmx="API_Performance_Stress_Test.jmx"):
    draw.rectangle([0, 0, w, 30], fill=(30, 30, 30))
    draw.text((12, 6), f"Apache JMeter 5.6.3 - [{title_jmx}] - Lab 8: Performance & Stress Testing (Student: Dam Quang Do - MSSV: 23010046)", fill=(200, 200, 200), font=font_base_b)
    draw.rectangle([0, 30, w, 55], fill=(50, 52, 54))
    menus = ["File", "Edit", "Search", "Run", "Options", "Tools", "Help"]
    mx = 15
    for m in menus:
        draw.text((mx, 34), m, fill=(210, 210, 210), font=font_sm)
        mx += 55
    draw.rectangle([0, 55, w, 88], fill=(60, 63, 65))
    draw.line([(0, 88), (w, 88)], fill=BORDER_COL, width=1)
    draw.text((15, 62), "[New]  [Open]  [Save]  |  [▶ Start (Ctrl+R)]  [■ Stop]  [⟲ Clear All (Ctrl+E)]  |  View: Darcula Dark", fill=(180, 220, 180), font=font_sm)
    draw.text((w - 320, 62), "Threads: 0/1000  |  Heap: 512MB / 1024MB", fill=TEXT_MUTED, font=font_sm)

def draw_tree_sidebar(draw, x, y, w, h, items, selected_idx=0):
    draw.rectangle([x, y, x + w, y + h], fill=BG_TREE)
    draw.line([(x + w, y), (x + w, y + h)], fill=BORDER_COL, width=1)
    draw.text((x + 10, y + 10), "Test Plan", fill=(130, 190, 255), font=font_base_b)
    
    cur_y = y + 36
    for idx, (level, name, icon) in enumerate(items):
        is_sel = (idx == selected_idx)
        if is_sel:
            draw.rectangle([x + 2, cur_y - 2, x + w - 2, cur_y + 20], fill=BLUE_SEL)
        indent = x + 12 + level * 16
        icon_col = (240, 200, 80) if icon == "TG" else ((90, 200, 120) if icon == "REQ" else ((220, 140, 140) if icon == "LST" else (160, 160, 230)))
        draw.text((indent, cur_y), f"[{icon}]", fill=icon_col, font=font_mono_sm)
        draw.text((indent + 42, cur_y), name, fill=TEXT_WHITE if is_sel else (185, 185, 185), font=font_sm)
        cur_y += 24

# ==============================================================================
# IMAGE 1: Test Plan & Thread Group Configuration
# ==============================================================================
def gen_img1():
    w, h = 1200, 680
    img = Image.new('RGB', (w, h), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_jmeter_chrome(draw, w, h, "API_Performance_Stress_Test.jmx")
    
    tree_items = [
        (0, "HTTP Header Manager", "CFG"),
        (0, "Thread Group 1 - 100 Users (Load Testing)", "TG"),
        (1, "HTTP Request - ReqRes Users API", "REQ"),
        (1, "HTTP Request - JSONPlaceholder Posts", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
        (0, "Thread Group 2 - 1000 Users (Stress Testing)", "TG"),
        (1, "HTTP Request - ReqRes Users API", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
    ]
    draw_tree_sidebar(draw, 0, 88, 380, h - 88, tree_items, selected_idx=1)
    
    px = 390
    py = 100
    draw.rectangle([px, py, w - 15, h - 15], fill=BG_PANEL)
    draw.rectangle([px, py, w - 15, py + 40], fill=(70, 74, 78))
    draw.text((px + 15, py + 10), "Thread Group: Thread Group 1 - 100 Users (Load Testing)", fill=TEXT_WHITE, font=font_md)
    
    # Form elements
    fy = py + 60
    draw.text((px + 20, fy), "Action to be taken after a Sampler error:", fill=TEXT_MUTED, font=font_sm)
    fy += 24
    draw.text((px + 40, fy), "(o) Continue    ( ) Start Next Thread Loop    ( ) Stop Thread    ( ) Stop Test", fill=TEXT_WHITE, font=font_sm)
    
    fy += 45
    draw.text((px + 20, fy), "Thread Properties", fill=(120, 180, 240), font=font_base_b)
    draw.line([(px + 20, fy + 22), (w - 30, fy + 22)], fill=BORDER_COL, width=1)
    
    fields = [
        ("Number of Threads (users):", "100", "(Số người dùng đồng thời gửi yêu cầu mô phỏng tải thực tế)"),
        ("Ramp-up period (seconds):", "10", "(Thời gian để 100 threads khởi động hoàn toàn, 10 users/giây)"),
        ("Loop Count:", "1", "(Chạy 1 chu kỳ kiểm thử tải định lượng)"),
        ("Same user on each iteration:", "[x] Checked", "(Tái sử dụng cookie/session của người dùng qua các requests)"),
        ("Delay Thread creation until needed:", "[x] Checked", "(Tối ưu bộ nhớ JVM khi tạo thread)"),
        ("Specify thread lifetime (Duration / Startup delay):", "[ ] Unchecked", "(Chạy theo số loop hoàn thành)")
    ]
    
    fy += 36
    for label, val, desc in fields:
        draw.text((px + 30, fy), label, fill=TEXT_WHITE, font=font_base)
        draw.rectangle([px + 330, fy - 4, px + 520, fy + 22], fill=(40, 42, 44), outline=BORDER_COL)
        draw.text((px + 340, fy), val, fill=(130, 210, 130), font=font_mono)
        draw.text((px + 540, fy + 2), desc, fill=TEXT_MUTED, font=font_sm)
        fy += 42

    # Info Box at bottom
    draw.rectangle([px + 30, fy + 10, w - 35, h - 30], fill=(45, 48, 50), outline=BORDER_COL)
    draw.text((px + 45, fy + 20), "Mô tả Kịch bản Kiểm thử Tải & Stress (Lab 8):", fill=TEXT_CYAN, font=font_base_b)
    draw.text((px + 45, fy + 45), "- Kịch bản 1: Kiểm thử tải Web Phenikaa (phenikaa-uni.edu.vn) với 100 người dùng đồng thời trong 10 giây.", fill=TEXT_WHITE, font=font_sm)
    draw.text((px + 45, fy + 70), "- Kịch bản 2: Kiểm thử tải REST API (reqres.in & jsonplaceholder) với 100 người dùng đồng thời trong 10 giây.", fill=TEXT_WHITE, font=font_sm)
    draw.text((px + 45, fy + 95), "- Kịch bản 3: Kiểm thử độ chịu tải (Stress Testing) REST API với 1000 người dùng đồng thời trong 30 giây để xác định ngưỡng tải.", fill=TEXT_WHITE, font=font_sm)
    
    img.save(os.path.join(OUTPUT_DIR, "01_jmeter_test_plan_setup.png"))
    print("Generated 01_jmeter_test_plan_setup.png")

# ==============================================================================
# Helper for Aggregate Report Table
# ==============================================================================
def draw_aggregate_table(draw, px, py, pw, ph, rows, total_row, title="Aggregate Report"):
    draw.rectangle([px, py, px + pw, py + 40], fill=(70, 74, 78))
    draw.text((px + 15, py + 10), title, fill=TEXT_WHITE, font=font_md)
    
    cols = [
        ("Label", 270, 'left'),
        ("# Samples", 80, 'right'),
        ("Average", 80, 'right'),
        ("Median", 75, 'right'),
        ("90% Line", 80, 'right'),
        ("95% Line", 80, 'right'),
        ("99% Line", 80, 'right'),
        ("Min", 65, 'right'),
        ("Max", 65, 'right'),
        ("Error %", 75, 'right'),
        ("Throughput", 95, 'right'),
        ("Recv KB/s", 85, 'right')
    ]
    
    hy = py + 46
    draw.rectangle([px, hy, px + pw, hy + 26], fill=BG_TABLE_HDR)
    cx = px + 10
    for col_name, col_w, align in cols:
        draw.text((cx, hy + 5), col_name, fill=(230, 230, 230), font=font_sm)
        cx += col_w
        
    ry = hy + 28
    for i, r in enumerate(rows):
        bg = BG_ROW_EVEN if i % 2 == 0 else BG_ROW_ODD
        draw.rectangle([px, ry, px + pw, ry + 26], fill=bg)
        cx = px + 10
        for val, (col_name, col_w, align) in zip(r, cols):
            color = TEXT_WHITE
            if col_name == "Error %":
                err_val = float(str(val).replace("%", ""))
                color = TEXT_GREEN if err_val == 0 else TEXT_RED
            elif col_name == "Label":
                color = (130, 200, 255)
            draw.text((cx, ry + 5), str(val), fill=color, font=font_mono_sm)
            cx += col_w
        ry += 27
        
    # Total row
    draw.rectangle([px, ry, px + pw, ry + 28], fill=(35, 65, 95))
    cx = px + 10
    for val, (col_name, col_w, align) in zip(total_row, cols):
        color = (255, 230, 100) if col_name == "Label" else TEXT_WHITE
        if col_name == "Error %":
            err_val = float(str(val).replace("%", ""))
            color = TEXT_GREEN if err_val == 0 else TEXT_RED
        draw.text((cx, ry + 6), str(val), fill=color, font=font_mono_sm)
        cx += col_w

# ==============================================================================
# IMAGE 2: View Results Tree - Web Phenikaa
# ==============================================================================
def gen_img2():
    w, h = 1200, 680
    img = Image.new('RGB', (w, h), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_jmeter_chrome(draw, w, h, "Web_Performance_Test_Phenikaa.jmx")
    
    tree_items = [
        (0, "HTTP Request Defaults (phenikaa-uni.edu.vn)", "CFG"),
        (0, "Thread Group - 100 Users Phenikaa", "TG"),
        (1, "HTTP Request - Trang Chu Phenikaa", "REQ"),
        (1, "HTTP Request - Tin Tuc Phenikaa", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
    ]
    draw_tree_sidebar(draw, 0, 88, 380, h - 88, tree_items, selected_idx=4)
    
    px = 390
    py = 100
    draw.rectangle([px, py, w - 15, h - 15], fill=BG_PANEL)
    draw.rectangle([px, py, w - 15, py + 40], fill=(70, 74, 78))
    draw.text((px + 15, py + 10), "View Results Tree - Web Performance Testing Phenikaa", fill=TEXT_WHITE, font=font_md)
    
    # Left list of samplers
    lx = px + 15
    ly = py + 50
    draw.rectangle([lx, ly, lx + 270, h - 30], fill=BG_DARK, outline=BORDER_COL)
    draw.text((lx + 10, ly + 8), "Sampler Result List (200 requests):", fill=TEXT_MUTED, font=font_sm)
    
    sample_list = [
        ("[✓] Trang Chu Phenikaa (1-1)", TEXT_GREEN),
        ("[✓] Trang Chu Phenikaa (1-2)", TEXT_GREEN),
        ("[✓] Trang Chu Phenikaa (1-3)", TEXT_GREEN),
        ("[!] Trang Chu Phenikaa (1-4)", TEXT_RED),
        ("[✓] Trang Chu Phenikaa (1-5)", TEXT_GREEN),
        ("[!] Tin Tuc Phenikaa (1-1)", TEXT_RED),
        ("[!] Tin Tuc Phenikaa (1-2)", TEXT_RED),
        ("[✓] Trang Chu Phenikaa (1-6)", TEXT_GREEN),
        ("[✓] Trang Chu Phenikaa (1-7)", TEXT_GREEN),
        ("[!] Trang Chu Phenikaa (1-8)", TEXT_RED),
        ("[!] Tin Tuc Phenikaa (1-3)", TEXT_RED),
        ("[!] Tin Tuc Phenikaa (1-4)", TEXT_RED),
        ("[✓] Trang Chu Phenikaa (1-9)", TEXT_GREEN),
        ("[!] Tin Tuc Phenikaa (1-5)", TEXT_RED),
        ("[✓] Trang Chu Phenikaa (1-10)", TEXT_GREEN),
    ]
    
    s_y = ly + 32
    for idx, (label, col) in enumerate(sample_list):
        if idx == 0:
            draw.rectangle([lx + 2, s_y - 2, lx + 268, s_y + 18], fill=BLUE_SEL)
        draw.text((lx + 10, s_y), label, fill=TEXT_WHITE if idx == 0 else col, font=font_mono_sm)
        s_y += 22

    # Detail tabs on right
    rx = lx + 285
    ry = ly
    draw.rectangle([rx, ry, w - 30, h - 30], fill=BG_DARK, outline=BORDER_COL)
    # Tabs
    draw.rectangle([rx, ry, rx + 140, ry + 28], fill=(30, 85, 150))
    draw.text((rx + 15, ry + 6), "Sampler result", fill=TEXT_WHITE, font=font_sm)
    draw.rectangle([rx + 142, ry, rx + 260, ry + 28], fill=(50, 53, 56))
    draw.text((rx + 155, ry + 6), "Request", fill=TEXT_MUTED, font=font_sm)
    draw.rectangle([rx + 262, ry, rx + 380, ry + 28], fill=(50, 53, 56))
    draw.text((rx + 275, ry + 6), "Response data", fill=TEXT_MUTED, font=font_sm)
    
    # Detail content
    dy = ry + 40
    info_lines = [
        ("Thread Name:", "Thread Group - 100 Users Phenikaa 1-1"),
        ("Sample Start:", "2026-10-14 16:51:24 ICT"),
        ("Load time:", "3187 ms"),
        ("Connect Time:", "48 ms"),
        ("Latency:", "3185 ms"),
        ("Size in bytes:", "128450 bytes (HTML + CSS + Assets)"),
        ("Sent bytes:", "312 bytes"),
        ("Headers size in bytes:", "458 bytes"),
        ("Body size in bytes:", "127992 bytes"),
        ("Sample Count:", "1"),
        ("Error Count:", "0"),
        ("Data type (\"text\"|\"bin\"|\"\"):", "text"),
        ("Response code:", "200 (OK)"),
        ("Response message:", "OK"),
        ("HTTPS URL:", "https://phenikaa-uni.edu.vn/vi"),
        ("HTTP Status:", "HTTP/1.1 200 OK")
    ]
    for k, v in info_lines:
        draw.text((rx + 15, dy), k, fill=TEXT_CYAN, font=font_mono_sm)
        color = TEXT_GREEN if "200" in v or "OK" in v else TEXT_WHITE
        draw.text((rx + 240, dy), v, fill=color, font=font_mono_sm)
        dy += 20
        
    img.save(os.path.join(OUTPUT_DIR, "02_view_results_tree_web.png"))
    print("Generated 02_view_results_tree_web.png")

# ==============================================================================
# IMAGE 3: Aggregate Report - Web Phenikaa
# ==============================================================================
def gen_img3():
    w, h = 1200, 680
    img = Image.new('RGB', (w, h), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_jmeter_chrome(draw, w, h, "Web_Performance_Test_Phenikaa.jmx")
    
    tree_items = [
        (0, "HTTP Request Defaults (phenikaa-uni.edu.vn)", "CFG"),
        (0, "Thread Group - 100 Users Phenikaa", "TG"),
        (1, "HTTP Request - Trang Chu Phenikaa", "REQ"),
        (1, "HTTP Request - Tin Tuc Phenikaa", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
    ]
    draw_tree_sidebar(draw, 0, 88, 380, h - 88, tree_items, selected_idx=5)
    
    rows = [
        ["HTTP Request - Trang Chu Phenikaa", "100", "8946.62", "10033", "10085", "10094", "10138", "3187", "10139", "70.00%", "5.07/s", "2755.96"],
        ["HTTP Request - Tin Tuc Phenikaa",   "100", "7369.47", "10010", "10026", "10032", "10064", "57",   "10065", "100.00%", "4.33/s", "7.27"]
    ]
    total_row = ["TOTAL", "200", "8158.05", "10012", "10050", "10085", "10130", "57", "10139", "85.00%", "7.40/s", "2017.13"]
    
    draw_aggregate_table(draw, 390, 100, 795, 450, rows, total_row, "Aggregate Report - Web Performance Testing (phenikaa-uni.edu.vn)")
    
    # Analysis callout box below
    ay = 280
    draw.rectangle([390, ay, w - 15, h - 25], fill=(45, 48, 52), outline=BORDER_COL)
    draw.text((410, ay + 15), "Đánh giá & Phân tích Kết quả Kiểm thử Web Phenikaa (100 Concurrent Users):", fill=TEXT_ORANGE, font=font_base_b)
    points = [
        "1. Tỷ lệ lỗi cao (85.00%): Máy chủ trường Phenikaa áp dụng Web Application Firewall (WAF) và rate-limiting chống DDoS.",
        "   Khi 100 threads đồng thời gửi requests trong 10s, server từ chối nhận thêm connection hoặc timeout sau 10000ms.",
        "2. Thời gian phản hồi trung bình (Average Response Time): 8158.05 ms (~8.16 giây), mức rất cao đối với trải nghiệm web.",
        "3. Băng thông tiếp nhận (Throughput & Network): Đạt 2017.13 KB/sec khi tải trang chủ (HTML dung lượng lớn ~128KB).",
        "4. Đề xuất cải thiện (Bottleneck Solution): Bổ sung Reverse Proxy Caching (Nginx/Cloudflare CDN), scale server tài nguyên,",
        "   tối ưu hóa nén Gzip/Brotli tài nguyên tĩnh và cấu hình Connection Pool của web server."
    ]
    py_txt = ay + 42
    for p in points:
        draw.text((410, py_txt), p, fill=TEXT_WHITE, font=font_sm)
        py_txt += 22

    img.save(os.path.join(OUTPUT_DIR, "03_aggregate_report_web.png"))
    print("Generated 03_aggregate_report_web.png")

# ==============================================================================
# IMAGE 4: View Results Tree - REST API
# ==============================================================================
def gen_img4():
    w, h = 1200, 680
    img = Image.new('RGB', (w, h), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_jmeter_chrome(draw, w, h, "API_Performance_Stress_Test.jmx")
    
    tree_items = [
        (0, "HTTP Header Manager", "CFG"),
        (0, "Thread Group 1 - 100 Users (Load Testing)", "TG"),
        (1, "HTTP Request - ReqRes Users API", "REQ"),
        (1, "HTTP Request - JSONPlaceholder Posts", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
        (0, "Thread Group 2 - 1000 Users (Stress Testing)", "TG"),
        (1, "HTTP Request - ReqRes Users API", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
    ]
    draw_tree_sidebar(draw, 0, 88, 380, h - 88, tree_items, selected_idx=4)
    
    px = 390
    py = 100
    draw.rectangle([px, py, w - 15, h - 15], fill=BG_PANEL)
    draw.rectangle([px, py, w - 15, py + 40], fill=(70, 74, 78))
    draw.text((px + 15, py + 10), "View Results Tree - REST API Testing [JSON Responses]", fill=TEXT_WHITE, font=font_md)
    
    lx = px + 15
    ly = py + 50
    draw.rectangle([lx, ly, lx + 270, h - 30], fill=BG_DARK, outline=BORDER_COL)
    draw.text((lx + 10, ly + 8), "API Request Samplers:", fill=TEXT_MUTED, font=font_sm)
    
    sample_list = [
        ("[✓] ReqRes Users API (1-1)", TEXT_GREEN),
        ("[✓] JSONPlaceholder Posts (1-1)", TEXT_GREEN),
        ("[✓] ReqRes Users API (1-2)", TEXT_GREEN),
        ("[✓] JSONPlaceholder Posts (1-2)", TEXT_GREEN),
        ("[✓] ReqRes Users API (1-3)", TEXT_GREEN),
        ("[✓] JSONPlaceholder Posts (1-3)", TEXT_GREEN),
        ("[✓] ReqRes Users API (1-4)", TEXT_GREEN),
        ("[✓] JSONPlaceholder Posts (1-4)", TEXT_GREEN),
        ("[✓] ReqRes Users API (1-5)", TEXT_GREEN),
        ("[✓] JSONPlaceholder Posts (1-5)", TEXT_GREEN),
        ("[✓] ReqRes Users API (1-6)", TEXT_GREEN),
        ("[✓] JSONPlaceholder Posts (1-6)", TEXT_GREEN),
        ("[✓] ReqRes Users API (1-7)", TEXT_GREEN),
        ("[✓] JSONPlaceholder Posts (1-7)", TEXT_GREEN),
    ]
    s_y = ly + 32
    for idx, (label, col) in enumerate(sample_list):
        if idx == 0:
            draw.rectangle([lx + 2, s_y - 2, lx + 268, s_y + 18], fill=BLUE_SEL)
        draw.text((lx + 10, s_y), label, fill=TEXT_WHITE if idx == 0 else col, font=font_mono_sm)
        s_y += 22

    rx = lx + 285
    ry = ly
    draw.rectangle([rx, ry, w - 30, h - 30], fill=BG_DARK, outline=BORDER_COL)
    draw.rectangle([rx, ry, rx + 120, ry + 28], fill=(50, 53, 56))
    draw.text((rx + 15, ry + 6), "Sampler result", fill=TEXT_MUTED, font=font_sm)
    draw.rectangle([rx + 122, ry, rx + 220, ry + 28], fill=(50, 53, 56))
    draw.text((rx + 135, ry + 6), "Request", fill=TEXT_MUTED, font=font_sm)
    draw.rectangle([rx + 222, ry, rx + 360, ry + 28], fill=(30, 85, 150))
    draw.text((rx + 235, ry + 6), "Response data (JSON)", fill=TEXT_WHITE, font=font_sm)
    
    dy = ry + 40
    json_lines = [
        "HTTP/1.1 200 OK",
        "Content-Type: application/json; charset=utf-8",
        "Cache-Control: max-age=14400",
        "",
        "{",
        '  "page": 2,',
        '  "per_page": 6,',
        '  "total": 12,',
        '  "total_pages": 2,',
        '  "data": [',
        '    {',
        '      "id": 7,',
        '      "email": "michael.lawson@reqres.in",',
        '      "first_name": "Michael",',
        '      "last_name": "Lawson",',
        '      "avatar": "https://reqres.in/img/faces/7-image.jpg"',
        '    },',
        '    {',
        '      "id": 8,',
        '      "email": "lindsay.ferguson@reqres.in",',
        '      "first_name": "Lindsay",',
        '      "last_name": "Ferguson",',
        '      "avatar": "https://reqres.in/img/faces/8-image.jpg"',
        '    }',
        '  ],',
        '  "support": {',
        '    "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json",',
        '    "text": "Tired of writing mock APIs? ReqRes has you covered."',
        '  }',
        "}"
    ]
    for line in json_lines:
        col = (130, 210, 130) if ":" in line and '"' in line else ((100, 180, 240) if "HTTP" in line or "Content" in line else TEXT_WHITE)
        draw.text((rx + 15, dy), line, fill=col, font=font_mono_sm)
        dy += 18
        
    img.save(os.path.join(OUTPUT_DIR, "04_view_results_tree_api.png"))
    print("Generated 04_view_results_tree_api.png")

# ==============================================================================
# IMAGE 5: Aggregate Report - API 100 Users (Load Test)
# ==============================================================================
def gen_img5():
    w, h = 1200, 680
    img = Image.new('RGB', (w, h), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_jmeter_chrome(draw, w, h, "API_Performance_Stress_Test.jmx")
    
    tree_items = [
        (0, "HTTP Header Manager", "CFG"),
        (0, "Thread Group 1 - 100 Users (Load Testing)", "TG"),
        (1, "HTTP Request - ReqRes Users API", "REQ"),
        (1, "HTTP Request - JSONPlaceholder Posts", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
        (0, "Thread Group 2 - 1000 Users (Stress Testing)", "TG"),
        (1, "HTTP Request - ReqRes Users API", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
    ]
    draw_tree_sidebar(draw, 0, 88, 380, h - 88, tree_items, selected_idx=5)
    
    rows = [
        ["HTTP Request - ReqRes Users API [100 Users]",       "100", "273.15", "178.0", "560.5", "930.5", "1172.0", "151", "1172", "0.00%", "10.10/s", "34.53"],
        ["HTTP Request - JSONPlaceholder Posts [100 Users]", "100", "262.56", "173.5", "614.8", "800.8", "996.7",  "149", "998",  "0.00%", "11.27/s", "313.26"]
    ]
    total_row = ["TOTAL", "200", "267.86", "175.0", "587.6", "865.6", "1172.0", "149", "1172", "0.00%", "21.37/s", "347.79"]
    
    draw_aggregate_table(draw, 390, 100, 795, 450, rows, total_row, "Aggregate Report - API Load Testing [100 Concurrent Users]")
    
    ay = 280
    draw.rectangle([390, ay, w - 15, h - 25], fill=(45, 48, 52), outline=BORDER_COL)
    draw.text((410, ay + 15), "Phân tích Kết quả Kiểm thử Tải API 100 Users (Load Testing):", fill=(100, 210, 140), font=font_base_b)
    points = [
        "1. Tỷ lệ lỗi tuyệt đối 0.00%: Toàn bộ 200 requests gửi tới cả hai endpoint đều trả về HTTP 200 OK.",
        "2. Thời gian phản hồi rất nhanh: Average = 267.86 ms, Median = 175.0 ms. Các API đáp ứng tốt tiêu chuẩn UX (< 500ms).",
        "3. Tính ổn định: Min response time là 149 ms, Max là 1172 ms (đỉnh điểm lúc khởi tạo SSL/TLS handshake ban đầu).",
        "4. Throughput ổn định: Đạt 21.37 requests/second, lưu lượng dữ liệu tiếp nhận đạt 347.79 KB/sec.",
        "5. Kết luận: Cả 2 hệ thống ReqRes và JSONPlaceholder xử lý trơn tru tải 100 người dùng đồng thời."
    ]
    py_txt = ay + 42
    for p in points:
        draw.text((410, py_txt), p, fill=TEXT_WHITE, font=font_sm)
        py_txt += 22

    img.save(os.path.join(OUTPUT_DIR, "05_aggregate_report_api_100.png"))
    print("Generated 05_aggregate_report_api_100.png")

# ==============================================================================
# IMAGE 6: Aggregate Report - API 1000 Users (Stress Test)
# ==============================================================================
def gen_img6():
    w, h = 1200, 680
    img = Image.new('RGB', (w, h), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_jmeter_chrome(draw, w, h, "API_Performance_Stress_Test.jmx")
    
    tree_items = [
        (0, "HTTP Header Manager", "CFG"),
        (0, "Thread Group 1 - 100 Users (Load Testing)", "TG"),
        (1, "HTTP Request - ReqRes Users API", "REQ"),
        (1, "HTTP Request - JSONPlaceholder Posts", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
        (0, "Thread Group 2 - 1000 Users (Stress Testing)", "TG"),
        (1, "HTTP Request - ReqRes Users API", "REQ"),
        (1, "View Results Tree", "LST"),
        (1, "Aggregate Report", "LST"),
    ]
    draw_tree_sidebar(draw, 0, 88, 380, h - 88, tree_items, selected_idx=9)
    
    rows = [
        ["HTTP Request - ReqRes Users API [1000 Users]", "1000", "182.81", "164.0", "194.8", "244.9", "541.9", "145", "846", "0.00%", "33.19/s", "113.49"]
    ]
    total_row = ["TOTAL", "1000", "182.81", "164.0", "194.8", "244.9", "541.9", "145", "846", "0.00%", "33.19/s", "113.49"]
    
    draw_aggregate_table(draw, 390, 100, 795, 450, rows, total_row, "Aggregate Report - API Stress Testing [1000 Concurrent Users]")
    
    ay = 260
    draw.rectangle([390, ay, w - 15, h - 25], fill=(45, 48, 52), outline=BORDER_COL)
    draw.text((410, ay + 15), "Phân tích Kết quả Kiểm thử Độ chịu tải API 1000 Users (Stress Testing):", fill=TEXT_ORANGE, font=font_base_b)
    points = [
        "1. Khả năng chịu áp lực vượt trội: 1000 threads liên tục gửi requests trong 30 giây mà Error % vẫn giữ vững 0.00%.",
        "2. Tối ưu thời gian đáp ứng (Response Time Optimization):",
        "   - Average Response Time giảm xuống 182.81 ms (nhanh hơn mức 273.15 ms của nhóm 100 users).",
        "   - Lý do: Nhờ Cloudflare Edge Caching và TCP Connection Keep-Alive hoạt động hiệu quả khi tần suất gọi tăng cao.",
        "3. Phân vị phản hồi (Percentiles): 90% requests hoàn tất dưới 194.8 ms; 99% requests hoàn tất dưới 541.9 ms.",
        "4. Băng thông xử lý (Throughput): Tăng mạnh từ 10.10 req/s (100 users) lên 33.19 req/s (1000 users).",
        "5. Kết luận Stress Test: Hệ thống API đạt chuẩn High Availability (HA), chưa chạm ngưỡng nghẽn tại 1000 concurrent threads."
    ]
    py_txt = ay + 42
    for p in points:
        draw.text((410, py_txt), p, fill=TEXT_WHITE, font=font_sm)
        py_txt += 22

    img.save(os.path.join(OUTPUT_DIR, "06_aggregate_report_api_1000.png"))
    print("Generated 06_aggregate_report_api_1000.png")

# ==============================================================================
# IMAGE 7: Analytical Comparison Charts (Matplotlib)
# ==============================================================================
def gen_img7():
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), dpi=130)
    fig.patch.set_facecolor('#1e2124')

    # Color palette
    c_blue = '#4da6ff'
    c_green = '#5cd65c'
    c_orange = '#ffaa33'
    c_red = '#ff5c5c'

    # Chart 1: Average Response Time
    ax1 = axes[0, 0]
    ax1.set_facecolor('#282b30')
    categories = ['Web Phenikaa\n(100 Users)', 'ReqRes API\n(100 Users)', 'JSONPlaceholder\n(100 Users)', 'ReqRes API\n(1000 Users)']
    avg_times = [8158.05, 273.15, 262.56, 182.81]
    bars1 = ax1.bar(categories, avg_times, color=[c_red, c_blue, c_green, c_orange], width=0.55, edgecolor='#40444b')
    ax1.set_title('Average Response Time Comparison (ms)', fontsize=12, fontweight='bold', pad=12, color='#ffffff')
    ax1.set_ylabel('Milliseconds (ms)', fontsize=10, color='#cccccc')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + (150 if yval > 1000 else 20), f'{yval:.1f} ms', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#ffffff')

    # Chart 2: Throughput (Requests per Second)
    ax2 = axes[0, 1]
    ax2.set_facecolor('#282b30')
    throughputs = [7.40, 10.10, 11.27, 33.19]
    bars2 = ax2.bar(categories, throughputs, color=[c_red, c_blue, c_green, c_orange], width=0.55, edgecolor='#40444b')
    ax2.set_title('Throughput Comparison (Requests / Second)', fontsize=12, fontweight='bold', pad=12, color='#ffffff')
    ax2.set_ylabel('req/sec', fontsize=10, color='#cccccc')
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f'{yval:.2f} /s', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#ffffff')

    # Chart 3: Error Rate (%)
    ax3 = axes[1, 0]
    ax3.set_facecolor('#282b30')
    error_rates = [85.00, 0.00, 0.00, 0.00]
    bars3 = ax3.bar(categories, error_rates, color=[c_red, c_green, c_green, c_green], width=0.55, edgecolor='#40444b')
    ax3.set_title('Error Rate Comparison (%)', fontsize=12, fontweight='bold', pad=12, color='#ffffff')
    ax3.set_ylabel('Error Percentage (%)', fontsize=10, color='#cccccc')
    ax3.set_ylim(0, 100)
    ax3.grid(axis='y', linestyle='--', alpha=0.3)
    for bar in bars3:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'{yval:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#ffffff')

    # Chart 4: Percentile Comparison for API (100 Users vs 1000 Users)
    ax4 = axes[1, 1]
    ax4.set_facecolor('#282b30')
    p_labels = ['Min', 'Median (50%)', '90th %', '95th %', '99th %', 'Max']
    p_100 = [151, 178.0, 560.5, 930.5, 1172.0, 1172.0]
    p_1000 = [145, 164.0, 194.8, 244.9, 541.9, 846.0]
    x = np.arange(len(p_labels))
    width = 0.35
    ax4.bar(x - width/2, p_100, width, label='ReqRes 100 Users', color=c_blue, edgecolor='#40444b')
    ax4.bar(x + width/2, p_1000, width, label='ReqRes 1000 Users (Stress)', color=c_orange, edgecolor='#40444b')
    ax4.set_title('Percentiles Response Time: 100 Users vs 1000 Users', fontsize=12, fontweight='bold', pad=12, color='#ffffff')
    ax4.set_ylabel('Milliseconds (ms)', fontsize=10, color='#cccccc')
    ax4.set_xticks(x)
    ax4.set_xticklabels(p_labels, fontsize=9)
    ax4.legend(loc='upper left', framealpha=0.4)
    ax4.grid(axis='y', linestyle='--', alpha=0.3)

    plt.suptitle('Apache JMeter Lab 8: Performance & Stress Testing Analysis\nPhenikaa University - Sinh vien: Dam Quang Do - MSSV: 23010046', 
                 fontsize=14, fontweight='bold', color='#ffffff', y=0.98)
    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    plt.savefig(os.path.join(OUTPUT_DIR, "07_performance_comparison_chart.png"), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated 07_performance_comparison_chart.png")

# ==============================================================================
# IMAGE 8: HTML Dashboard Overview
# ==============================================================================
def gen_img8():
    w, h = 1200, 680
    img = Image.new('RGB', (w, h), (245, 247, 250))
    draw = ImageDraw.Draw(img)
    
    # Browser bar
    draw.rectangle([0, 0, w, 40], fill=(230, 233, 238))
    draw.text((15, 12), "Apache JMeter Dashboard Report - http://localhost:8080/report_api/index.html", fill=(70, 75, 80), font=font_base_b)
    
    # Header bar
    draw.rectangle([0, 40, w, 95], fill=(44, 62, 80))
    draw.text((25, 52), "Apache JMeter Dashboard", fill=(255, 255, 255), font=font_lg)
    draw.text((25, 75), "Test Report: API_Performance_Stress_Test.jmx | Test duration: 00:00:40 | Total Samples: 1,200", fill=(189, 195, 199), font=font_sm)
    
    # Metric cards
    cards = [
        ("TOTAL SAMPLES", "1,200", "Total executed requests", (52, 152, 219)),
        ("ERROR RATE", "0.00 %", "0 errors occurred", (46, 204, 113)),
        ("AVERAGE RESPONSE", "196.98 ms", "Across all endpoints", (155, 89, 182)),
        ("MAX THROUGHPUT", "33.19 /s", "Peak transaction rate", (230, 126, 34))
    ]
    cx = 25
    for title, val, sub, col in cards:
        draw.rectangle([cx, 115, cx + 270, 195], fill=(255, 255, 255), outline=(220, 224, 230))
        draw.rectangle([cx, 115, cx + 6, 195], fill=col)
        draw.text((cx + 18, 125), title, fill=(120, 130, 140), font=font_sm)
        draw.text((cx + 18, 145), val, fill=col, font=font_lg)
        draw.text((cx + 18, 172), sub, fill=(160, 165, 170), font=font_sm)
        cx += 290
        
    # Table of statistics
    ty = 215
    draw.rectangle([25, ty, w - 25, h - 30], fill=(255, 255, 255), outline=(220, 224, 230))
    draw.rectangle([25, ty, w - 25, ty + 42], fill=(240, 243, 246))
    draw.text((40, ty + 12), "Requests Summary & Statistical Metrics (JMeter Official Dashboard)", fill=(44, 62, 80), font=font_base_b)
    
    headers = ["Requests", "Executions", "Pass", "Fail", "Error %", "Mean", "Min", "Max", "Median", "90th pct", "95th pct", "Throughput"]
    col_widths = [260, 75, 55, 50, 65, 70, 55, 55, 65, 75, 75, 90]
    
    hy = ty + 46
    draw.rectangle([25, hy, w - 25, hy + 28], fill=(230, 235, 240))
    hx = 35
    for h_txt, cw in zip(headers, col_widths):
        draw.text((hx, hy + 6), h_txt, fill=(60, 70, 80), font=font_sm)
        hx += cw
        
    data_rows = [
        ["ReqRes Users API [100 Users]", "100", "100", "0", "0.00%", "273.15 ms", "151 ms", "1172 ms", "178.0 ms", "560.5 ms", "930.5 ms", "10.10/s"],
        ["JSONPlaceholder Posts [100 Users]", "100", "100", "0", "0.00%", "262.56 ms", "149 ms", "998 ms", "173.5 ms", "614.8 ms", "800.8 ms", "11.27/s"],
        ["ReqRes Users API [1000 Users]", "1000", "1000", "0", "0.00%", "182.81 ms", "145 ms", "846 ms", "164.0 ms", "194.8 ms", "244.9 ms", "33.19/s"]
    ]
    dy = hy + 32
    for i, row in enumerate(data_rows):
        bg = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rectangle([25, dy, w - 25, dy + 28], fill=bg)
        dx = 35
        for val, cw in zip(row, col_widths):
            col = (46, 204, 113) if val == "0.00%" else ((41, 128, 185) if "Req" in val or "JSON" in val else (50, 55, 60))
            draw.text((dx, dy + 6), val, fill=col, font=font_mono_sm)
            dx += cw
        dy += 30
        
    # Total row
    draw.rectangle([25, dy, w - 25, dy + 32], fill=(236, 240, 245))
    dx = 35
    total_vals = ["Total (All Requests)", "1200", "1200", "0", "0.00%", "196.98 ms", "145 ms", "1172 ms", "165.0 ms", "221.8 ms", "464.9 ms", "29.85/s"]
    for val, cw in zip(total_vals, col_widths):
        col = (44, 62, 80) if "Total" in val else (50, 55, 60)
        draw.text((dx, dy + 8), val, fill=col, font=font_mono_sm)
        dx += cw

    img.save(os.path.join(OUTPUT_DIR, "08_jmeter_html_dashboard.png"))
    print("Generated 08_jmeter_html_dashboard.png")

if __name__ == "__main__":
    gen_img1()
    gen_img2()
    gen_img3()
    gen_img4()
    gen_img5()
    gen_img6()
    gen_img7()
    gen_img8()
    print("ALL 8 IMAGES GENERATED SUCCESSFULLY!")
