import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

base = 'http://todomvc.com/examples/angularjs/'

class TodoTest(unittest.TestCase):
 
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_addTodo(self):
        self.driver.get(base)
        newTodoInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'new-todo'))
        )
        newTodoInput.send_keys('get eggs')
        newTodoInput.submit()

        self.assertEqual(len(self.driver.find_elements_by_css_selector('#todo-list>li')), 1)

    def test_editTodo(self):
        self.driver.get(base)
        newTodoInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'new-todo'))
        )
        newTodoInput.send_keys('get eggs')
        newTodoInput.submit()

        existingTodo = self.driver.find_elements_by_css_selector('#todo-list>li>div')[0]
        ActionChains(self.driver).double_click(existingTodo).send_keys(Keys.END).send_keys(' and spam\n').perform()

        self.assertEqual(self.driver.find_element_by_css_selector('#todo-list>li>div>label').text, 'get eggs and spam')

    def test_completeTodo(self):
        self.driver.get(base)
        newTodoInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'new-todo'))
        )
        newTodoInput.send_keys('get eggs')
        newTodoInput.submit()

        #complete
        existingTodo = self.driver.find_elements_by_css_selector('#todo-list>li>div>input')[0]
        existingTodo.click()

        self.assertTrue('completed' in self.driver.find_elements_by_css_selector('#todo-list>li')[0].get_attribute('class'))

    def test_reactivateTodo(self):
        self.driver.get(base)
        newTodoInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'new-todo'))
        )
        newTodoInput.send_keys('get eggs')
        newTodoInput.submit()
        
        # complete
        existingTodo = self.driver.find_elements_by_css_selector('#todo-list>li>div>input')[0]
        existingTodo.click()
        #reactivate
        existingTodo = self.driver.find_elements_by_css_selector('#todo-list>li>div>input')[0]
        existingTodo.click()

        self.assertFalse('completed' in self.driver.find_elements_by_css_selector('#todo-list>li')[0].get_attribute('class'))

    def test_addSecondTodo(self):
        self.driver.get(base)
        newTodoInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'new-todo'))
        )
        newTodoInput.send_keys('get eggs')
        newTodoInput.submit()

        # add second
        newTodoInput.send_keys('get more eggs')
        newTodoInput.submit()

        self.assertEqual(len(self.driver.find_elements_by_css_selector('#todo-list>li')), 2)

    def test_completeAllTodos(self):
        self.driver.get(base)
        newTodoInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "new-todo"))
        )
        newTodoInput.send_keys('get eggs')
        newTodoInput.submit()

        # add second
        newTodoInput.send_keys('get more eggs')
        newTodoInput.submit()

        # complete all
        self.driver.find_element_by_id('toggle-all').click()

        # check all are completed
        completedCount = 0
        for element in self.driver.find_elements_by_css_selector('#todo-list>li'):
            if "completed" in element.get_attribute('class'):
                completedCount += 1
        self.assertEqual(completedCount, 2)

    def test_filterCompleted(self):
        self.driver.get(base)
        newTodoInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'new-todo'))
        )
        newTodoInput.send_keys('get eggs')
        newTodoInput.submit()

        # add second
        newTodoInput.send_keys('get more eggs')
        newTodoInput.submit()

        # complete second
        existingTodo = self.driver.find_elements_by_css_selector('#todo-list>li>div>input')[1]
        existingTodo.click()

        # click 'completed'
        self.driver.find_element_by_link_text('Completed').click()

        # check only second is visible
        self.assertEqual(self.driver.find_element_by_css_selector('#todo-list>li>div>label').text, 'get more eggs')

    def test_clickClose(self):
        self.driver.get(base)
        newTodoInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'new-todo'))
        )
        newTodoInput.send_keys('get eggs')
        newTodoInput.submit()

        # add second
        newTodoInput.send_keys('get more eggs')
        newTodoInput.submit()

        # close first, have to put mouse over entry to get close button to appear
        todoEntry = self.driver.find_elements_by_css_selector('#todo-list>li>.view')[0]
        hiddenCloseIcon = self.driver.find_elements_by_css_selector('#todo-list>li>.view>.destroy')[0]
        ActionChains(self.driver).move_to_element(todoEntry).click(hiddenCloseIcon).perform()

        
        # test second (now is first and only element) still present
        self.assertEqual(self.driver.find_element_by_css_selector('#todo-list>li>div>label').text, 'get more eggs')

    def test_closeAllCompletedTodos(self):
        self.driver.get(base)
        newTodoInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'new-todo'))
        )
        newTodoInput.send_keys('get eggs')
        newTodoInput.submit()

        #complete
        existingTodo = self.driver.find_elements_by_css_selector('#todo-list>li>div>input')[0]
        existingTodo.click()

        self.driver.find_element_by_id('clear-completed')

        self.assertEqual(len(self.driver.find_elements_by_css_selector('#todo-list>li')), 1)


if __name__ == '__main__':
    unittest.main()

'''
# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# go to the base page
driver.get(base)

newTodoInput = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "new-todo"))
)

# find new-todo element
#inputElement = driver.find_element_by_id("new-todo")

# type in the search
newTodoInput.send_keys("get eggs")

# submit the form
newTodoInput.submit()

#2. edit existing To-do
existingTodo = driver.find_elements_by_css_selector("#todo-list>li>div")[0]
ActionChains(driver).double_click(existingTodo).send_keys(" and spam\n").perform()


#3. complete a To-do
existingTodo = driver.find_elements_by_css_selector("#todo-list>li>div>input")[0]
existingTodo.click()

#4. reactivate a completed To-do
existingTodo = driver.find_elements_by_css_selector("#todo-list>.completed>div>input")[0]
existingTodo.click()

#5. add a second To-do
newTodoInput.send_keys("get more eggs")
newTodoInput.submit()

#6.
driver.find_element_by_id("toggle-all").click()

#7.
driver.find_element_by_link_text("Completed").click()

#8.
todoEntry = driver.find_elements_by_css_selector("#todo-list>li>.view")[0]
hiddenCloseIcon = driver.find_elements_by_css_selector("#todo-list>li>.view>.destroy")[0]

ActionChains(driver).move_to_element(todoEntry).click(hiddenCloseIcon).perform()

#9.
driver.find_element_by_id("clear-completed").click()
'''