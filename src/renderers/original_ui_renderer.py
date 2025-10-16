import pygame
import pygame.gfxdraw
from typing import List, Tuple


class Button:
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int = 40,
        height: int = 20,
        color: Tuple[int, int, int] = (112, 64, 144),  # Purple color (0x704090)
        is_submit: bool = False,
    ):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.base_color = color
        self.current_color = color
        self.is_pressed = False
        self.is_active = False
        self.is_submit = is_submit

        # Different styling for submit button
        if is_submit:
            self.text_color = (208, 208, 208)  # Light gray
            self.base_color = (64, 128, 112)  # Greenish
            self.font = pygame.font.SysFont("times", 20)  # Slightly smaller
        else:
            self.text_color = (0, 0, 0)  # Black
            self.font = pygame.font.SysFont("times", 12)

        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen: pygame.Surface):
        # Button shadow effect
        shadow_offset = 4 if not self.is_pressed else 2
        shadow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surface,
            (32, 160, 48, 100),
            pygame.Rect(0, 0, self.width, self.height),
            border_radius=2,
        )
        screen.blit(shadow_surface, (self.x + shadow_offset, self.y + shadow_offset))

        # Main button
        button_color = self.current_color
        if self.is_pressed:
            button_color = tuple(max(0, c + 0x38) for c in self.base_color)
            button_pos = (self.x + 2, self.y + 2)
        elif self.is_active:
            button_color = tuple(max(0, c + 0x20) for c in self.base_color)
            button_pos = (self.x + 1, self.y + 1)
        else:
            button_pos = (self.x, self.y)

        pygame.draw.rect(
            screen, button_color, pygame.Rect(*button_pos, self.width, self.height), border_radius=2
        )
        pygame.draw.rect(
            screen,
            (192, 192, 192),
            pygame.Rect(*button_pos, self.width, self.height),
            1,
            border_radius=2,
        )

        # Text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(
            center=(button_pos[0] + self.width // 2, button_pos[1] + self.height // 2)
        )
        screen.blit(text_surface, text_rect)


class ScoreBoard:
    def __init__(self, x: int, y: int, width: int = 120, height: int = 160):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("times", 12)

        # Color schemes matching CircleRenderer
        self.COLORS = {
            "neutral": {
                "small": self._hex_to_rgb("0xe0e0e0"),
                "medium": self._hex_to_rgb("0xa0a0b0"),
                "large": self._hex_to_rgb("0x7070a0"),
            },
            "red": {
                "small": self._hex_to_rgb("0xe01010"),
                "medium": self._hex_to_rgb("0xc01010"),
                "large": self._hex_to_rgb("0xa01010"),
            },
            "blue": {
                "small": self._hex_to_rgb("0x1010e0"),
                "medium": self._hex_to_rgb("0x1010c0"),
                "large": self._hex_to_rgb("0x1010a0"),
            },
        }

    def _hex_to_rgb(self, hex_color):
        """Convert hex color string to RGB tuple"""
        hex_color = hex_color.replace("0x", "")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def calculate_stats(self, circle_manager):
        # Count small circles with correct color values
        small_red = sum(
            1
            for circle in circle_manager.small_circles
            if circle.color == self.COLORS["red"]["small"]
        )
        small_blue = sum(
            1
            for circle in circle_manager.small_circles
            if circle.color == self.COLORS["blue"]["small"]
        )

        # Count medium circles
        medium_red = sum(
            1
            for circle in circle_manager.medium_circles
            if circle.color == self.COLORS["red"]["medium"]
        )
        medium_blue = sum(
            1
            for circle in circle_manager.medium_circles
            if circle.color == self.COLORS["blue"]["medium"]
        )

        # Count large circles
        large_red = sum(
            1
            for circle in circle_manager.large_circles
            if circle.color == self.COLORS["red"]["large"]
        )
        large_blue = sum(
            1
            for circle in circle_manager.large_circles
            if circle.color == self.COLORS["blue"]["large"]
        )

        # Calculate totals
        total_red = small_red + medium_red + large_red
        total_blue = small_blue + medium_blue + large_blue

        # Calculate percentages (based on small circles as they represent board coverage)
        total_small_circles = len(circle_manager.small_circles)
        red_percentage = (small_red / total_small_circles * 100) if total_small_circles > 0 else 0
        blue_percentage = (small_blue / total_small_circles * 100) if total_small_circles > 0 else 0

        return {
            "small": (small_red, small_blue),
            "medium": (medium_red, medium_blue),
            "large": (large_red, large_blue),
            "total": (total_red, total_blue),
            "percentage": (red_percentage, blue_percentage),
        }


