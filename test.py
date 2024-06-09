import sys
import unittest

from PyQt5 import QtWidgets

from main import Ui_MainWindow
from models import Cartridge


class TestMainWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        obj = Ui_MainWindow(MainWindow)
        obj.setupUi(MainWindow)

        # Заполняем новыми данными
        cartridges_info = [
            # Индекс типа банкноты, кол-во банкнот, неисправна
            (0, 1, False),
            (1, 8, False),
            (2, 1, False),
            (3, 2, False),
        ]
        for i, cartridge_info in enumerate(cartridges_info):
            banknote_type_index = cartridge_info[0]
            banknote_type = obj.banknote_types[banknote_type_index]
            quantity = cartridge_info[1]

            cartridge = Cartridge(
                number=i,
                banknote_type=banknote_type,
                banknote_type_index=banknote_type_index,
                quantity=quantity,
                quantity_temp=quantity,
                broken=cartridge_info[2],
                dynamic=0,
                dynamic_temp=0,
            )
            obj.cartridges_type_objs_dict[banknote_type].append(cartridge)
            obj.cartridges.append(cartridge)

        obj.test_mode = True
        cls.obj = obj

    def test_calc_result_1800(self):

        self.sum_test = 1800
        self.obj.num_money = self.sum_test
        self.obj.num_money_temp = self.sum_test

        self.obj.calc_result()

        sum_result = 0
        for cartridge in self.obj.cartridges:
            sum_result += (cartridge.banknote_type * cartridge.dynamic)

        self.assertEqual(self.sum_test, sum_result)

    def test_calc_result_1600(self):

        self.sum_test = 1600
        self.obj.num_money = self.sum_test
        self.obj.num_money_temp = self.sum_test

        self.obj.calc_result()

        sum_result = 0
        for cartridge in self.obj.cartridges:
            sum_result += (cartridge.banknote_type * cartridge.dynamic)

        self.assertEqual(self.sum_test, sum_result)


if __name__ == '__main__':
    unittest.main()
