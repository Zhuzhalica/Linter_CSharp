from linter import Linter
from rules import Rules
import unittest

class TestLinter(unittest.TestCase):
    def setUp(self):
        self.rules = Rules('C:\\Users\\German\\Linter_CSharp\\Tests\\r1.json')
        self.linter = Linter(self.rules)

    def test_init(self):
        self.assertEqual(self.linter.rules, self.rules)

    def test_number_line(self):
        self.assertEqual(self.linter.number_line, 1)

    def test_enters_count(self):
        self.assertEqual(self.linter.enters_count, 0)

    def test_offset_level(self):
        self.assertEqual(self.linter.offset_level, 0)

    def test_check_separate_symbol(self):
        self.linter.check_separate_symbol("v += 2; ;")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_separate_symbol_with_tab(self):
        self.linter.check_separate_symbol("var l = new List<int>();  ")
        self.assertEqual(len(self.linter.errors), 0)

    def test_check_class_variable_declaration(self):
        self.assertEqual(len(self.linter.find_classes_variable_declaration("public static int N = 1;")), 0)

    def test_check_class_variable_name(self):
        self.linter.check_class_variable_name("public static  HashSet<int> t = new HashSet<int>();")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_line_length(self):
        line = "                                var Lsost = line.Split(' ').Where(x => x.Length > 0).Select(x => int.Parse(x)).ToArray();"
        self.linter.check_line_length(line)
        self.assertEqual(len(self.linter.errors), 1)

    def test_get_variable_name(self):
        self.assertEqual(self.linter.get_variable_name("var result = 0;"), "result")

    def test_get_variable_name_(self):
        self.assertEqual(self.linter.get_variable_name("var Users = new List<int>();"), "Users")

    def test_check_bracket_line(self):
        self.linter.check_bracket_line("}s")
        self.assertEqual(len(self.linter.errors), 1)

    def test_get_method_name(self):
        name = self.linter.get_method_name("private static void FindResult ()")
        self.assertEqual(name, "FindResult")

    def test_check_correspondence_alphabet(self):
        self.linter.check_correspondence_alphabet("resultsК")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_variable_name(self):
        self.linter.check_variable_name("ListUsers")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_method_name_without_error(self):
        self.linter.check_method_name("FindResultGraph")
        self.assertEqual(len(self.linter.errors), 0)

    def test_check_method_name_with_error(self):
        self.linter.check_method_name("findResultGraph")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_enters(self):
        self.linter.check_enters("public static void GetAnswer (int[] S,List<string> words)    ")
        self.assertEqual(len(self.linter.errors), 0)

    def test_check_count_tabulation(self):
        self.linter.check_count_tabulation("    var v =0;")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_count_spaces(self):
        self.linter.check_spaces("var v =0;")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_extra_spaces(self):
        self.linter.check_spaces("public static  HashSet<int> T;")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_extra_spaces_before(self):
        self.linter.check_spaces("static void Main ()")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_spaces_end_line(self):
        self.linter.check_spaces("public void FindResult()  ")
        self.assertEqual(len(self.linter.errors), 1)

    def test_is_method_declaration(self):
        method = "public static void GetAnswer(int[] S, List<string> words)"
        v = self.linter.find_method_declaration(method)
        self.assertEqual(v[0],method)

    def test_check_calculate_level_tabulation(self):
        self.linter.calculate_level_tabulation("    {")
        self.assertEqual(self.linter.offset_level, 1)

    def test_check_calculate_level_tab(self):
        self.linter.calculate_level_tabulation("    }")
        self.assertEqual(self.linter.offset_level, -1)

    def test_find_common_variable_declaration(self):
        variable = self.linter.find_common_variable_declaration("for (var i=0; i < 5; i++)")
        self.assertEqual(len(variable), 1)

    def test_find_methods_variable_declaration(self):
        variables = self.linter.find_methods_variable_declaration('var l = int.Parse("ste");')
        self.assertEqual(len(variables), 1)

    def test_check_class_name(self):
        self.linter.in_method = True
        self.linter.check_class_variable_name("var s = Console.ReadLine().Split();")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_variable_usage_line(self):
        self.linter.dict_variables["r"] = [19,19]
        self.linter.number_line = 21
        self.linter.check_variable_usage_line("var s = r + 10;")
        self.assertEqual(len(self.linter.dict_variables["r"]), 3)

    def test_check_variable_usage(self):
        self.linter.dict_variables["r"] = [19, 19, 20]
        self.linter.dict_variables["S"] = [21, 21]
        self.linter.check_variables_usage()
        self.assertEqual(len(self.linter.errors), 1)

    def test_variable_check_out_method(self):
        self.linter.in_method = False
        self.linter.check_variable("var s = Console.Readline().Split();")
        self.assertEqual(len(self.linter.errors), 1)

    def test_variable_check_in_method(self):
        self.linter.in_method = True
        self.linter.check_variable("var s = Console.Readline().Split();")
        self.assertEqual(len(self.linter.errors), 0)

    def test_variable_check_in_class(self):
        self.linter.in_method = True
        self.linter.check_variable("public int N = 5;")
        self.assertEqual(len(self.linter.errors), 1)

    def test_variable_check_in_class_out_method(self):
        self.linter.in_method = False
        self.linter.check_variable("public int Number = 5;")
        self.assertEqual(len(self.linter.errors), 1)

    def test_configure_options_class(self):
        self.linter.configure_options("class")
        self.assertTrue(self.linter.variable_check)
        self.assertFalse(self.linter.separator_check)

    def test_configure_options_namespace(self):
        self.linter.configure_options("namespace")
        self.assertFalse(self.linter.separator_check)

    def test_configure_options_command(self):
        for command in self.rules.tabulation_after_command:
            self.linter.configure_options(command)
            self.assertFalse(self.linter.separator_check)

    def test_check_first_line_in_method_with_brackets(self):
        self.linter.in_method = True
        self.linter.first_inner_line_func = True
        self.linter.check_first_line_in_method("    {")
        self.assertEqual(len(self.linter.errors), 0)

    def test_check_first_line_in_method(self):
        self.linter.in_method = True
        self.linter.first_inner_line_func = True
        self.linter.offset_level = 1
        self.linter.check_first_line_in_method("        h.Add(t);")
        self.assertEqual(len(self.linter.errors), 0)

    def test_check_method_end(self):
        self.linter.in_method = True
        self.linter.method_start_offset_level = 1
        self.linter.offset_level = 1
        self.linter.check_method_end()
        self.assertFalse(self.linter.in_method)
        self.assertEqual(self.linter.method_start_offset_level, -1)

    def test_closed_brackets(self):
        self.linter.offset_level = 1
        self.linter.check_closed_brackets("}")
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_content_method_in_method(self):
        self.linter.in_method = True
        self.linter.check_content_method_in_method('            public static void GetAnswer(int k)')
        self.assertEqual(len(self.linter.errors), 1)

    def test_check_content_method_out_method(self):
        self.linter.in_method = False
        self.linter.check_content_method_in_method('        public static void GetAnswer(int k)')
        self.assertEqual(len(self.linter.errors), 0)

    def test_run(self):
        self.linter.run("C:\\Users\\German\\Linter_CSharp\\Tests\\DM.cs")
        self.assertEqual(len(self.linter.errors), 9)
