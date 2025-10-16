import pygame
from ..utils.settings import GameMode
from ..managers.network.network_manager import GameNetworkManager
from ..utils.settings import RED


class MenuSystem:
    def __init__(self):
        self.title_font = pygame.font.SysFont("times", 48)
        self.version_font = pygame.font.SysFont("times", 32)
        self.button_font = pygame.font.SysFont("times", 36)
        self.small_font = pygame.font.SysFont("times", 24)
        self.mode = GameMode.MENU
        self.room_code = ""
        self.input_active = False
        self.network_manager = GameNetworkManager()
        self.player_color = None
        self.show_size_selection = False
        self.selected_game_mode = None

        # Load button sound
        self.button_sound = pygame.mixer.Sound("assets/sounds/button.mp3")

        # Button colors
        self.button_color = (112, 64, 144)  # Purple color (0x704090)
        self.button_active_color = tuple(max(0, c + 0x20) for c in self.button_color)
        self.button_pressed_color = tuple(max(0, c + 0x38) for c in self.button_color)

        # Track which button is being pressed
        self.pressed_button = None
        self.pressed_size_button = None

    def draw(self, surface):
        surface.fill((0, 0, 0))  # Black background

        if self.show_size_selection:
            self._draw_size_selection(surface)
        elif self.mode == GameMode.MENU:
            self._draw_main_menu(surface)
        elif self.mode == GameMode.WAITING:
            self._draw_waiting_screen(surface)

    def _draw_size_selection(self, surface):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.fill((32, 32, 32))
        overlay.set_alpha(200)
        surface.blit(overlay, (0, 0))

        # Draw prompt
        prompt = self.title_font.render("Select Game Size:", True, (208, 208, 208))
        prompt_rect = prompt.get_rect(center=(surface.get_width() // 2, 200))
        surface.blit(prompt, prompt_rect)

        # Button dimensions
        button_width = 200
        button_height = 60
        button_spacing = 80
        start_y = 300

        # Draw size selection buttons
        buttons = ["LARGE", "SMALL"]
        for i, text in enumerate(buttons):
            button_rect = pygame.Rect(
                (surface.get_width() - button_width) // 2,
                start_y + i * button_spacing,
                button_width,
                button_height,
            )
            is_pressed = self.pressed_size_button == i
            self._draw_button(surface, text, button_rect, is_pressed)

    def _draw_button(self, surface, text, rect, is_pressed=False):
        # Button shadow effect (only vertical offset)
        shadow_offset = 4 if not is_pressed else 2
        shadow_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surface,
            (32, 160, 48, 100),
            pygame.Rect(0, 0, rect.width, rect.height),
            border_radius=2,
        )
        surface.blit(shadow_surface, (rect.x, rect.y + shadow_offset))

        # Main button
        button_color = self.button_pressed_color if is_pressed else self.button_color
        button_pos = (rect.x, rect.y + (2 if is_pressed else 0))

        pygame.draw.rect(
            surface,
            button_color,
            pygame.Rect(button_pos[0], button_pos[1], rect.width, rect.height),
            border_radius=2,
        )
        pygame.draw.rect(
            surface,
            (192, 192, 192),
            pygame.Rect(button_pos[0], button_pos[1], rect.width, rect.height),
            1,
            border_radius=2,
        )

        # Text
        text_surface = self.button_font.render(text, True, (208, 208, 208))
        text_rect = text_surface.get_rect(
            center=(button_pos[0] + rect.width // 2, button_pos[1] + rect.height // 2)
        )
        surface.blit(text_surface, text_rect)

    def _draw_main_menu(self, surface):
        # Draw title
        title = self.title_font.render("The Ring World", True, (0, 128, 255))
        title_rect = title.get_rect(center=(surface.get_width() // 2, 100))
        surface.blit(title, title_rect)

        # Draw version
        version = self.version_font.render("Version 1.37", True, (0, 128, 255))
        version_rect = version.get_rect(center=(surface.get_width() // 2, 150))
        surface.blit(version, version_rect)

        # Button dimensions
        button_width = 200
        button_height = 60
        button_spacing = 80
        start_y = 250

        # Draw buttons
        buttons = ["OFFLINE", "VS AI", "ONLINE", "TRAINING"]
        for i, text in enumerate(buttons):
            button_rect = pygame.Rect(
                (surface.get_width() - button_width) // 2,
                start_y + i * button_spacing,
                button_width,
                button_height,
            )
            is_pressed = self.pressed_button == i
            self._draw_button(surface, text, button_rect, is_pressed)

        if self.input_active:
            self._draw_room_input(surface)

    def handle_events(self, event):
        if self.show_size_selection:
            return self._handle_size_selection(event)
        elif self.mode == GameMode.MENU and not self.input_active:
            return self._handle_main_menu(event)
        elif event.type == pygame.KEYDOWN and self.input_active:
            return self._handle_room_input(event)

        # Check if match is found
        if self.mode == GameMode.WAITING:
            match_status = self.network_manager.check_match_status()
            if match_status:
                self.player_color = match_status
                return GameMode.ONLINE, match_status

        return None, None

    def play_button_sound(self):
        """Play the button press sound effect"""
        self.button_sound.play()

    def _handle_size_selection(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            center_x = pygame.display.get_surface().get_width() // 2
            button_width = 200
            button_height = 60
            button_spacing = 80
            start_y = 300

            mouse_pos = pygame.mouse.get_pos()
            for i in range(2):  # 2 size options
                button_rect = pygame.Rect(
                    center_x - button_width // 2,
                    start_y + i * button_spacing,
                    button_width,
                    button_height,
                )
                if button_rect.collidepoint(mouse_pos):
                    self.pressed_size_button = i
                    self.play_button_sound()  # Play sound when button is pressed
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed_size_button is not None:
                center_x = pygame.display.get_surface().get_width() // 2
                button_width = 200
                button_height = 60
                button_spacing = 80
                start_y = 300

                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(
                    center_x - button_width // 2,
                    start_y + self.pressed_size_button * button_spacing,
                    button_width,
                    button_height,
                )

                if button_rect.collidepoint(mouse_pos):
                    reduced_version = self.pressed_size_button == 1  # 1 is small version
                    self.show_size_selection = False

                    if self.selected_game_mode == GameMode.ONLINE:
                        self.input_active = True
                        self.mode = GameMode.MENU
                        return None, None
                    else:
                        return (
                            self.selected_game_mode,
                            (RED if self.selected_game_mode == GameMode.AI else None),
                            reduced_version,
                        )

            self.pressed_size_button = None

        return None, None

    def _handle_main_menu(self, event):
        center_x = pygame.display.get_surface().get_width() // 2
        button_width = 200
        button_height = 60
        button_spacing = 80
        start_y = 250

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(4):  # 4 buttons total
                button_rect = pygame.Rect(
                    center_x - button_width // 2,
                    start_y + i * button_spacing,
                    button_width,
                    button_height,
                )
                if button_rect.collidepoint(mouse_pos):
                    self.pressed_button = i
                    self.play_button_sound()  # Play sound when button is pressed
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed_button is not None:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(
                    center_x - button_width // 2,
                    start_y + self.pressed_button * button_spacing,
                    button_width,
                    button_height,
                )
                if button_rect.collidepoint(mouse_pos):
                    if self.pressed_button == 0:  # OFFLINE
                        self.selected_game_mode = GameMode.OFFLINE
                    elif self.pressed_button == 1:  # VS AI
                        self.selected_game_mode = GameMode.AI
                    elif self.pressed_button == 2:  # ONLINE
                        self.selected_game_mode = GameMode.ONLINE
                    elif self.pressed_button == 3:  # TRAINING
                        self.selected_game_mode = GameMode.TRAINING

                    self.show_size_selection = True

            self.pressed_button = None

        return None, None

    def _handle_room_input(self, event):
        if event.key == pygame.K_RETURN and self.room_code:
            self.mode = GameMode.WAITING
            self.network_manager.join_room(self.room_code)
            self.input_active = False
            return GameMode.WAITING, None
        elif event.key == pygame.K_BACKSPACE:
            self.room_code = self.room_code[:-1]
        elif len(self.room_code) < 10:  # Limit room code length
            if event.unicode.isalnum():  # Only allow alphanumeric characters
                self.room_code += event.unicode.upper()
        return None, None

    def _draw_room_input(self, surface):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.fill((32, 32, 32))  # Darker overlay
        overlay.set_alpha(200)
        surface.blit(overlay, (0, 0))

        # Draw input box
        prompt = self.title_font.render("Enter Room Code:", True, (208, 208, 208))
        prompt_rect = prompt.get_rect(center=(surface.get_width() // 2, 200))
        surface.blit(prompt, prompt_rect)

        # Input box
        input_rect = pygame.Rect(0, 0, 300, 60)
        input_rect.center = (surface.get_width() // 2, 300)

        pygame.draw.rect(surface, (64, 64, 64), input_rect)
        pygame.draw.rect(surface, (192, 192, 192), input_rect, 1)

        input_text = self.button_font.render(self.room_code, True, (208, 208, 208))
        text_rect = input_text.get_rect(center=input_rect.center)
        surface.blit(input_text, text_rect)

        # Draw instruction
        instruction = self.small_font.render("Press ENTER to join", True, (128, 128, 128))
        instruction_rect = instruction.get_rect(center=(surface.get_width() // 2, 380))
        surface.blit(instruction, instruction_rect)

    def _draw_waiting_screen(self, surface):
        waiting_text = self.title_font.render("Waiting for opponent...", True, (208, 208, 208))
        room_text = self.button_font.render(f"Room: {self.room_code}", True, (208, 208, 208))

        waiting_rect = waiting_text.get_rect(center=(surface.get_width() // 2, 200))
        room_rect = room_text.get_rect(center=(surface.get_width() // 2, 300))

        surface.blit(waiting_text, waiting_rect)
        surface.blit(room_text, room_rect)
