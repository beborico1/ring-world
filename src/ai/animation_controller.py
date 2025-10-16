from ..utils.settings import DEFAULT_ROTATION_DURATION


class AnimationController:
    """Handles animation-related operations"""

    def __init__(self, circle_system):
        self.system = circle_system
        self.default_rotation_duration = DEFAULT_ROTATION_DURATION  # Store default duration
        self.current_rotation_duration = self.default_rotation_duration

    def set_animation_duration(self, duration: float):
        """Set animation duration for all animation handlers"""
        self.current_rotation_duration = duration
        self.system.animation_handler.rotation_duration = duration
        # Individual controller durations will be updated through the animation_handler's
        # rotation_duration property setter, so we don't need to set them individually anymore

    def reset_animation_duration(self):
        """Reset animation duration to default for all handlers"""
        self.set_animation_duration(self.default_rotation_duration)

    def wait_for_animations(self):
        """Wait for all animations to complete before proceeding."""
        while self.system.is_any_circle_animating():
            self.system.animation_handler.update()
            self.system.update()
