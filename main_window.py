# -*- coding: utf-8 -*-

import json
from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QCursor, QAction, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QMenu,
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTreeView,
    QWidget,
    QSplitter,
)

from ui_main import Ui_MainWindow
from theme_window import ThemeWindow
from feedback_window import FeedbackWindow
from about_window import AboutWindow
from message_window import MessageWindow

from cursor import CursorDirection
from language import Language
from icon import LogoIcon, MenuIcon
from style import LabelStyle, ButtonStyle, WidgetStyle, MenuStyle
from utils import FileUtils
from widget import WidgetManager


# main window
class MainWindow(QMainWindow):
    def __init__(self, p_theme, p_translator, p_setting):
        super(MainWindow, self).__init__()

        self.theme = p_theme
        self.translator = p_translator
        self.setting = p_setting

        self.cursor_direction = CursorDirection.Default
        self.left_btn_pressed = False
        self.drag_point = 0

        self.cn_menu = None
        self.en_menu = None

        self.wid_mng = WidgetManager()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init()

    # initialize the window
    def init(self):
        self.init_window()
        self.init_app_bar()
        self.init_more_menu()
        self.init_language()
        self.init_window_content()

    # initialize the window style
    def init_window(self):
        self.ui.wid_main.setStyleSheet(WidgetStyle.get_border("wid_main"))
        self.setWindowFlags(
            Qt.Window
            | Qt.FramelessWindowHint
            | Qt.WindowSystemMenuHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

    # initialize the window title bar(self-defined logo, title and min/restore/max icons)
    def init_app_bar(self):
        self.ui.lbl_logo.setMinimumSize(QSize(24, 24))
        self.ui.lbl_logo.setMaximumSize(QSize(24, 24))
        self.ui.lbl_logo.setPixmap(LogoIcon.get_pixmap())
        self.ui.lbl_logo.setScaledContents(True)

        self.ui.btn_max.setVisible(True)
        self.ui.btn_restore.setVisible(False)

        self.ui.btn_more.setFlat(True)
        self.ui.btn_min.setFlat(True)
        self.ui.btn_close.setFlat(True)
        self.ui.btn_max.setFlat(True)
        self.ui.btn_restore.setFlat(True)

        self.ui.btn_more.setIcon(MenuIcon.get_more())
        self.ui.btn_min.setIcon(MenuIcon.get_min())
        self.ui.btn_close.setIcon(MenuIcon.get_close())
        self.ui.btn_max.setIcon(MenuIcon.get_max())
        self.ui.btn_restore.setIcon(MenuIcon.get_restore())

        self.ui.btn_more.setIconSize(QSize(24, 24))
        self.ui.btn_min.setIconSize(QSize(24, 24))
        self.ui.btn_close.setIconSize(QSize(24, 24))
        self.ui.btn_max.setIconSize(QSize(24, 24))
        self.ui.btn_restore.setIconSize(QSize(24, 24))

        self.ui.btn_close.setStyleSheet(ButtonStyle.get_close())

        self.ui.btn_min.clicked.connect(self.on_min)
        self.ui.btn_close.clicked.connect(self.on_exit)
        self.ui.btn_max.clicked.connect(self.on_max)
        self.ui.btn_restore.clicked.connect(self.on_restore)

        self.ui.lbl_title.setStyleSheet(LabelStyle.get_title())

    # initialize the other menu(theme, language, feedback and about)
    def init_more_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet(MenuStyle.get_more())

        action = QAction(MainWindow.tr("menu_theme"), self)
        action.setIcon(MenuIcon.get_theme())
        action.triggered.connect(self.on_show_theme)
        menu.addAction(action)
        self.wid_mng.add(action, text="menu_theme")

        languageMenu = QMenu(MainWindow.tr("menu_language"))
        languageMenu.setIcon(MenuIcon.get_language())
        menu.addMenu(languageMenu)
        self.wid_mng.add(languageMenu, text="menu_language")

        action = QAction(MainWindow.tr("menu_chinese"), languageMenu)
        action.setCheckable(True)
        action.setChecked(True)
        action.triggered.connect(self.on_show_chinese)
        languageMenu.addAction(action)
        self.cn_menu = action
        self.wid_mng.add(action, text="menu_chinese")

        action = QAction(MainWindow.tr("menu_english"), languageMenu)
        action.setCheckable(True)
        action.setChecked(False)
        action.triggered.connect(self.on_show_english)
        languageMenu.addAction(action)
        self.en_menu = action
        self.wid_mng.add(action, text="menu_english")

        action = QAction(MainWindow.tr("menu_feedback"), self)
        action.setIcon(MenuIcon.get_feedback())
        action.triggered.connect(self.on_show_feedback)
        menu.addAction(action)
        self.wid_mng.add(action, text="menu_feedback")

        action = QAction(MainWindow.tr("menu_about"), self)
        action.setIcon(MenuIcon.get_about())
        action.triggered.connect(self.on_show_about)
        menu.addAction(action)
        self.wid_mng.add(action, text="menu_about")

        self.ui.btn_more.setMenu(menu)
        self.ui.btn_more.setStyleSheet(ButtonStyle.get_more())

    # initialize the default language
    def init_language(self):
        if self.setting.get_language() == Language.Chinese.value:
            self.cn_menu.setChecked(True)
            self.en_menu.setChecked(False)
        else:
            self.en_menu.setChecked(True)
            self.cn_menu.setChecked(False)

    def init_window_content(self):
        self.gridLayout = QGridLayout(self.ui.widget_body)
        self.horizontalLayoutTop = QHBoxLayout()
        self.lineEdit = QLineEdit(self.ui.widget_body)
        self.lineEdit.setMinimumSize(QSize(0, 32))
        self.lineEdit.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayoutTop.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.ui.widget_body)
        self.pushButton.setMinimumSize(QSize(0, 32))
        self.pushButton.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayoutTop.addWidget(self.pushButton)

        self.gridLayout.addLayout(self.horizontalLayoutTop, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.treeView = QTreeView(self.ui.widget_body)
        self.treeView.setMinimumSize(QSize(0, 500))

        self.horizontalLayout.addWidget(self.treeView)

        self.tabWidget = QTabWidget(self.ui.widget_body)
        self.tabWidget.setMinimumSize(QSize(0, 500))
        self.wid_json = QWidget()
        self.horizontalLayout111 = QHBoxLayout(self.wid_json)
        self.textEdit = QTextEdit(self.wid_json)
        self.textEdit.setMaximumSize(QSize(16777215, 16777215))
        self.textEdit.setAcceptRichText(False)

        self.horizontalLayout111.addWidget(self.textEdit)

        self.tabWidget.addTab(self.wid_json, "JSON")
        self.wid_table = QWidget()
        self.fieldLayout = QGridLayout(self.wid_table)
        self.tableWidget = QTableWidget(self.wid_table)

        self.fieldLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.tabWidget.addTab(self.wid_table, MainWindow.tr('title_table'))
        
        self.horizontalLayout.addWidget(self.tabWidget)

        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.ui.widget_body.setLayout(self.gridLayout)

        self.lineEdit.setMaxLength(100 * 1024 * 1024)
        self.lineEdit.setText("")
        self.pushButton.setText(MainWindow.tr('title_convert'))
        self.wid_mng.add(self.pushButton, text="title_convert")

        self.lineEdit.mouseDoubleClickEvent = self.on_input_double_click
        self.lineEdit.keyPressEvent = self.on_input_press
        self.pushButton.clicked.connect(self.on_convert)

        self.tableWidget.setMouseTracking(True)
        self.tableWidget.itemClicked.connect(self.on_item_clicked)
        self.tableWidget.itemSelectionChanged.connect(self.on_item_select_changed)

        self.select = QtGui.QAction(MainWindow.tr('menu_select_all'))
        self.select.triggered.connect(self.on_select_all)
        self.wid_mng.add(self.select, text="menu_select_all")
        
        self.copy = QtGui.QAction(MainWindow.tr('menu_copy'))
        self.copy.triggered.connect(self.on_copy)
        self.wid_mng.add(self.copy, text="menu_copy")

        self.textEdit.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.textEdit.addActions([self.select, self.copy])
        self.clipboard = QtGui.QGuiApplication.clipboard()

        self.tabWidget.currentChanged.connect(self.on_current_changed)

        self.column_name_list = [MainWindow.tr('title_json_tree')]
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.column_name_list)
        self.treeView.setModel(self.model)
        self.treeView.clicked.connect(self.on_treeview_clicked)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.treeView)
        self.splitter.addWidget(self.tabWidget)
        self.splitter.setSizes([10000, 10000])
        self.horizontalLayout.addWidget(self.splitter)

        self.tree_items_dict = {}
        self.json_data = None

    def init_tree(self, json_obj):
        # 判断是list还是dict
        # 再判断每个子元素是list还是dict
        # 子元素是list则展示key为下标，dict则展示其key值
        if isinstance(json_obj, list):
            text = MainWindow.tr('title_json_array') + " [" + str(len(json_obj)) + "]"
            item = QStandardItem(text)
            item.setEditable(False)
            self.model.setItem(0, 0, item)

            self.tree_items_dict[id(item)] = json_obj
            self.init_tree_list_node(item, 0, json_obj)
        elif isinstance(json_obj, dict):
            text = MainWindow.tr('title_json_object') + " {" + str(len(json_obj)) + "}"
            item = QStandardItem(text)
            item.setEditable(False)
            self.model.setItem(0, 0, item)

            self.tree_items_dict[id(item)] = json_obj
            self.init_tree_dict_node(item, 0, json_obj)

    def init_tree_list_node(self, parent, index, json_obj):
        row = 0
        for node in json_obj:
            if isinstance(node, list):
                text = str(index) + " [" + str(len(node)) + "]"
                item = QStandardItem(text)
                item.setEditable(False)
                parent.setChild(row, 0, item)

                row += 1
                index += 1

                self.tree_items_dict[id(item)] = node

                self.init_tree_list_node(item, index, node)
            elif isinstance(node, dict):
                text = str(index) + " {" + str(len(node)) + "}"
                item = QStandardItem(text)
                item.setEditable(False)
                parent.setChild(row, 0, item)

                row += 1
                index += 1

                self.tree_items_dict[id(item)] = node

                self.init_tree_dict_node(item, index, node)
            else:
                text = str(index)
                item = QStandardItem(text)
                item.setEditable(False)
                parent.setChild(row, 0, item)

                index += 1
                row += 1

    def init_tree_dict_node(self, parent, index, json_obj):
        row = 0
        for key, node in json_obj.items():
            if isinstance(node, list):
                text = key + " [" + str(len(node)) + "]"
                item = QStandardItem(text)
                item.setEditable(False)
                parent.setChild(row, 0, item)

                row += 1

                self.tree_items_dict[id(item)] = node

                self.init_tree_list_node(item, index, node)
            elif isinstance(node, dict):
                text = key + " {" + str(len(node)) + "}"
                item = QStandardItem(text)
                item.setEditable(False)
                parent.setChild(row, 0, item)

                row += 1
                index += 1

                self.tree_items_dict[id(item)] = node

                self.init_tree_dict_node(item, index, node)
            else:
                text = key + " : " + str(node)
                item = QStandardItem(text)
                item.setEditable(False)
                parent.setChild(row, 0, item)

                index += 1
                row += 1

    def reset_tree(self):
        self.tree_items_dict = {}
        self.model.setRowCount(0)

    def on_treeview_clicked(self, index):
        item = self.model.itemFromIndex(index)
        obj = self.tree_items_dict.get(id(item))
        self.init_table_result(obj)
        # print("on_treeview_clicked", item, item.text(), obj)

    def on_input_double_click(self, _):
        self.lineEdit.setText("")

    def on_input_press(self, event):
        if event.key() == Qt.Key.Key_Enter:
            self.on_convert()

        return QtWidgets.QLineEdit.keyPressEvent(self.lineEdit, event)

    def on_convert(self):
        text = self.lineEdit.text()
        if len(text) == 0:
            return

        valid = True
        self.json_data = None

        try:
            self.json_data = json.loads(text)
        except:
            valid = False
            pass

        if not valid:
            return QtWidgets.QMessageBox.information(self, MainWindow.tr('title_tip'), MainWindow.tr('tip_invalid_json'))

        self.reset_tree()
        self.init_tree(self.json_data)

        index = self.tabWidget.currentIndex()
        if index == 0:
            self.init_json_result(self.json_data)
            self.textEdit.setFocus()
        elif index == 1:
            self.init_table_result(self.json_data)

    def on_select_all(self):
        self.textEdit.selectAll()

    def on_copy(self):
        text = self.textEdit.toPlainText()
        self.clipboard.setText(text)

    def on_key_press(self, event: QtGui.QKeyEvent):
        ctrl_pressed = event.modifiers() & Qt.ControlModifier
        if ctrl_pressed and (event.key() == Qt.Key.Key_A):
            self.on_select_all()
        elif ctrl_pressed and (event.key() == Qt.Key.Key_C):
            self.on_copy()

    def on_current_changed(self):
        index = self.tabWidget.currentIndex()
        if index == 0:
            self.init_json_result(self.json_data)
            self.textEdit.setFocus()
        elif index == 1:
            self.init_table_result(self.json_data)
            self.tableWidget.setFocus()

    def on_item_clicked(self, item):
        print(item, item.row(), item.column(), item.text())

    def on_item_select_changed(self):
        selected_items = self.tableWidget.selectedItems()
        col_count = self.tableWidget.columnCount()

        msg = ""
        count = 0

        for item in selected_items:
            count += 1
            msg += item.text()
            if count >= col_count:
                msg += "\n"
            else:
                msg += " "

        self.clipboard.setText(msg)

    def init_json_result(self, json_data):
        if not json_data:
            return
        
        text = json.dumps(
            json_data, ensure_ascii=False, indent=4, separators=(",", ": ")
        )
        self.textEdit.setText(text)

    # 单条数据
    def add_one_dict_result(self, dict_data):
        if not isinstance(dict_data, dict):
            return

        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(len(dict_data.keys()))
        self.tableWidget.setHorizontalHeaderLabels(dict_data.keys())

        column = 0
        for _, value in dict_data.items():
            item = QtWidgets.QTableWidgetItem(str(value))
            item.setFlags(item.flags and (~Qt.ItemFlag.ItemIsEditable))
            self.tableWidget.setItem(0, column, item)
            column += 1

    # 多条数据
    def add_one_list_result(self, list_data):
        if not isinstance(list_data, list):
            return

        first_record = list_data[0]
        if len(first_record) == 0:
            return
            
        if not isinstance(first_record, dict):
            return

        self.tableWidget.setRowCount(len(list_data))
        self.tableWidget.setColumnCount(len(first_record.keys()))
        self.tableWidget.setHorizontalHeaderLabels(first_record.keys())

        row = 0
        for record in list_data:
            column = 0
            for _, value in record.items():
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(item.flags and (~Qt.ItemFlag.ItemIsEditable))
                self.tableWidget.setItem(row, column, item)
                column += 1
            row += 1

    def init_table_result(self, json_data):
        if not self.json_data:
            return

        # 如果是list则默认为是多条记录
        # 如果是dict，则遍历子项，如果有list则找第一个；否则认为是单条记录
        if isinstance(json_data, dict):
            multi_record = False
            for key, value in json_data.items():
                if isinstance(value, list):
                    multi_record = True
                    self.add_one_list_result(value)
                    break

            if not multi_record:
                self.add_one_dict_result(json_data)

        elif isinstance(json_data, list):
            self.add_one_list_result(json_data)

    # minimize the window
    def on_min(self):
        self.showMinimized()

    # maximize the window
    def on_max(self):
        self.ui.btn_max.setVisible(False)
        self.ui.btn_restore.setVisible(True)
        self.showMaximized()

    # restore the window
    def on_restore(self):
        self.ui.btn_max.setVisible(True)
        self.ui.btn_restore.setVisible(False)
        self.showNormal()

    # exit the application
    def on_exit(self):
        # confirm before exit
        dlg = MessageWindow(
            self,
            self.theme,
            MainWindow.tr("title_exit"),
            MainWindow.tr("tip_exit_message"),
        )
        result = dlg.exec()
        if result != QDialog.DialogCode.Accepted:
            return

        one = QApplication.instance()
        one.quit()

    # update widgets that created dynamically
    # call this function when changing language
    def update_dynamic_widgets(self):
        dynamic_widgets = self.wid_mng.get_all()
        for widget, text in dynamic_widgets.items():
            if isinstance(widget, QMenu):
                widget.setTitle(MainWindow.tr(text))
            else:
                widget.setText(MainWindow.tr(text))
                
        self.tabWidget.setTabText(1, MainWindow.tr('title_table'))
        self.column_name_list = [MainWindow.tr('title_json_tree')]
        self.model.setHorizontalHeaderLabels(self.column_name_list)

    # show theme window
    def on_show_theme(self):
        dlg = ThemeWindow(self, self.theme)
        dlg.theme_signal.connect(self.proc_theme_signal)
        dlg.show()

    # response when changing Chinese language
    def on_show_chinese(self):
        cn_checked = self.cn_menu.isChecked()
        en_checked = not cn_checked

        self.cn_menu.setChecked(cn_checked)
        self.en_menu.setChecked(en_checked)

        if cn_checked:
            self.translator.load("zh_CN")
            self.setting.save(Language.Chinese.value, self.theme.get_theme_name())
        else:
            self.translator.load("en_US")
            self.setting.save(Language.English.value, self.theme.get_theme_name())

        self.ui.retranslateUi(self)
        self.update_dynamic_widgets()

    # response when changing English language
    def on_show_english(self):
        en_checked = self.en_menu.isChecked()
        cn_checked = not en_checked

        self.en_menu.setChecked(en_checked)
        self.cn_menu.setChecked(cn_checked)

        if en_checked:
            self.translator.load("en_US")
            self.setting.save(Language.English.value, self.theme.get_theme_name())
        else:
            self.translator.load("zh_CN")
            self.setting.save(Language.Chinese.value, self.theme.get_theme_name())

        self.ui.retranslateUi(self)
        # update the widgets that created dynamically when changing language
        self.update_dynamic_widgets()

    # show feedback window
    def on_show_feedback(self):
        dlg = FeedbackWindow(self, self.theme)
        dlg.show()

    # show about window
    def on_show_about(self):
        dlg = AboutWindow(self, self.theme)
        dlg.show()

    # process the signal of changing theme
    def proc_theme_signal(self, content):
        language = (
            Language.Chinese
            if self.cn_menu and self.cn_menu.isChecked()
            else Language.English
        )
        self.setting.save(language.value, FileUtils.get_name(content))

    # get the cursor direction when dragging the mouse
    def get_cursor_direction(self, global_point):
        padding = 1

        rect = self.rect()
        top_left = self.mapToGlobal(rect.topLeft())
        bottom_right = self.mapToGlobal(rect.bottomRight())

        x = global_point.x()
        y = global_point.y()

        if (
            top_left.x() + padding >= x >= top_left.x()
            and top_left.y() + padding >= y >= top_left.y()
        ):
            self.cursor_direction = CursorDirection.LeftTop
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif (
            bottom_right.x() - padding <= x <= bottom_right.x()
            and bottom_right.y() - padding <= y <= bottom_right.y()
        ):
            self.cursor_direction = CursorDirection.RightBottom
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif (
            top_left.x() + padding >= x >= top_left.x()
            and bottom_right.y() - padding <= y <= bottom_right.y()
        ):
            self.cursor_direction = CursorDirection.LeftBottom
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif (
            bottom_right.x() >= x >= bottom_right.x() - padding
            and top_left.y() <= y <= top_left.y() + padding
        ):
            self.cursor_direction = CursorDirection.RightTop
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif top_left.x() + padding >= x >= top_left.x():
            self.cursor_direction = CursorDirection.Left
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif bottom_right.x() >= x >= bottom_right.x() - padding:
            self.cursor_direction = CursorDirection.Right
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif top_left.y() <= y <= top_left.y() + padding:
            self.cursor_direction = CursorDirection.Up
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif bottom_right.y() >= y >= bottom_right.y() - padding:
            self.cursor_direction = CursorDirection.Down
            self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            self.cursor_direction = CursorDirection.Default
            self.setCursor(QCursor(Qt.ArrowCursor))

    # process mouse event when dragging the window
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_btn_pressed = True

            if self.cursor_direction != CursorDirection.Default:
                self.mouseGrabber()
            else:
                self.drag_point = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        global_point = e.globalPos()
        rect = self.rect()
        top_left = self.mapToGlobal(rect.topLeft())
        bottom_right = self.mapToGlobal(rect.bottomRight())

        if not self.left_btn_pressed:
            self.get_cursor_direction(global_point)
        else:
            if self.cursor_direction != CursorDirection.Default:
                move_rect = QRect(top_left, bottom_right)

                if self.cursor_direction == CursorDirection.Left:
                    if bottom_right.x() - global_point.x() <= self.minimumWidth():
                        move_rect.setX(top_left.x())
                    else:
                        move_rect.setX(global_point.x())
                elif self.cursor_direction == CursorDirection.Right:
                    move_rect.setWidth(global_point.x() - top_left.x())
                elif self.cursor_direction == CursorDirection.Up:
                    if bottom_right.y() - global_point.y() <= self.minimumHeight():
                        move_rect.setY(top_left.y())
                    else:
                        move_rect.setY(global_point.y())
                elif self.cursor_direction == CursorDirection.Down:
                    move_rect.setHeight(global_point.y() - top_left.y())
                elif self.cursor_direction == CursorDirection.LeftTop:
                    if bottom_right.x() - global_point.x() <= self.minimumWidth():
                        move_rect.setX(top_left.x())
                    else:
                        move_rect.setX(global_point.x())

                    if bottom_right.y() - global_point.y() <= self.minimumHeight():
                        move_rect.setY(top_left.y())
                    else:
                        move_rect.setY(global_point.y())
                elif self.cursor_direction == CursorDirection.RightTop:
                    move_rect.setWidth(global_point.x() - top_left.x())
                    move_rect.setY(global_point.y())
                elif self.cursor_direction == CursorDirection.LeftBottom:
                    move_rect.setX(global_point.x())
                    move_rect.setHeight(global_point.y() - top_left.y())
                elif self.cursor_direction == CursorDirection.RightBottom:
                    move_rect.setWidth(global_point.x() - top_left.x())
                    move_rect.setHeight(global_point.y() - top_left.y())
                else:
                    pass

                self.setGeometry(move_rect)
            else:
                self.move(e.globalPos() - self.drag_point)
                e.accept()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_btn_pressed = False

            if self.cursor_direction != CursorDirection.Default:
                self.releaseMouse()
                self.setCursor(QCursor(Qt.ArrowCursor))
