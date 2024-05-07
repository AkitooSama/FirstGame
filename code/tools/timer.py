from pygame.time import get_ticks

class Timer:
	def __init__(self, duration: float, func = None, repeat: bool = False):
		self.duration: float = duration
		self.func = func
		self.start_time: float = 0
		self.active: bool = False
		self.repeat: bool = repeat

	def activate(self) -> None:
		self.active = True
		self.start_time = get_ticks()

	def deactivate(self) -> None:
		self.active = False
		self.start_time = 0
		if self.repeat:
			self.activate()

	def update(self) -> None:
		current_time = get_ticks()
		if current_time - self.start_time >= self.duration:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()

