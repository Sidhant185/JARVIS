# GUI.py
import os
import sys
import math
import random
from dotenv import dotenv_values
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect,
    QTextEdit, QLineEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize, QTimer, QEasingCurve, QPropertyAnimation, QPoint, QEvent, QRect, QDateTime, QRectF
from PyQt5.QtGui import (
    QMovie, QRegion, QColor, QPainter, QLinearGradient, QBrush, QPainterPath, QPen, QFont,
    QPixmap, QPainterPath
)
try:
    from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
    from PyQt5.QtCore import QUrl
    MULTIMEDIA_AVAILABLE = True
except Exception:
    MULTIMEDIA_AVAILABLE = False


# --- Environment Setup ---
def setup_environment():
    """Ensure directories, files, and Qt plugin paths are configured."""
    env_vars = dotenv_values(".env")
    assistant_name = env_vars.get("AssistantName", "Assistant")

    current_dir = os.getcwd()
    temp_dir = os.path.join(current_dir, "Frontend", "Files")
    graphics_dir = os.path.join(current_dir, "Frontend", "Graphics")

    # Ensure temp files exist
    os.makedirs(temp_dir, exist_ok=True)
    for fname, default in [("Mic.data", "False"), ("Status.data", ""), ("Responses.data", "")]:
        fpath = os.path.join(temp_dir, fname)
        if not os.path.exists(fpath):
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(default)

    # macOS fix: set cocoa plugin path if not already defined
    if sys.platform == "darwin" and "QT_QPA_PLATFORM_PLUGIN_PATH" not in os.environ:
        for py_ver in ("3.9", "3.10", "3.11"):
            candidate = os.path.join(
                os.path.dirname(sys.executable),
                f"../lib/python{py_ver}/site-packages/PyQt5/Qt5/plugins/platforms"
            )
            candidate = os.path.abspath(candidate)
            if os.path.exists(candidate):
                os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = candidate
                break

    return assistant_name, temp_dir, graphics_dir


