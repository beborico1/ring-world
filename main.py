"""
Main entry point for Ring World game - Web compatible version
This file is specifically for Pygbag web deployment
"""
import asyncio
import pygame
import sys

# For web deployment, we need to use asyncio
try:
    import platform
    if platform.system() == "Emscripten":
        # Running in browser
        RUNNING_IN_BROWSER = True
    else:
        RUNNING_IN_BROWSER = False
except:
    RUNNING_IN_BROWSER = False

from src.game import Game

async def main():
    """Async main function for web compatibility"""
    game = Game()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            # Delegate event handling to game
            game.controller.current_time = pygame.time.get_ticks()

            # Handle debug events first if in gameplay modes
            from src.utils.settings import GameMode
            if game.controller.game_mode not in [GameMode.MENU, GameMode.WAITING]:
                if game.controller.managers["render"].handle_debug_events(event):
                    if game.controller.systems["circle"]:
                        game.controller.systems["circle"].update_adjacent_connections()
                    continue

            # Process game event
            if game.controller.game_mode in [GameMode.MENU, GameMode.WAITING]:
                result = game.controller.systems["menu"].handle_events(event)
                if result is not None:
                    if len(result) == 2:
                        new_mode, color = result
                        reduced_version = False
                    else:
                        new_mode, color, reduced_version = result

                    if new_mode:
                        game.set_game_mode(new_mode, reduced_version)
                        game.controller.player_color = color

            elif game.controller.game_mode == GameMode.TRAINING:
                if game.controller.systems["circle"] and game.controller.event_handler:
                    game.controller.event_handler.handle_events(event)

            elif game.controller.game_mode in [GameMode.OFFLINE, GameMode.ONLINE, GameMode.AI]:
                if game.controller.systems["circle"]:
                    can_move = (
                        game.controller.game_mode == GameMode.OFFLINE
                        or (
                            game.controller.game_mode == GameMode.ONLINE
                            and game.controller.player_color
                            == game.controller.systems["circle"].game_state.turn
                        )
                        or (
                            game.controller.game_mode == GameMode.AI
                            and game.controller.systems["circle"].game_state.turn == "red"
                        )
                    )

                    if can_move:
                        game.controller.systems["circle"].handle_events(event)

        if not running:
            break

        # Update game state
        from src.utils.settings import GameMode
        if game.controller.game_mode in [GameMode.ONLINE, GameMode.WAITING]:
            new_mode, new_color = game.controller.managers["network"].handle_network_messages(
                game.controller.game_mode,
                game.controller.systems["circle"],
                game.controller.player_color,
            )
            if new_mode:
                game.controller.game_mode = new_mode
                game.controller.player_color = new_color

            if game.controller.game_mode == GameMode.ONLINE:
                game.controller.managers["network"].handle_online_moves(
                    game.controller.systems["circle"]
                )

        elif game.controller.game_mode == GameMode.AI and game.controller.ai_player:
            game.controller.ai_player.make_move()
        elif game.controller.game_mode == GameMode.TRAINING:
            game.controller.update_ai_players()

        # Update circle system if it exists
        if game.controller.systems["circle"]:
            game.controller.systems["circle"].update()

        # Update training stats before rendering
        game.controller.update_training_stats()

        # Render frame
        game.controller.managers["render"].render_frame(
            game.controller.game_mode,
            game.controller.systems,
        )

        game.controller.clock.tick(60)

        # This is crucial for Pygbag - yield control to browser
        await asyncio.sleep(0)

    # Cleanup
    from src.utils.settings import GameMode
    if game.controller.game_mode == GameMode.ONLINE:
        game.controller.managers["network"].network_manager.shutdown()
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