class ScoreBoard:
    def __init__(self, x: int, y: int, width: int = 120, height: int = 160):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("times", 12)

        # Corrected color values as lists
        self.COLORS = {
            "neutral": [128, 128, 128],  # Grey/White
            "red": [255, 0, 0],  # Pure Red
            "blue": [0, 0, 255],  # Pure Blue
        }

    def calculate_stats(self, circle_manager):
        if not circle_manager:
            print("Debug: circle_manager is None")
            return None

        # Count small circles
        small_red = sum(
            1 for circle in circle_manager.small_circles if circle.color == self.COLORS["red"]
        )
        small_blue = sum(
            1 for circle in circle_manager.small_circles if circle.color == self.COLORS["blue"]
        )

        # Count medium circles
        medium_red = sum(
            1 for circle in circle_manager.medium_circles if circle.color == self.COLORS["red"]
        )
        medium_blue = sum(
            1 for circle in circle_manager.medium_circles if circle.color == self.COLORS["blue"]
        )

        # Count large circles
        large_red = sum(
            1 for circle in circle_manager.large_circles if circle.color == self.COLORS["red"]
        )
        large_blue = sum(
            1 for circle in circle_manager.large_circles if circle.color == self.COLORS["blue"]
        )

        # Calculate totals
        total_red = small_red + medium_red + large_red
        total_blue = small_blue + medium_blue + large_blue

        # Calculate percentages
        total_small_circles = len(circle_manager.small_circles)
        red_percentage = (small_red / total_small_circles * 100) if total_small_circles > 0 else 0
        blue_percentage = (small_blue / total_small_circles * 100) if total_small_circles > 0 else 0

        return {
            "small": (small_red, small_blue),
            "medium": (medium_red, medium_blue),
            "large": (large_red, large_blue),
            "total": (total_red, total_blue),
            "percentage": (red_percentage, blue_percentage),
        }

    def draw(self, screen, circle_manager=None):
        cell_width = self.width // 4
        cell_height = 20

        # Draw header row with Red and Blue columns using correct colors
        headers = ["Red", "Blue"]
        header_colors = [self.COLORS["red"], self.COLORS["blue"]]

        for col, (header, color) in enumerate(zip(headers, header_colors)):
            x_pos = self.x + (col + 2) * cell_width  # Position in the last two columns
            pygame.draw.rect(screen, color, pygame.Rect(x_pos, self.y, cell_width, cell_height))
            text = self.font.render(header, True, (255, 255, 255))
            text_rect = text.get_rect(center=(x_pos + cell_width // 2, self.y + cell_height // 2))
            screen.blit(text, text_rect)

        # Calculate statistics if circle_manager is provided
        stats = self.calculate_stats(circle_manager) if circle_manager else None

        # Draw rows with labels and numbers
        rows = [
            ("L1", "272", stats["small"] if stats else (0, 0)),  # Small circles
            ("L2", "48", stats["medium"] if stats else (0, 0)),  # Medium circles
            ("L3", "8", stats["large"] if stats else (0, 0)),  # Large circles
            ("", "", stats["total"] if stats else (0, 0)),  # Totals
            ("", "", stats["percentage"] if stats else (0, 0)),  # Percentages
        ]

        for row, (label, number, counts) in enumerate(rows):
            y_pos = self.y + ((row + 1) * cell_height)

            # Draw row label if it exists
            if label:
                pygame.draw.rect(
                    screen, (64, 64, 64), pygame.Rect(self.x, y_pos, cell_width, cell_height)
                )
                text = self.font.render(label, True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(self.x + cell_width // 2, y_pos + cell_height // 2)
                )
                screen.blit(text, text_rect)

            # Draw number in second column if it exists
            if number:
                pygame.draw.rect(
                    screen,
                    (64, 64, 64),
                    pygame.Rect(self.x + cell_width, y_pos, cell_width, cell_height),
                )
                text = self.font.render(number, True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(self.x + cell_width * 1.5, y_pos + cell_height // 2)
                )
                screen.blit(text, text_rect)

            # Draw the counts/percentages in the last two columns
            for col, count in enumerate(counts):
                cell_color = (64, 64, 64) if row % 2 == 0 else (48, 48, 48)
                x_pos = self.x + (col + 2) * cell_width
                pygame.draw.rect(
                    screen,
                    cell_color,
                    pygame.Rect(x_pos, y_pos, cell_width, cell_height),
                )
                pygame.draw.rect(
                    screen,
                    (192, 192, 192),
                    pygame.Rect(x_pos, y_pos, cell_width, cell_height),
                    1,
                )

                # Format the number based on whether it's a percentage
                if row == 4:  # Last row (percentage row)
                    text = self.font.render(f"{int(count)}%", True, (255, 255, 255))
                else:
                    text = self.font.render(str(count), True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(x_pos + cell_width // 2, y_pos + cell_height // 2)
                )
                screen.blit(text, text_rect)


class MoveRegister:
    def __init__(self, x: int, y: int, width: int = 120, height: int = 200):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("times", 12)

    def draw(self, screen: pygame.Surface):
        headers = ["#", "L1", "L2", "L3"]
        cell_width = self.width // 4

        # Draw headers
        for col, header in enumerate(headers):
            pygame.draw.rect(
                screen, (80, 80, 80), pygame.Rect(self.x + col * cell_width, self.y, cell_width, 20)
            )
            text = self.font.render(header, True, (255, 255, 255))
            screen.blit(text, (self.x + col * cell_width + 5, self.y + 5))

        # Draw cells
        cell_height = 20
        for row in range(8):
            y_pos = self.y + (row + 1) * cell_height
            for col in range(4):
                cell_color = (64, 64, 64) if row % 2 == 0 else (48, 48, 48)
                pygame.draw.rect(
                    screen,
                    cell_color,
                    pygame.Rect(self.x + col * cell_width, y_pos, cell_width, cell_height),
                )
                pygame.draw.rect(
                    screen,
                    (192, 192, 192),
                    pygame.Rect(self.x + col * cell_width, y_pos, cell_width, cell_height),
                    1,
                )


class GameUI:
    def __init__(self, game_controller, width: int = 600, height: int = 600):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("The Ring World")
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.game_controller = game_controller

        # Load sound effects
        self.sounds = {
            "submit": pygame.mixer.Sound("assets/sounds/submit.mp3"),
            "cancel": pygame.mixer.Sound("assets/sounds/cancel.mp3"),
            "button": pygame.mixer.Sound("assets/sounds/button.mp3"),
        }

        # Create UI elements
        self.title_font = pygame.font.SysFont("times", 18)
        self.version_font = pygame.font.SysFont("times", 12)
        self.status_font = pygame.font.SysFont("times", 12)

        # Adjusted positions
        self.scoreboard = ScoreBoard(475, 10)  # Move to top
        self.move_register = MoveRegister(475, height - 185)  # Move to bottom

        # Create all buttons with adjusted positions
        self.buttons: List[Button] = [
            Button("Submit", 380, 10, 80, 30, is_submit=True),  # Align with scoreboard
            Button("Cancel", width - 50, 180, 40, 20),
            Button("Resign", width - 50, 210, 40, 20),
            Button("Quit", width - 50, 240, 40, 20),
            Button("Prev", width - 50, height - 270, 40, 20),  # Above move register
            Button("Next", width - 50, height - 240, 40, 20),  # Above move register
        ]

    def draw_status_boxes(self):
        # Top status box (smaller and narrower)
        pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(13, 600 - 103, 100, 25))
        pygame.draw.rect(self.screen, (192, 192, 192), pygame.Rect(13, 600 - 103, 100, 25), 1)
        if "circle" in self.game_controller.systems:
            phase = self.game_controller.systems["circle"].game_state.phase
            phase_text = f"Phase: {phase}"
        else:
            phase_text = "Phase: N/A"
        status_text = self.status_font.render(phase_text, True, (0, 0, 0))

        self.screen.blit(status_text, (16, 600 - 95))

        # Bottom status box (larger)
        pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(10, 600 - 75, 200, 70))
        pygame.draw.rect(self.screen, (192, 192, 192), pygame.Rect(10, 600 - 75, 200, 70), 1)

    def draw(self):
        # Fill background
        self.screen.fill((0, 0, 0))

        # Draw title
        title_surface = self.title_font.render("The Ring World", True, (0, 128, 255))
        self.screen.blit(title_surface, (20, 20))

        # Draw version more to the right
        version_surface = self.version_font.render("Version 1.37", True, (0, 128, 255))
        self.screen.blit(version_surface, (40, 45))  # Moved right

        # Draw status boxes
        self.draw_status_boxes()

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        # Draw scoreboard and move register
        self.scoreboard.draw(self.screen, self.game_controller.systems.get("circle").circle_manager)
        self.move_register.draw(self.screen)

    def play_button_sound(self, button_text: str):
        """Play the appropriate sound for the button press"""
        if button_text == "Submit":
            self.sounds["submit"].play()
        elif button_text == "Cancel":
            self.sounds["cancel"].play()
        else:
            self.sounds["button"].play()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.is_pressed = True
                    self.play_button_sound(button.text)
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                button.is_pressed = False
