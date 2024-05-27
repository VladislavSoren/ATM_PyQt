import logging
import time

from PyQt5 import QtCore, QtWidgets

from config import BANKNOTE_TYPES, MAX_CARTRIDGES, MAX_QUANTITY_BANKNOTES, MAX_QUANTITY_SUM
from dop import log_time
from models import Cartridge, CartridgeInfoGen, Status

# Параметры логирования
logging.basicConfig(filename="py_log.log",
                    filemode="w",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Ui_MainWindow(object):

    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.num_money_temp = 0
        self.banknote_types = sorted(BANKNOTE_TYPES)
        self.cartridges_type_objs_dict = {}
        self.cartridges = []
        for banknote_type in self.banknote_types:
            self.cartridges_type_objs_dict[int(banknote_type)] = []
        self.start_banknote_type_index = -1
        self.result_status = None
        self.calc_time = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.num_cartridges = QtWidgets.QSpinBox(self.centralwidget)
        self.num_cartridges.setGeometry(QtCore.QRect(30, 10, 140, 30))
        self.num_cartridges.setMaximum(MAX_CARTRIDGES)
        self.num_cartridges.setObjectName("num_cartridges")

        self.btn_calc_result = QtWidgets.QPushButton(self.centralwidget)
        self.btn_calc_result.setGeometry(QtCore.QRect(300, 310, 131, 61))
        self.btn_calc_result.setObjectName("btn_calc_result")

        self.btn_randomise = QtWidgets.QPushButton(self.centralwidget)
        self.btn_randomise.setGeometry(QtCore.QRect(100, 310, 185, 61))
        self.btn_randomise.setObjectName("btn_randomise")

        self.num_money = QtWidgets.QSpinBox(self.centralwidget)
        self.num_money.setGeometry(QtCore.QRect(330, 10, 140, 30))
        self.num_money.setMaximum(MAX_QUANTITY_SUM)
        self.num_money.setObjectName("num_money")

        # splitter
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(30, 60, 341, 19))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_n_0 = QtWidgets.QLabel(self.splitter)
        self.label_n_0.setObjectName("label_n_0")
        self.box_banknote_type_0 = QtWidgets.QComboBox(self.splitter)
        self.box_banknote_type_0.setEditable(False)
        self.box_banknote_type_0.setObjectName("box_banknote_type_0")
        self.num_remaining_quantity_0 = QtWidgets.QSpinBox(self.splitter)
        self.num_remaining_quantity_0.setMaximum(MAX_QUANTITY_BANKNOTES)
        self.num_remaining_quantity_0.setObjectName("num_remaining_quantity_0")
        self.label_dynamic_0 = QtWidgets.QLabel(self.splitter)
        self.label_dynamic_0.setObjectName("label_dynamic_0")
        self.flag_broken_0 = QtWidgets.QCheckBox(self.splitter)
        self.flag_broken_0.setObjectName("flag_broken_0")

        # splitter_1
        self.splitter_1 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_1.setGeometry(QtCore.QRect(30, 90, 341, 19))
        self.splitter_1.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_1.setObjectName("splitter_1")
        self.label_n_1 = QtWidgets.QLabel(self.splitter_1)
        self.label_n_1.setObjectName("label_n_1")
        self.box_banknote_type_1 = QtWidgets.QComboBox(self.splitter_1)
        self.box_banknote_type_1.setEditable(False)
        self.box_banknote_type_1.setObjectName("box_banknote_type_1")
        self.num_remaining_quantity_1 = QtWidgets.QSpinBox(self.splitter_1)
        self.num_remaining_quantity_1.setMaximum(MAX_QUANTITY_BANKNOTES)
        self.num_remaining_quantity_1.setObjectName("num_remaining_quantity_1")
        self.label_dynamic_1 = QtWidgets.QLabel(self.splitter_1)
        self.label_dynamic_1.setObjectName("label_dynamic_1")
        self.flag_broken_1 = QtWidgets.QCheckBox(self.splitter_1)
        self.flag_broken_1.setObjectName("flag_broken_1")

        # splitter_2
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setGeometry(QtCore.QRect(30, 120, 341, 19))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.label_n_2 = QtWidgets.QLabel(self.splitter_2)
        self.label_n_2.setObjectName("label_n_2")
        self.box_banknote_type_2 = QtWidgets.QComboBox(self.splitter_2)
        self.box_banknote_type_2.setEditable(False)
        self.box_banknote_type_2.setObjectName("box_banknote_type_2")
        self.num_remaining_quantity_2 = QtWidgets.QSpinBox(self.splitter_2)
        self.num_remaining_quantity_2.setMaximum(MAX_QUANTITY_BANKNOTES)
        self.num_remaining_quantity_2.setObjectName("num_remaining_quantity_2")
        self.label_dynamic_2 = QtWidgets.QLabel(self.splitter_2)
        self.label_dynamic_2.setObjectName("label_dynamic_2")
        self.flag_broken_2 = QtWidgets.QCheckBox(self.splitter_2)
        self.flag_broken_2.setObjectName("flag_broken_2")

        # splitter_3
        self.splitter_3 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_3.setGeometry(QtCore.QRect(30, 150, 341, 19))
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.label_n_3 = QtWidgets.QLabel(self.splitter_3)
        self.label_n_3.setObjectName("label_n_3")
        self.box_banknote_type_3 = QtWidgets.QComboBox(self.splitter_3)
        self.box_banknote_type_3.setEditable(False)
        self.box_banknote_type_3.setObjectName("box_banknote_type_3")
        self.num_remaining_quantity_3 = QtWidgets.QSpinBox(self.splitter_3)
        self.num_remaining_quantity_3.setMaximum(MAX_QUANTITY_BANKNOTES)
        self.num_remaining_quantity_3.setObjectName("num_remaining_quantity_3")
        self.label_dynamic_3 = QtWidgets.QLabel(self.splitter_3)
        self.label_dynamic_3.setObjectName("label_dynamic_3")
        self.flag_broken_3 = QtWidgets.QCheckBox(self.splitter_3)
        self.flag_broken_3.setObjectName("flag_broken_3")

        # splitter_4
        self.splitter_4 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_4.setGeometry(QtCore.QRect(30, 180, 341, 19))
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.label_n_4 = QtWidgets.QLabel(self.splitter_4)
        self.label_n_4.setObjectName("label_n_4")
        self.box_banknote_type_4 = QtWidgets.QComboBox(self.splitter_4)
        self.box_banknote_type_4.setEditable(False)
        self.box_banknote_type_4.setObjectName("box_banknote_type_4")
        self.num_remaining_quantity_4 = QtWidgets.QSpinBox(self.splitter_4)
        self.num_remaining_quantity_4.setMaximum(MAX_QUANTITY_BANKNOTES)
        self.num_remaining_quantity_4.setObjectName("num_remaining_quantity_4")
        self.label_dynamic_4 = QtWidgets.QLabel(self.splitter_4)
        self.label_dynamic_4.setObjectName("label_dynamic_4")
        self.flag_broken_4 = QtWidgets.QCheckBox(self.splitter_4)
        self.flag_broken_4.setObjectName("flag_broken_4")

        # splitter_5
        self.splitter_5 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_5.setGeometry(QtCore.QRect(30, 210, 341, 19))
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.label_n_5 = QtWidgets.QLabel(self.splitter_5)
        self.label_n_5.setObjectName("label_n_5")
        self.box_banknote_type_5 = QtWidgets.QComboBox(self.splitter_5)
        self.box_banknote_type_5.setEditable(False)
        self.box_banknote_type_5.setObjectName("box_banknote_type_5")
        self.num_remaining_quantity_5 = QtWidgets.QSpinBox(self.splitter_5)
        self.num_remaining_quantity_5.setMaximum(MAX_QUANTITY_BANKNOTES)
        self.num_remaining_quantity_5.setObjectName("num_remaining_quantity_5")
        self.label_dynamic_5 = QtWidgets.QLabel(self.splitter_5)
        self.label_dynamic_5.setObjectName("label_dynamic_5")
        self.flag_broken_5 = QtWidgets.QCheckBox(self.splitter_5)
        self.flag_broken_5.setObjectName("flag_broken_5")

        # splitter_6
        self.splitter_6 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_6.setGeometry(QtCore.QRect(30, 240, 341, 19))
        self.splitter_6.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_6.setObjectName("splitter_6")
        self.label_n_6 = QtWidgets.QLabel(self.splitter_6)
        self.label_n_6.setObjectName("label_n_6")
        self.box_banknote_type_6 = QtWidgets.QComboBox(self.splitter_6)
        self.box_banknote_type_6.setEditable(False)
        self.box_banknote_type_6.setObjectName("box_banknote_type_6")
        self.num_remaining_quantity_6 = QtWidgets.QSpinBox(self.splitter_6)
        self.num_remaining_quantity_6.setMaximum(MAX_QUANTITY_BANKNOTES)
        self.num_remaining_quantity_6.setObjectName("num_remaining_quantity_6")
        self.label_dynamic_6 = QtWidgets.QLabel(self.splitter_6)
        self.label_dynamic_6.setObjectName("label_dynamic_6")
        self.flag_broken_6 = QtWidgets.QCheckBox(self.splitter_6)
        self.flag_broken_6.setObjectName("flag_broken_6")

        # splitter_7
        self.splitter_7 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_7.setGeometry(QtCore.QRect(30, 270, 341, 19))
        self.splitter_7.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_7.setObjectName("splitter_7")
        self.label_n_7 = QtWidgets.QLabel(self.splitter_7)
        self.label_n_7.setObjectName("label_n_7")
        self.box_banknote_type_7 = QtWidgets.QComboBox(self.splitter_7)
        self.box_banknote_type_7.setEditable(False)
        self.box_banknote_type_7.setObjectName("box_banknote_type_7")
        self.num_remaining_quantity_7 = QtWidgets.QSpinBox(self.splitter_7)
        self.num_remaining_quantity_7.setMaximum(MAX_QUANTITY_BANKNOTES)
        self.num_remaining_quantity_7.setObjectName("num_remaining_quantity_7")
        self.label_dynamic_7 = QtWidgets.QLabel(self.splitter_7)
        self.label_dynamic_7.setObjectName("label_dynamic_7")
        self.flag_broken_7 = QtWidgets.QCheckBox(self.splitter_7)
        self.flag_broken_7.setObjectName("flag_broken_7")

        # Результаты
        self.splitter_res = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_res.setGeometry(QtCore.QRect(50, 370, 400, 60))
        self.splitter_res.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_res.setObjectName("splitter_res")
        self.label_result = QtWidgets.QLabel(self.splitter_res)
        self.label_result.setObjectName("label_result")
        self.label_calc_time = QtWidgets.QLabel(self.splitter_res)
        self.label_calc_time.setObjectName("label_calc_time")
        self.label_mks = QtWidgets.QLabel(self.splitter_res)
        self.label_mks.setObjectName("label_mks")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # События
        self.num_cartridges.valueChanged.connect(self.num_cartridges_changed)
        self.num_money.valueChanged.connect(self.num_money_changed)
        self.btn_calc_result.clicked.connect(self.calc_result)
        self.btn_randomise.clicked.connect(self.btn_randomise_clicked)

        # Кассета_0
        self.box_banknote_type_0.currentIndexChanged.connect(self.dropbox_0_changed)
        self.num_remaining_quantity_0.valueChanged.connect(self.num_remaining_quantity_0_changed)
        self.flag_broken_0.stateChanged.connect(self.flag_broken_0_changed)

        # Кассета_1
        self.box_banknote_type_1.currentIndexChanged.connect(self.dropbox_1_changed)
        self.num_remaining_quantity_1.valueChanged.connect(self.num_remaining_quantity_1_changed)
        self.flag_broken_1.stateChanged.connect(self.flag_broken_1_changed)

        # Кассета_2
        self.box_banknote_type_2.currentIndexChanged.connect(self.dropbox_2_changed)
        self.num_remaining_quantity_2.valueChanged.connect(self.num_remaining_quantity_2_changed)
        self.flag_broken_2.stateChanged.connect(self.flag_broken_2_changed)

        # Кассета_3
        self.box_banknote_type_3.currentIndexChanged.connect(self.dropbox_3_changed)
        self.num_remaining_quantity_3.valueChanged.connect(self.num_remaining_quantity_3_changed)
        self.flag_broken_3.stateChanged.connect(self.flag_broken_3_changed)

        # Кассета_4
        self.box_banknote_type_4.currentIndexChanged.connect(self.dropbox_4_changed)
        self.num_remaining_quantity_4.valueChanged.connect(self.num_remaining_quantity_4_changed)
        self.flag_broken_4.stateChanged.connect(self.flag_broken_4_changed)

        # Кассета_5
        self.box_banknote_type_5.currentIndexChanged.connect(self.dropbox_5_changed)
        self.num_remaining_quantity_5.valueChanged.connect(self.num_remaining_quantity_5_changed)
        self.flag_broken_5.stateChanged.connect(self.flag_broken_5_changed)

        # Кассета_6
        self.box_banknote_type_6.currentIndexChanged.connect(self.dropbox_6_changed)
        self.num_remaining_quantity_6.valueChanged.connect(self.num_remaining_quantity_6_changed)
        self.flag_broken_6.stateChanged.connect(self.flag_broken_6_changed)

        # Кассета_7
        self.box_banknote_type_7.currentIndexChanged.connect(self.dropbox_7_changed)
        self.num_remaining_quantity_7.valueChanged.connect(self.num_remaining_quantity_7_changed)
        self.flag_broken_7.stateChanged.connect(self.flag_broken_7_changed)

        # Дефолтная видимость
        self.splitter.hide()
        self.splitter_1.hide()
        self.splitter_2.hide()
        self.splitter_3.hide()
        self.splitter_4.hide()
        self.splitter_5.hide()
        self.splitter_6.hide()
        self.splitter_7.hide()

    def dropbox_changed(self, index, box_banknote_type):
        # Переносим изменённую кассету в раздел с выбранным типом
        for i, cartridge in enumerate(self.cartridges_type_objs_dict[self.cartridges[index].banknote_type]):
            if cartridge.number == index:
                index_del = i
        # Удаляем элемент по найденному индексу
        self.cartridges_type_objs_dict[self.cartridges[index].banknote_type].pop(index_del)

        # Заносим кассету в слот с другим типом
        self.cartridges_type_objs_dict[int(box_banknote_type.currentText())].append(self.cartridges[index])

        # Меняем значения типов в объекте самой кассеты
        self.cartridges[index].banknote_type = int(box_banknote_type.currentText())
        self.cartridges[index].banknote_type_index = int(box_banknote_type.currentIndex())

    # События по изменениям номиналов кассет
    def dropbox_0_changed(self):
        print(f'dropbox_0_changed')
        self.dropbox_changed(0, self.box_banknote_type_0)

    def dropbox_1_changed(self):
        print('dropbox_1_changed')
        self.dropbox_changed(1, self.box_banknote_type_1)

    def dropbox_2_changed(self):
        print('dropbox_2_changed')
        self.dropbox_changed(2, self.box_banknote_type_2)

    def dropbox_3_changed(self):
        print('dropbox_3_changed')
        self.dropbox_changed(3, self.box_banknote_type_3)

    def dropbox_4_changed(self):
        print('dropbox_4_changed')
        self.dropbox_changed(4, self.box_banknote_type_4)

    def dropbox_5_changed(self):
        print('dropbox_5_changed')
        self.dropbox_changed(5, self.box_banknote_type_5)

    def dropbox_6_changed(self):
        print('dropbox_6_changed')
        self.dropbox_changed(6, self.box_banknote_type_6)

    def dropbox_7_changed(self):
        print('dropbox_7_changed')
        self.dropbox_changed(6, self.box_banknote_type_7)

    # События по изменениям кол-ва банкнот в кассетах
    def num_remaining_quantity_0_changed(self):
        index = 0
        print(f'num_remaining_quantity_{index}_changed')
        self.cartridges[index].quantity = self.num_remaining_quantity_0.value()
        self.cartridges[index].quantity_temp = self.num_remaining_quantity_0.value()

    def num_remaining_quantity_1_changed(self):
        index = 1
        print(f'num_remaining_quantity_{index}_changed')
        self.cartridges[index].quantity = self.num_remaining_quantity_1.value()
        self.cartridges[index].quantity_temp = self.num_remaining_quantity_1.value()

    def num_remaining_quantity_2_changed(self):
        index = 2
        print(f'num_remaining_quantity_{index}_changed')
        self.cartridges[index].quantity = self.num_remaining_quantity_2.value()
        self.cartridges[index].quantity_temp = self.num_remaining_quantity_2.value()

    def num_remaining_quantity_3_changed(self):
        index = 3
        print(f'num_remaining_quantity_{index}_changed')
        self.cartridges[index].quantity = self.num_remaining_quantity_3.value()
        self.cartridges[index].quantity_temp = self.num_remaining_quantity_3.value()

    def num_remaining_quantity_4_changed(self):
        index = 4
        print(f'num_remaining_quantity_{index}_changed')
        self.cartridges[index].quantity = self.num_remaining_quantity_4.value()
        self.cartridges[index].quantity_temp = self.num_remaining_quantity_4.value()

    def num_remaining_quantity_5_changed(self):
        index = 5
        print(f'num_remaining_quantity_{index}_changed')
        self.cartridges[index].quantity = self.num_remaining_quantity_5.value()
        self.cartridges[index].quantity_temp = self.num_remaining_quantity_5.value()

    def num_remaining_quantity_6_changed(self):
        index = 6
        print(f'num_remaining_quantity_{index}_changed')
        self.cartridges[index].quantity = self.num_remaining_quantity_6.value()
        self.cartridges[index].quantity_temp = self.num_remaining_quantity_6.value()

    def num_remaining_quantity_7_changed(self):
        index = 7
        print(f'num_remaining_quantity_{index}_changed')
        self.cartridges[index].quantity = self.num_remaining_quantity_7.value()
        self.cartridges[index].quantity_temp = self.num_remaining_quantity_7.value()

    # События по изменениям флагам неисправности кассет
    def flag_broken_0_changed(self):
        index = 0
        self.cartridges[index].broken = self.flag_broken_0.isChecked()
        print(f"QCheckBox is checked: {self.cartridges[index].broken}")

    def flag_broken_1_changed(self):
        index = 1
        self.cartridges[index].broken = self.flag_broken_1.isChecked()
        print(f"QCheckBox is checked: {self.cartridges[index].broken}")

    def flag_broken_2_changed(self):
        index = 2
        self.cartridges[index].broken = self.flag_broken_2.isChecked()
        print(f"QCheckBox is checked: {self.cartridges[index].broken}")

    def flag_broken_3_changed(self):
        index = 3
        self.cartridges[index].broken = self.flag_broken_3.isChecked()
        print(f"QCheckBox is checked: {self.cartridges[index].broken}")

    def flag_broken_4_changed(self):
        index = 4
        self.cartridges[index].broken = self.flag_broken_4.isChecked()
        print(f"QCheckBox is checked: {self.cartridges[index].broken}")

    def flag_broken_5_changed(self):
        index = 5
        self.cartridges[index].broken = self.flag_broken_5.isChecked()
        print(f"QCheckBox is checked: {self.cartridges[index].broken}")

    def flag_broken_6_changed(self):
        index = 6
        self.cartridges[index].broken = self.flag_broken_6.isChecked()
        print(f"QCheckBox is checked: {self.cartridges[index].broken}")

    def flag_broken_7_changed(self):
        index = 7
        self.cartridges[index].broken = self.flag_broken_7.isChecked()
        print(f"QCheckBox is checked: {self.cartridges[index].broken}")

    # Расчёт результата
    @log_time(logger=logger, description='calc_result')
    def calc_result(self):
        start = time.time() * 1_000_000

        stop = False
        status = Status.FAULT

        while True:
            # Начинаем с самого крупного номинала
            current_banknote_type = self.banknote_types[self.start_banknote_type_index]

            # Проверяем есть ли купюры в кассетах данного типа
            for current_cartridge in self.cartridges_type_objs_dict[current_banknote_type]:

                # Если кассета исправна, то учитываем её в расчётах
                if not current_cartridge.broken:

                    # Находим остаток и расходуемое кол-во купюр
                    rest = self.num_money_temp % current_banknote_type
                    count = self.num_money_temp // current_banknote_type

                    # Если остатка нет и нам хватает купюр -> Перерасчёт и Выдача (Успех)
                    if rest == 0 and count <= current_cartridge.quantity_temp:
                        current_cartridge.quantity_temp -= count
                        self.num_money_temp -= count * current_banknote_type
                        current_cartridge.dynamic_temp = current_cartridge.quantity - current_cartridge.quantity_temp
                        status = Status.SUCCESS
                        print(status)
                        stop = True
                        break

                    # Если нам достаточно средств -> Делаем Перерасчёт
                    if count <= current_cartridge.quantity_temp:
                        current_cartridge.quantity_temp -= count
                        self.num_money_temp -= count * current_banknote_type
                        current_cartridge.dynamic_temp = current_cartridge.quantity - current_cartridge.quantity_temp

            if stop:
                break

            self.start_banknote_type_index -= 1

            # Если мы прошлись по всем кассетам, но не смогли набрать сумму -> Недостаточно средств
            if self.start_banknote_type_index == -(MAX_CARTRIDGES - 1):
                print(status)
                break

        # Если успешно, то заменяем основные на temp
        if status == Status.SUCCESS:
            for cartridge in self.cartridges:
                cartridge.quantity = cartridge.quantity_temp
                self.num_money.setValue(self.num_money_temp)
                cartridge.dynamic = cartridge.dynamic_temp

        # Если нет, то temp на основные
        if status == Status.FAULT:
            for cartridge in self.cartridges:
                cartridge.quantity_temp = cartridge.quantity
                self.num_money_temp = self.num_money.value()
                cartridge.dynamic_temp = cartridge.dynamic

        # Рассчитываем время исполнения
        end = time.time() * 1_000_000
        calc_time = end - start
        # calc_time = round(end - start, 10)

        # Заносим статус
        self.result_status = status
        self.calc_time = calc_time

        # Возвращаем требуемые расчётные переменные в дефолтное состояние
        self.start_banknote_type_index = -1

        # Обновляем фронт
        self.update_front()

    def randomise(self):
        print("randomise")

        # Очищаем старые данные
        for key in self.cartridges_type_objs_dict.keys():
            self.cartridges_type_objs_dict[key] = []
        self.cartridges.clear()

        # Заполняем новыми данными
        for i in range(self.num_cartridges.value()):
            banknote_type_index = CartridgeInfoGen.gen_banknote_type_index()
            banknote_type = self.banknote_types[banknote_type_index]
            quantity = CartridgeInfoGen.gen_quantity()

            cartridge = Cartridge(
                number=i,
                banknote_type=banknote_type,
                banknote_type_index=banknote_type_index,
                quantity=quantity,
                quantity_temp=quantity,
                broken=CartridgeInfoGen.gen_broken(),
                dynamic=0,
                dynamic_temp=0,
            )
            self.cartridges_type_objs_dict[banknote_type].append(cartridge)
            self.cartridges.append(cartridge)

    def update_front(self):
        print("update_front")

        # Обновляем статус результата расчёта и время
        self.label_result.setText(str(self.result_status))
        self.label_calc_time.setText(str(self.calc_time))
        self.label_mks.setText("microsecond")

        if self.num_cartridges.value() > 0:
            index = 0
            self.splitter.show()
            self.box_banknote_type_0.setCurrentIndex(self.cartridges[index].banknote_type_index)
            self.num_remaining_quantity_0.setValue(self.cartridges[index].quantity)
            self.label_dynamic_0.setText(str(self.cartridges[index].dynamic))
            self.flag_broken_0.setChecked(self.cartridges[index].broken)
        else:
            self.splitter.hide()

        if self.num_cartridges.value() > 1:
            index = 1
            self.splitter_1.show()
            self.box_banknote_type_1.setCurrentIndex(self.cartridges[index].banknote_type_index)
            self.num_remaining_quantity_1.setValue(self.cartridges[index].quantity)
            self.label_dynamic_1.setText(str(self.cartridges[index].dynamic))
            self.flag_broken_1.setChecked(self.cartridges[index].broken)
        else:
            self.splitter_1.hide()

        if self.num_cartridges.value() > 2:
            index = 2
            self.splitter_2.show()
            self.box_banknote_type_2.setCurrentIndex(self.cartridges[index].banknote_type_index)
            self.num_remaining_quantity_2.setValue(self.cartridges[index].quantity)
            self.label_dynamic_2.setText(str(self.cartridges[index].dynamic))
            self.flag_broken_2.setChecked(self.cartridges[index].broken)
        else:
            self.splitter_2.hide()

        if self.num_cartridges.value() > 2:
            index = 2
            self.splitter_2.show()
            self.box_banknote_type_2.setCurrentIndex(self.cartridges[index].banknote_type_index)
            self.num_remaining_quantity_2.setValue(self.cartridges[index].quantity)
            self.label_dynamic_2.setText(str(self.cartridges[index].dynamic))
            self.flag_broken_2.setChecked(self.cartridges[index].broken)
        else:
            self.splitter_2.hide()

        if self.num_cartridges.value() > 3:
            index = 3
            self.splitter_3.show()
            self.box_banknote_type_3.setCurrentIndex(self.cartridges[index].banknote_type_index)
            self.num_remaining_quantity_3.setValue(self.cartridges[index].quantity)
            self.label_dynamic_3.setText(str(self.cartridges[index].dynamic))
            self.flag_broken_3.setChecked(self.cartridges[index].broken)
        else:
            self.splitter_3.hide()

        if self.num_cartridges.value() > 4:
            index = 4
            self.splitter_4.show()
            self.box_banknote_type_4.setCurrentIndex(self.cartridges[index].banknote_type_index)
            self.num_remaining_quantity_4.setValue(self.cartridges[index].quantity)
            self.label_dynamic_4.setText(str(self.cartridges[index].dynamic))
            self.flag_broken_4.setChecked(self.cartridges[index].broken)
        else:
            self.splitter_4.hide()

        if self.num_cartridges.value() > 5:
            index = 5
            self.splitter_5.show()
            self.box_banknote_type_5.setCurrentIndex(self.cartridges[index].banknote_type_index)
            self.num_remaining_quantity_5.setValue(self.cartridges[index].quantity)
            self.label_dynamic_5.setText(str(self.cartridges[index].dynamic))
            self.flag_broken_5.setChecked(self.cartridges[index].broken)
        else:
            self.splitter_5.hide()

        if self.num_cartridges.value() > 6:
            index = 6
            self.splitter_6.show()
            self.box_banknote_type_6.setCurrentIndex(self.cartridges[index].banknote_type_index)
            self.num_remaining_quantity_6.setValue(self.cartridges[index].quantity)
            self.label_dynamic_6.setText(str(self.cartridges[index].dynamic))
            self.flag_broken_6.setChecked(self.cartridges[index].broken)
        else:
            self.splitter_6.hide()

        if self.num_cartridges.value() > 7:
            index = 7
            self.splitter_7.show()
            self.box_banknote_type_7.setCurrentIndex(self.cartridges[index].banknote_type_index)
            self.num_remaining_quantity_7.setValue(self.cartridges[index].quantity)
            self.label_dynamic_7.setText(str(self.cartridges[index].dynamic))
            self.flag_broken_7.setChecked(self.cartridges[index].broken)
        else:
            self.splitter_7.hide()

    def num_cartridges_changed(self):
        print("num_cartridges_changed")
        self.randomise()
        self.update_front()

    def btn_randomise_clicked(self):
        print("btn_randomise_clicked")
        self.randomise()
        self.update_front()

    def num_money_changed(self):
        print("num_money_changed")
        self.num_money_temp = self.num_money.value()

    # Наполняем фронт
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ATM"))
        self.btn_calc_result.setText(_translate("MainWindow", "Выдать"))
        self.btn_randomise.setText(_translate("MainWindow", "Рандомное заполнение"))

        # Результат
        self.label_result.setText(_translate("MainWindow", self.result_status))

        # Кассета_0
        self.label_n_0.setText(_translate("MainWindow", "1"))
        self.box_banknote_type_0.clear()
        for i, banknote_type in enumerate(self.banknote_types):
            self.box_banknote_type_0.addItem(_translate("MainWindow", str(banknote_type)))
        self.flag_broken_0.setText(_translate("MainWindow", "Несправна"))

        # Кассета_1
        self.label_n_1.setText(_translate("MainWindow", "2"))
        self.box_banknote_type_1.clear()
        for i, banknote_type in enumerate(self.banknote_types):
            self.box_banknote_type_1.addItem(_translate("MainWindow", str(banknote_type)))
        self.flag_broken_1.setText(_translate("MainWindow", "Несправна"))

        # Кассета_2
        self.label_n_2.setText(_translate("MainWindow", "3"))
        self.box_banknote_type_2.clear()
        for i, banknote_type in enumerate(self.banknote_types):
            self.box_banknote_type_2.addItem(_translate("MainWindow", str(banknote_type)))
        self.flag_broken_2.setText(_translate("MainWindow", "Несправна"))

        # Кассета_3
        self.label_n_3.setText(_translate("MainWindow", "4"))
        self.box_banknote_type_3.clear()
        for i, banknote_type in enumerate(self.banknote_types):
            self.box_banknote_type_3.addItem(_translate("MainWindow", str(banknote_type)))
        self.flag_broken_3.setText(_translate("MainWindow", "Несправна"))

        # Кассета_4
        self.label_n_4.setText(_translate("MainWindow", "5"))
        self.box_banknote_type_4.clear()
        for i, banknote_type in enumerate(self.banknote_types):
            self.box_banknote_type_4.addItem(_translate("MainWindow", str(banknote_type)))
        self.flag_broken_4.setText(_translate("MainWindow", "Несправна"))

        # Кассета_5
        self.label_n_5.setText(_translate("MainWindow", "6"))
        self.box_banknote_type_5.clear()
        for i, banknote_type in enumerate(self.banknote_types):
            self.box_banknote_type_5.addItem(_translate("MainWindow", str(banknote_type)))
        self.flag_broken_5.setText(_translate("MainWindow", "Несправна"))

        # Кассета_6
        self.label_n_6.setText(_translate("MainWindow", "7"))
        self.box_banknote_type_6.clear()
        for i, banknote_type in enumerate(self.banknote_types):
            self.box_banknote_type_6.addItem(_translate("MainWindow", str(banknote_type)))
        self.flag_broken_6.setText(_translate("MainWindow", "Несправна"))

        # Кассета_7
        self.label_n_7.setText(_translate("MainWindow", "8"))
        self.box_banknote_type_7.clear()
        for i, banknote_type in enumerate(self.banknote_types):
            self.box_banknote_type_7.addItem(_translate("MainWindow", str(banknote_type)))
        self.flag_broken_7.setText(_translate("MainWindow", "Несправна"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