# --- Animated Purple/Blue Wave Background with Particles & Parallax ---
class FuturisticBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._phase = 0.0
        self._speed = 0.02
        self._mouse_offset = QPoint(0, 0)
        self._last_interaction_ms = 0
        self._mode = "purple"  # or "blue"
        self._is_idle = False
        self._walk = 0.0  # horizontal wave walk

        # Mature HUD theme schemes
        self._schemes = {
            "purple": {
                "gradient": [
                    (0.0, QColor(0, 0, 0)),
                    (0.5, QColor(0, 0, 0)),
                    (1.0, QColor(0, 0, 0))
                ],
                "waves": [
                    QColor(187, 0, 255, 70),  # neon purple outer
                    QColor(142, 45, 226, 60),
                    QColor(255, 0, 221, 45)
                ],
                "particle": QColor(210, 160, 255)
            },
            "blue": {
                "gradient": [
                    (0.0, QColor(0, 0, 0)),
                    (0.5, QColor(0, 0, 0)),
                    (1.0, QColor(0, 0, 0))
                ],
                "waves": [
                    QColor(56, 189, 248, 70),
                    QColor(14, 165, 233, 60),
                    QColor(2, 132, 199, 45)
                ],
                "particle": QColor(160, 220, 255)
            }
        }

        # particles: x, y, size, dx, dy, alpha
        self._particles = []
        self._init_particles(70)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

    def set_mode(self, mode: str):
        self._mode = "blue" if mode == "blue" else "purple"
        self._speed = 0.026 if self._mode == "blue" else 0.018
        self.update()

    def get_speed(self) -> float:
        return self._speed

    def _init_particles(self, count):
        self._particles.clear()
        for _ in range(count):
            self._particles.append([
                random.uniform(0, 1),
                random.uniform(0, 1),
                random.uniform(0.8, 2.0),
                random.uniform(-0.12, 0.12),
                random.uniform(-0.06, 0.06),
                random.randint(60, 140)
            ])

    def _tick(self):
        self._phase += self._speed
        self._walk += 0.6  # smooth left->right drift
        if self._phase > 2 * math.pi:
            self._phase -= 2 * math.pi
        if self._last_interaction_ms:
            from time import time
            idle = (time() * 1000) - self._last_interaction_ms
            base = 0.026 if self._mode == "blue" else 0.018
            target_speed = base if idle < 20000 else base * 0.45
            self._speed += (target_speed - self._speed) * 0.02
            self._is_idle = idle >= 20000
        else:
            self._is_idle = False
        self.update()

    def mouseMoveEvent(self, event):
        self._mouse_offset = event.pos() - self.rect().center()
        from time import time
        self._last_interaction_ms = int(time() * 1000)
        super().mouseMoveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        w = self.width(); h = self.height()
        scheme = self._schemes[self._mode]
        grad = QLinearGradient(0, 0, w, h)
        for pos, col in scheme["gradient"]:
            grad.setColorAt(pos, col)
        painter.fillRect(self.rect(), QBrush(grad))

        # Hex-grid (subtle)
        self._draw_hex_grid(painter, cell=42, stroke=QColor(255,255,255,8))

        # Parallax waves
        parallax_x = self._mouse_offset.x() * 0.01
        parallax_y = self._mouse_offset.y() * 0.01
        colors = scheme["waves"]
        self._draw_wave(painter, 18, 280, 1.0, int(h * 0.35 + parallax_y), colors[0], parallax_x + self._walk)
        self._draw_wave(painter, 24, 380, 0.8, int(h * 0.55 + parallax_y * 0.6), colors[1], parallax_x * 0.6 + self._walk * 0.7)
        self._draw_wave(painter, 30, 520, 0.6, int(h * 0.75 + parallax_y * 0.3), colors[2], parallax_x * 0.3 + self._walk * 0.5)

        # Bokeh soft glows
        self._draw_bokeh(painter)

        # Particles
        base_particle = scheme["particle"]
        painter.setPen(Qt.NoPen)
        for x_norm, y_norm, size, dx, dy, alpha in self._particles:
            x = int(x_norm * w) + int(parallax_x * 8)
            y = int(y_norm * h) + int(parallax_y * 8)
            c = QColor(base_particle.red(), base_particle.green(), base_particle.blue(), alpha)
            painter.setBrush(QBrush(c))
            painter.drawEllipse(x, y, int(size), int(size))

    def _draw_wave(self, painter: QPainter, amplitude: int, wavelength: int, speed: float, y_offset: int, color: QColor, x_shift: float = 0.0):
        path = QPainterPath()
        w = self.width(); start_y = y_offset
        path.moveTo(0, start_y)
        for x in range(0, w + 2, 4):
            y = start_y + amplitude * math.sin(((x + x_shift) / wavelength * 2 * math.pi) + (self._phase * speed))
            path.lineTo(x, y)
        path.lineTo(w, self.height()); path.lineTo(0, self.height()); path.closeSubpath()
        painter.fillPath(path, QBrush(color))

    def _draw_hex_grid(self, painter: QPainter, cell=36, stroke=QColor(255,255,255,12)):
        w = self.width(); h = self.height()
        if w <= 0 or h <= 0:
            return
        painter.save()
        pen = QPen(stroke); pen.setWidth(1)
        painter.setPen(pen); painter.setBrush(Qt.NoBrush)
        # Hex metrics
        a = cell / 2.0
        r = cell * math.sqrt(3) / 2.0
        for row in range(0, int(h / (r)) + 2):
            y = row * r
            x_offset = a if row % 2 else 0
            for col in range(0, int(w / cell) + 2):
                cx = col * cell + x_offset
                path = QPainterPath()
                for i in range(6):
                    angle = math.radians(60 * i + 30)
                    px = cx + a * math.cos(angle)
                    py = y + a * math.sin(angle)
                    if i == 0:
                        path.moveTo(px, py)
                    else:
                        path.lineTo(px, py)
                path.closeSubpath()
                painter.drawPath(path)
        painter.restore()

    def _draw_bokeh(self, painter: QPainter):
        painter.save()
        painter.setPen(Qt.NoPen)
        glows = [
            (QColor(109, 40, 217, 40), 180, 140),
            (QColor(124, 58, 237, 30), 420, 260),
            (QColor(14, 165, 233, 25), 900, 180),
        ]
        for color, gx, gy in glows:
            painter.setBrush(color)
            painter.drawEllipse(gx, gy, 220, 220)
        painter.restore()


