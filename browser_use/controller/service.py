import logging

from browser_use.agent.views import ActionResult
from browser_use.browser.service import BrowserService
from browser_use.browser.views import BrowserState
from browser_use.controller.views import (
	ControllerActions,
	ControllerPageState,
)
from browser_use.utils import time_execution_sync

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Controller:
	"""
	Controller service that interacts with the browser.

	Right now this is just a LLM friendly wrapper around the browser service.
	In the future we can add the functionality that this is a self-contained agent that can plan and act single steps.

	TODO: easy hanging fruit: pass in a list of actions, compare html that changed and self assess if goal is done -> makes clicking MUCH MUCH faster and cheaper.

	TODO#2: from the state generate functions that can be passed directly into the LLM as function calls. Then it could actually in the same call request for example multiple actions and new state.
	"""

	def __init__(self, keep_open: bool = False):
		self.browser = BrowserService(keep_open=keep_open)
		self.cached_state: BrowserState | None = None

	def get_state(self, screenshot: bool = False) -> ControllerPageState:
		self.cached_state = self.browser.get_state(screenshot=screenshot)
		return self.cached_state

	@time_execution_sync('--act')
	def act(self, action: ControllerActions) -> ActionResult:
		try:
			current_state = self.cached_state

			if action.search_google:
				self.browser.search_google(action.search_google.query)
			elif action.switch_tab:
				self.browser.switch_tab(action.switch_tab.handle)
			elif action.open_tab:
				self.browser.open_tab(action.open_tab.url)
			elif action.go_to_url:
				self.browser.go_to_url(action.go_to_url.url)
			elif action.nothing:
				pass
			elif action.go_back:
				self.browser.go_back()
			elif action.done:
				self.browser.done(action.done.text)
				return ActionResult(is_done=True, extracted_content=action.done.text)
			elif action.click_element:
				self.browser.click_element_by_index(
					action.click_element.index, current_state, action.click_element.num_clicks
				)
			elif action.input_text:
				self.browser.input_text_by_index(
					action.input_text.index, action.input_text.text, current_state
				)
			elif action.extract_page_content:
				content = self.browser.extract_page_content()
				return ActionResult(extracted_content=content)
			else:
				raise ValueError(f'Unknown default action: {action}')

			return ActionResult()

		except Exception as e:
			raise Exception(f'Error while executing action {action}: {str(e)}') from e
