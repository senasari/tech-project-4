from mock import patch

import log_book
import unittest


class TestLogbook(unittest.TestCase):

    def setUp(self):
        self.entry_len_before_test = len(log_book.Entry.select())
        self.name = 'sena'
        self.date = '2018-10-07'
        self.task = 'task1'
        self.timespent = '90'
        self.notes = 'notes'

    def tearDown(self):
        """deletes any entry created for testing purposes"""
        if self.entry_len_before_test < len(log_book.Entry.select()):
            log_book.Entry.select()[0].delete_instance()

    def test_menu_loop_add_entree_and_exit(self):
        """tests if adding entry and then exiting works"""
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect=['a', self.name, self.task, self.timespent, self.notes, 's', 'q']):
                log_book.menu_loop()

    def test_menu_loop_search_entree_by_employee_and_exit(self):
        """tests searching entry by their name"""
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect=['s', 'n', self.name, 'r', 'r',  'q']):
                log_book.menu_loop()

    def test_menu_loop_search_entree_by_date_and_exit(self):
        """tests searching entry by date"""
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect=['s', 'd', self.date, 'r', 'r',  'q']):
                log_book.menu_loop()

    def test_menu_loop_search_entree_by_task_and_exit(self):
        """tests searching entry by task name"""
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect=['s', 't', self.task, 'r', 'r',  'q']):
                log_book.menu_loop()

    def test_menu_loop_search_entree_by_timespent_and_exit(self):
        """tests searching entry by timespent"""
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect=['s', 'ts', self.timespent, 'r', 'r',  'q']):
                log_book.menu_loop()

    def test_menu_loop_search_entree_by_term_in_tasks_and_notes(self):
        """tests searching entry by term in tasks and notes """
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect=['s', 't', '', 'r', 'r',  'q']):
                log_book.menu_loop()

    def test_add_entree_with_negative_timespent_raise_error(self):
        """when adding an entree with a negative timespent checks if it raises error"""
        with self.assertRaises(SystemExit):
            with self.assertRaises(ValueError):
                with patch('builtins.input', side_effect=['a', self.name, self.task, '-45', self.timespent,
                                                          'any note', 'r', 'q']):
                    log_book.menu_loop()

    def test_menu_loop_view_next_and_previous_and_exit(self):
        """testing next and previous options"""
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect=['v', 'n', 'p', 'r', 'q']):
                log_book.menu_loop()

    def test_menu_loop_valid_choice_loop(self):
        """tests if the choice is still valid after the security while loop for choice to be valid"""
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect=['fk;adlsfjs;kf', 'k;fdlsf;ajsd;fkd', ';fdklsjf;ksaj', 'f;dlkf', 'q']):
                log_book.menu_loop()

    def test_search_menu_loop_valid_choice_loop(self):
        """tests if the choice is valid after the security while loop for choice to be valid"""
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect=['fk;adlsfjs;kf','k;fdlsf;ajsd;fkd',
                                                      ';fdklsjf;ksaj', 'f;dlkf', 'r', 'q']):
                log_book.search_entry()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