# Glowing cursor follower with trail
class GlowCursorOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self._trail = []  # list of (x, y, alpha)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._decay)
        self._timer.start(16)

    def sizeHint(self):
        if self.parent() is not None:
            return self.parent().size()
        return super().sizeHint()

    def update_position(self, pos: QPoint):
        # Map global to local
        local = self.mapFromGlobal(pos)
        self._trail.append([local.x(), local.y(), 255])
        if len(self._trail) > 25:
            self._trail.pop(0)
        self.update()

    def _decay(self):
        changed = False
        for t in self._trail:
            t[2] = max(0, t[2] - 12)
            changed = True
        if changed:
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for x, y, a in self._trail:
            if a <= 0:
                continue
            color = QColor(192, 132, 252, a)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QPoint(x, y), 6, 6)


# Rotating neon ring widget
class RotatingRing(QWidget):
    def __init__(self, color=QColor(150, 120, 210), thickness=2, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._color = color
        self._thickness = thickness
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def _tick(self):
        self._angle = (self._angle + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(6, 6, -6, -6)
        rectf = QRectF(rect)
        pen = QPen(self._color)
        pen.setWidth(self._thickness)
        pen.setCapStyle(Qt.RoundCap)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._angle)
        painter.translate(-self.width() / 2, -self.height() / 2)
        path = QPainterPath()
        path.arcMoveTo(rectf, 0)
        path.arcTo(rectf, 0, 220)
        painter.drawPath(path)


class HUDCore(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def _tick(self):
        self._angle = (self._angle + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = self.rect().center()
        max_r = min(self.width(), self.height()) // 2 - 8
        # Concentric rings
        for i, radius in enumerate([max_r, int(max_r*0.78), int(max_r*0.58)]):
            pen = QPen(QColor(170, 170, 220, 80 - i*10)); pen.setWidth(1)
            painter.setPen(pen); painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(center, radius, radius)
        # Radial ticks
        painter.save(); painter.translate(center)
        tick_pen = QPen(QColor(140, 200, 240, 140)); tick_pen.setWidth(1)
        painter.setPen(tick_pen)
        for i in range(36):
            angle = i * 10
            painter.save(); painter.rotate(angle + self._angle * 0.5)
            painter.drawLine(0, -max_r, 0, -max_r + 8)
            painter.restore()
        painter.restore()
        # Dashed rotating scanner arc
        scanner_r = int(max_r*0.88)
        pen = QPen(QColor(120, 220, 255, 160)); pen.setWidth(2); pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.translate(center); painter.rotate(self._angle * 1.2); painter.translate(-center)
        rect = QRectF(center.x()-scanner_r, center.y()-scanner_r, scanner_r*2, scanner_r*2)
        path = QPainterPath(); path.arcMoveTo(rect, 0); path.arcTo(rect, 0, 40)
        painter.drawPath(path)
        # Data blips
        painter.resetTransform()
        painter.translate(center)
        blip_pen = QPen(QColor(120, 220, 255, 180)); blip_pen.setWidth(2)
        painter.setPen(blip_pen)
        for i in range(6):
            a = (self._angle * 3 + i * 60) % 360
            rad = math.radians(a)
            r = max_r * (0.4 + 0.55 * ((i % 3) / 2))
            x = math.cos(rad) * r; y = math.sin(rad) * r
            painter.drawPoint(int(x), int(y))


# Top neon flicker title
class FlickerTitle(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._t = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(50)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setStyleSheet("font-size: 22px; font-weight: 800; letter-spacing: 1.6px;")

    def _tick(self):
        self._t = (self._t + 1) % 200
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        base = QColor(187, 0, 255)
        white = QColor(255, 255, 255)
        for r, a in ((3, 50), (2, 90), (1, 140)):
            pen = QPen(QColor(base.red(), base.green(), base.blue(), a))
            pen.setWidth(r)
            painter.setPen(pen)
            painter.drawText(rect, int(Qt.AlignHCenter | Qt.AlignVCenter), self.text())
        flicker = 255 if self._t % 33 not in (0, 1) else 120
        painter.setPen(QPen(QColor(white.red(), white.green(), white.blue(), flicker), 1))
        painter.drawText(rect, int(Qt.AlignHCenter | Qt.AlignVCenter), self.text())


# Cyberpunk neon button
class NeonButton(QPushButton):
    def __init__(self, label: str, color: QColor, parent=None):
        super().__init__(label, parent)
        self._base_color = color
        self._hover = False
        self.setCursor(Qt.PointingHandCursor)
        self._update_style()

    def enterEvent(self, event):
        self._hover = True
        self._update_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self._update_style()
        super().leaveEvent(event)

    def _update_style(self):
        c = self._base_color
        glow = 0.75 if self._hover else 0.35
        self.setStyleSheet(
            f"""
            QPushButton {{
                background: rgba({c.red()},{c.green()},{c.blue()},{int(255*0.10)});
                color: #e9defc;
                border: 1px solid rgba({c.red()},{c.green()},{c.blue()},180);
                border-radius: 10px;
                padding: 8px 14px;
            }}
            QPushButton:hover {{
                box-shadow: 0 0 18px rgba({c.red()},{c.green()},{c.blue()},{int(255*glow)});
            }}
            """
        )


# Right-side glassmorphic panel
class GlassPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("glassPanel")
        self.setStyleSheet(
            "#glassPanel { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.14); border-radius: 14px; }"
            "QLabel { color: #e2e6f3; } QTextEdit { background: rgba(0,0,0,0.25); color: #cde3ff; border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; }"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        header = QHBoxLayout(); header.setSpacing(8)
        self.status_dot = QLabel("  ")
        self.status_dot.setFixedSize(12, 12)
        self.status_dot.setStyleSheet("background: #22c55e; border-radius: 6px;")
        self.status_text = QLabel("Status: Ready")
        header.addWidget(self.status_dot, 0)
        header.addWidget(self.status_text, 1)
        layout.addLayout(header)

        self.logs = QTextEdit(); self.logs.setReadOnly(True); self.logs.setPlaceholderText("Session log...")
        layout.addWidget(self.logs, 1)

    def set_status(self, status: str):
        txt = status.strip() or "ready"
        busy = any(k in txt for k in ["thinking", "processing", "working", "busy"]) and not any(k in txt for k in ["idle", "done", "ready"])
        self.status_text.setText(f"Status: {status if status else 'Ready'}")
        self.status_dot.setStyleSheet(f"background: {'#f59e0b' if busy else '#22c55e'}; border-radius: 6px;")

    def append_log(self, line: str):
        self.logs.append(line)
        self.logs.moveCursor(self.logs.textCursor().End)

    # No AI responses panel; only session logs are kept in-memory

# --- Main Window ---
class MainWindow(QMainWindow):
    def __init__(self, assistant_name, graphics_dir, temp_dir):
        super().__init__()
        self.setWindowTitle(f"{assistant_name} - Smart Assistant")
        self.setMinimumSize(1200, 780)
        self.graphics_dir = graphics_dir
        self.temp_dir = temp_dir

        font = QFont("Montserrat"); font.setPointSize(11); self.setFont(font)
        self.setStyleSheet("QLabel { color: #e2e6f3; }")

        self.background = FuturisticBackground()
        bg_layout = QVBoxLayout(self.background); bg_layout.setContentsMargins(40, 28, 40, 40); bg_layout.setSpacing(10); bg_layout.setAlignment(Qt.AlignTop)

        # Top neon title
        self.title = FlickerTitle(f"{assistant_name} · Neural Interface")
        bg_layout.addWidget(self.title)

        # Cyberpunk controls row
        controls_row = QHBoxLayout(); controls_row.setContentsMargins(0, 0, 0, 0); controls_row.setSpacing(10)
        self.run_btn = NeonButton("Run", QColor(0, 255, 183)); self.stop_btn = NeonButton("Stop", QColor(255, 71, 87)); self.settings_btn = NeonButton("Settings", QColor(187, 0, 255))
        self.run_btn.clicked.connect(lambda: self._on_command_clicked("run"))
        self.stop_btn.clicked.connect(lambda: self._on_command_clicked("stop"))
        self.settings_btn.clicked.connect(lambda: self._on_command_clicked("settings"))
        controls_row.addWidget(self.run_btn)
        controls_row.addWidget(self.stop_btn)
        controls_row.addWidget(self.settings_btn)
        controls_row.addStretch(1)

        # Legacy mini toggles preserved
        self.tagline = ShimmerLabel("Beyond Limits · Instant Intelligence"); self.tagline.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tagline.setStyleSheet("font-size: 12px; font-weight: 600; letter-spacing: 1.1px;")
        self._tagline_shadow = QGraphicsDropShadowEffect(self); self._tagline_shadow.setBlurRadius(18); self._tagline_shadow.setXOffset(0); self._tagline_shadow.setYOffset(0); self._tagline_shadow.setColor(QColor(125, 249, 255, 120)); self.tagline.setGraphicsEffect(self._tagline_shadow)
        self.theme_btn = QPushButton("Thinking: Off"); self.theme_btn.setStyleSheet("background: rgba(125,249,255,0.12); color: #d8eef3; border: 1px solid rgba(125,249,255,0.35); border-radius: 8px; padding: 6px 10px;"); self.theme_btn.clicked.connect(self._toggle_theme)
        self.ambient_btn = QPushButton("Ambient: Off"); self.ambient_btn.setStyleSheet("background: rgba(109,40,217,0.12); color: #e9defc; border: 1px solid rgba(109,40,217,0.35); border-radius: 8px; padding: 6px 10px;"); self.ambient_btn.clicked.connect(self._toggle_ambient)
        self.click_btn = QPushButton("Click: Off"); self.click_btn.setStyleSheet("background: rgba(168,85,247,0.12); color: #f0e9ff; border: 1px solid rgba(168,85,247,0.35); border-radius: 8px; padding: 6px 10px;"); self.click_btn.clicked.connect(self._toggle_click)
        controls_row.addWidget(self.tagline)
        controls_row.addWidget(self.theme_btn)
        controls_row.addWidget(self.ambient_btn)
        controls_row.addWidget(self.click_btn)
        bg_layout.addLayout(controls_row)

        status_row = QHBoxLayout(); status_row.setContentsMargins(0, 0, 0, 0); status_row.setSpacing(12)
        self.metric_latency = QLabel("latency 24ms"); self.metric_latency.setStyleSheet("color:#9fb3cc; font-size:11px;"); self.metric_cpu = QLabel("cpu 12%"); self.metric_cpu.setStyleSheet("color:#9fb3cc; font-size:11px;"); self.metric_temp = QLabel("temp 41°C"); self.metric_temp.setStyleSheet("color:#9fb3cc; font-size:11px;")
        status_row.addWidget(QWidget(), 1); status_row.addWidget(self.metric_latency); status_row.addWidget(self.metric_cpu); status_row.addWidget(self.metric_temp)
        bg_layout.addLayout(status_row)

        center = QWidget(); center_layout = QVBoxLayout(center); center_layout.setContentsMargins(0, 0, 0, 0); center_layout.setSpacing(16); center_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        card = QWidget(); card.setObjectName("glassCard"); card.setMaximumWidth(980)
        card_layout = QVBoxLayout(card); card_layout.setContentsMargins(28, 22, 28, 20); card_layout.setSpacing(12); card_layout.setAlignment(Qt.AlignCenter)
        card.setStyleSheet("#glassCard { background: transparent; border: none; border-radius: 0px; }")
        # Remove shadow so no rectangle is perceptible
        # (do not apply drop shadow effect to the transparent container)

        self.subtitle = QLabel("Listening · Thinking · Acting"); self.subtitle.setAlignment(Qt.AlignCenter); self.subtitle.setStyleSheet("font-size: 13px; color: #cfd6ea; margin-bottom: 6px;"); card_layout.addWidget(self.subtitle)
        self._subtitle_timer = QTimer(self); self._subtitle_timer.timeout.connect(self._tick_subtitle); self._subtitle_timer.start(800); self._subtitle_state = 0
        card_layout.addStretch(1)

        core_container = QWidget(); core_layout = QVBoxLayout(core_container); core_layout.setContentsMargins(0, 0, 0, 0); core_layout.setSpacing(0); core_layout.setAlignment(Qt.AlignCenter)
        self.gif_label = QLabel(); self.gif_label.setAlignment(Qt.AlignCenter); self.gif_label.setMinimumSize(360, 360); self.gif_label.setStyleSheet("background: transparent;")
        jarvis_gif_path = os.path.join(self.graphics_dir, "Jarvis.gif")
        if os.path.exists(jarvis_gif_path):
            self.movie = QMovie(jarvis_gif_path); screen = self.screen()
            if screen is not None:
                screen_rect = screen.availableGeometry(); max_width = int(screen_rect.width() * 0.62); max_height = int(screen_rect.height() * 0.62)
                self.movie.setScaledSize(QSize(max_width, max_height))
            self.gif_label.setMovie(self.movie); self.movie.frameChanged.connect(self._apply_circular_mask); self.movie.start()
        core_layout.addWidget(self.gif_label)
        # Pulsing aura rings around GIF
        self.ring_outer = RotatingRing(QColor(160, 140, 220, 200), 2, core_container)
        self.ring_inner = RotatingRing(QColor(120, 220, 255, 200), 2, core_container)
        self.hud_overlay = HUDCore(core_container); self.hud_overlay.raise_()
        card_layout.addWidget(core_container, 0, Qt.AlignHCenter)
        card_layout.addStretch(1)

        center_layout.addWidget(card)

        # Right glassmorphic panel
        self.right_panel = GlassPanel()
        self.right_panel.setMinimumWidth(360); self.right_panel.setMaximumWidth(420)

        # Arrange center + right side by HBox
        content_row = QHBoxLayout(); content_row.setContentsMargins(0, 0, 0, 0); content_row.setSpacing(16)
        content_row.addWidget(center, 3)
        content_row.addWidget(self.right_panel, 2)
        bg_layout.addLayout(content_row, 1)

        # Bottom input row
        bottom_row = QHBoxLayout(); bottom_row.setContentsMargins(0, 10, 0, 0); bottom_row.setSpacing(10)
        self.input_line = QLineEdit(); self.input_line.setPlaceholderText("Type a command or question...")
        self.input_line.setStyleSheet("background: rgba(255,255,255,0.06); color:#e2e6f3; border: 1px solid rgba(255,255,255,0.14); border-radius: 10px; padding: 10px;")
        self.send_btn = NeonButton("Send", QColor(0, 221, 255))
        self.input_line.returnPressed.connect(self._on_send)
        self.send_btn.clicked.connect(self._on_send)
        bottom_row.addWidget(self.input_line, 1)
        bottom_row.addWidget(self.send_btn, 0)
        bg_layout.addLayout(bottom_row)
        self.setCentralWidget(self.background)

        # Remove chat/console: do not create chat_panel, history, input, spinner, or related animations
        # Remove chat animations
        
        # Keep ambient/click/theme and metrics
        self._setup_startup_animation()
        self._glow_sync_timer = QTimer(self); self._glow_sync_timer.timeout.connect(self._sync_glow_to_speed); self._glow_sync_timer.start(30)

        # Ambient and click players as before
        self._ambient_on = False
        if MULTIMEDIA_AVAILABLE:
            self._player = QMediaPlayer(self); ambient_path = os.path.join(self.graphics_dir, "ambient.mp3")
            if os.path.exists(ambient_path):
                self._ambient_url = QUrl.fromLocalFile(ambient_path); self._player.setMedia(QMediaContent(self._ambient_url)); self._player.setVolume(12); self._player.stateChanged.connect(self._loop_ambient)
            else:
                self._player = None
        else:
            self._player = None
        self._ambient_dim_timer = QTimer(self); self._ambient_dim_timer.timeout.connect(self._dim_ambient); self._ambient_dim_timer.start(500)

        self._click_on = False
        if MULTIMEDIA_AVAILABLE:
            self._click_player = QMediaPlayer(self); click_path = os.path.join(self.graphics_dir, "click.mp3")
            self._click_url = QUrl.fromLocalFile(click_path) if os.path.exists(click_path) else None
        else:
            self._click_player = None; self._click_url = None
        self._metrics_timer = QTimer(self); self._metrics_timer.timeout.connect(self._update_metrics); self._metrics_timer.start(1500)

        # Backend-driven thinking
        self._last_status = ""; self._last_response_text = ""; self._backend_timer = QTimer(self); self._backend_timer.timeout.connect(self._update_backend_state); self._backend_timer.start(200)
        self._thinking_timeout_timer = QTimer(self); self._thinking_timeout_timer.setSingleShot(True); self._thinking_timeout_timer.timeout.connect(lambda: self._set_thinking(False))

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseMove and hasattr(self, 'cursor_overlay'):
            self.cursor_overlay.update_position(event.globalPos())
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.gif_label and self.hud_overlay:
            g = self.gif_label.geometry()
            self.hud_overlay.setGeometry(g)
            # Position aura rings to track the GIF bounds
            self.ring_outer.setGeometry(g.adjusted(-20, -20, 20, 20))
            self.ring_inner.setGeometry(g.adjusted(10, 10, -10, -10))
        if hasattr(self, 'cursor_overlay'):
            self.cursor_overlay.setGeometry(self.rect())
        self._apply_circular_mask()

    def _toggle_theme(self):
        new_mode = "blue" if self.background._mode == "purple" else "purple"
        self.background.set_mode(new_mode)
        self.theme_btn.setText("Thinking: On" if new_mode == "blue" else "Thinking: Off")
        if new_mode == "blue":
            self.ring_outer._color = QColor(120, 180, 235, 200)
            self.ring_inner._color = QColor(90, 210, 240, 200)
            self._tagline_shadow.setColor(QColor(125, 249, 255, 150))
        else:
            self.ring_outer._color = QColor(160, 140, 220, 200)
            self.ring_inner._color = QColor(120, 220, 255, 200)
            self._tagline_shadow.setColor(QColor(125, 249, 255, 120))
        self.ring_outer.update(); self.ring_inner.update()

    def _toggle_ambient(self):
        if self._player is None:
            self.ambient_btn.setText("Ambient: N/A")
            return
        self._ambient_on = not self._ambient_on
        if self._ambient_on:
            self._player.setMedia(QMediaContent(self._ambient_url))
            self._player.play()
            self.ambient_btn.setText("Ambient: On")
        else:
            self._player.pause()
            self.ambient_btn.setText("Ambient: Off")

    def _loop_ambient(self, state):
        if not self._ambient_on or self._player is None:
            return
        if state == QMediaPlayer.StoppedState:
            self._player.setMedia(QMediaContent(self._ambient_url))
            self._player.play()

    def _dim_ambient(self):
        if not self._ambient_on or self._player is None:
            return
        is_idle = getattr(self.background, "_is_idle", False)
        target = 8 if is_idle else 15
        cur = self._player.volume()
        if cur != target:
            step = 1 if cur < target else -1
            self._player.setVolume(cur + step)

    def _setup_startup_animation(self):
        start_rect = self.gif_label.geometry()
        end_rect = start_rect.adjusted(-30, -30, 30, 30)
        self._scale_anim = QPropertyAnimation(self.gif_label, b"geometry", self)
        self._scale_anim.setDuration(900)
        self._scale_anim.setStartValue(start_rect)
        self._scale_anim.setEndValue(end_rect)
        self._scale_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._scale_anim.start()

    def _animate_chatbox_entry(self):
        end_rect = self.chat_panel.geometry()
        if end_rect.isNull():
            self.chat_panel.show()
            self.chat_panel.repaint()
            end_rect = self.chat_panel.geometry()
        start_rect = QRect(end_rect.x(), end_rect.y() + 80, end_rect.width(), end_rect.height())
        self.chat_panel.setGeometry(start_rect)
        self._chat_anim = QPropertyAnimation(self.chat_panel, b"geometry", self)
        self._chat_anim.setDuration(600)
        self._chat_anim.setStartValue(start_rect)
        self._chat_anim.setEndValue(end_rect)
        self._chat_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._chat_anim.start()

    def _tick_subtitle(self):
        base = "Listening · Thinking · Acting"
        dots = ["", ".", "..", "..."]
        self._subtitle_state = (self._subtitle_state + 1) % len(dots)
        self.subtitle.setText(f"{base}{dots[self._subtitle_state]}")

    # Remove chat send handler and spinner functions
    def _send_message(self):
        pass
    def _show_spinner(self, show: bool):
        pass
    def _spin_tick(self):
        pass

    # New input send handler
    def _on_send(self):
        text = self.input_line.text().strip()
        if not text:
            return
        # Append to logs and clear input
        if hasattr(self, 'right_panel'):
            timestamp = QDateTime.currentDateTime().toString('hh:mm:ss')
            self.right_panel.append_log(f"[{timestamp}] User: {text}")
        self.input_line.clear()
        # Optional click
        if getattr(self, '_click_on', False) and self._click_player is not None and self._click_url is not None:
            self._click_player.setMedia(QMediaContent(self._click_url))
            self._click_player.play()
        # Signal processing state
        self._set_thinking(True)

    def _on_command_clicked(self, cmd: str):
        if hasattr(self, 'right_panel'):
            timestamp = QDateTime.currentDateTime().toString('hh:mm:ss')
            self.right_panel.append_log(f"[{timestamp}] Command: {cmd}")
        if cmd in ("run", "stop"):
            self._set_thinking(cmd == "run")

    def _apply_circular_mask(self, *_):
        rect = self.gif_label.rect()
        if rect.width() > 0 and rect.height() > 0:
            diameter = min(rect.width(), rect.height())
            x = (rect.width() - diameter) // 2
            y = (rect.height() - diameter) // 2
            mask_region = QRegion(x, y, diameter, diameter, QRegion.Ellipse)
            self.gif_label.setMask(mask_region)

    def _sync_glow_to_speed(self):
        # If no card shadow (transparent layout), skip glow sync safely
        if not hasattr(self, "_card_shadow") or self._card_shadow is None:
            return
        speed = self.background.get_speed()  # ~0.008 - 0.028
        t = (speed - 0.008) / (0.028 - 0.008)
        t = max(0.0, min(1.0, t))
        min_blur, max_blur = 24, 48
        blur = int(min_blur + (max_blur - min_blur) * t)
        self._card_shadow.setBlurRadius(blur)

    def _toggle_click(self):
        self._click_on = not getattr(self, "_click_on", False)
        if hasattr(self, "click_btn"):
            self.click_btn.setText("Click: On" if self._click_on else "Click: Off")

    def _update_metrics(self):
        import random
        lat = 18 + random.randint(0, 12)
        cpu = 8 + random.randint(0, 20)
        temp = 38 + random.randint(0, 7)
        if hasattr(self, "metric_latency"):
            self.metric_latency.setText(f"latency {lat}ms")
        if hasattr(self, "metric_cpu"):
            self.metric_cpu.setText(f"cpu {cpu}%")
        if hasattr(self, "metric_temp"):
            self.metric_temp.setText(f"temp {temp}°C")

    def _update_backend_state(self):
        try:
            status_path = os.path.join(self.temp_dir, "Status.data")
            with open(status_path, "r", encoding="utf-8") as f:
                status = f.read().strip().lower()
        except Exception:
            status = ""
        thinking_on = any(k in status for k in ["thinking", "processing", "working", "busy"]) and not any(k in status for k in ["idle", "done", "ready"]) 
        self._set_thinking(thinking_on)
        # Update right panel status text
        if hasattr(self, 'right_panel'):
            try:
                with open(status_path, "r", encoding="utf-8") as f:
                    raw_status = f.read().strip()
            except Exception:
                raw_status = ""
            self.right_panel.set_status(raw_status)
        # No longer reading Responses.data; keep only in-session logs

    def _set_thinking(self, on: bool):
        target_mode = "blue" if on else "purple"
        if getattr(self.background, "_mode", None) != target_mode:
            self._toggle_theme()


class ShimmerLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._t = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def _tick(self):
        self._t += 0.02
        if self._t > 1.0:
            self._t = 0.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        base = QColor(125, 249, 255)
        painter.setPen(base)
        grad = QLinearGradient(0, 0, rect.width(), 0)
        grad.setColorAt(max(0.0, self._t - 0.2), QColor(125, 249, 255, 80))
        grad.setColorAt(self._t, QColor(255, 255, 255))
        grad.setColorAt(min(1.0, self._t + 0.2), QColor(125, 249, 255, 80))
        painter.setBrush(Qt.NoBrush)
        painter.drawText(rect, int(Qt.AlignRight | Qt.AlignVCenter), self.text())
        painter.setPen(QPen(QBrush(grad), 1))
        painter.drawText(rect, int(Qt.AlignRight | Qt.AlignVCenter), self.text())


# --- GUI Runner ---
def run_gui():
    assistant_name, temp_dir, graphics_dir = setup_environment()

    app = QApplication(sys.argv)
    app.setApplicationName(f"{assistant_name} Is here!!")
    app.setApplicationDisplayName(f"{assistant_name} - Smart Assistant")

    window = MainWindow(assistant_name, graphics_dir, temp_dir)
    window.show()

    banner = f"""
    ┌──────────────────────────────────────────┐
    │   {assistant_name.upper()} IS NOW RUNNING! 🚀            │
    │   Close the window to exit gracefully.   │
    └──────────────────────────────────────────┘
    """
    print(banner)

    sys.exit(app.exec_())


# --- Entry Point ---
if __name__ == "__main__":
    try:
        run_gui()
    except Exception as e:
        print("\n❌ Failed to start GUI:", e)
        sys.exit(1)
