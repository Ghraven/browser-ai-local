import time

from browser_use.browser.service import BrowserService
from browser_use.controller.service import ControllerService
from browser_use.controller.views import (
	ClickElementControllerAction,
	ControllerActions,
	GoToUrlControllerAction,
)
from browser_use.dom.service import DomService
from browser_use.utils import time_execution_sync


def test_highlight_elements():
	controller = ControllerService()

	controller.act(ControllerActions(go_to_url=GoToUrlControllerAction(url='https://www.kayak.ch')))
	# browser.go_to_url('https://google.com/flights')
	# browser.go_to_url('https://immobilienscout24.de')

	time.sleep(1)
	# browser._click_element_by_xpath(
	# 	'/html/body/div[5]/div/div[2]/div/div/div[3]/div/div[1]/button[1]'
	# )
	# browser._click_element_by_xpath("//button[div/div[text()='Alle akzeptieren']]")

	while True:
		state = controller.get_current_state()

		time_execution_sync('highlight_selector_map_elements')(
			controller.browser.highlight_selector_map_elements
		)(state.selector_map)

		print(state.dom_items_to_string(use_tabs=False))
		# print(state.selector_map)

		# Find and print duplicate XPaths
		xpath_counts = {}
		for selector in state.selector_map.values():
			if selector in xpath_counts:
				xpath_counts[selector] += 1
			else:
				xpath_counts[selector] = 1

		print('\nDuplicate XPaths found:')
		for xpath, count in xpath_counts.items():
			if count > 1:
				print(f'XPath: {xpath}')
				print(f'Count: {count}\n')

		action = input('Select next action: ')

		time_execution_sync('remove_highlight_elements')(controller.browser.remove_highlights)()

		next_action = ControllerActions(click_element=ClickElementControllerAction(id=int(action)))

		controller.act(next_action)


def main():
	test_highlight_elements()


if __name__ == '__main__':
	main()