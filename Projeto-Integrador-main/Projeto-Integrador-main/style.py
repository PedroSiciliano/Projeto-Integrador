# perfect_acqua_system/style.py
STYLESHEET = """
    /* --- FUNDO E FONTES --- */
    QWidget, QDialog {
        font-family: "Segoe UI", sans-serif;
        font-size: 14px;
        color: #e2e8f0;
    }
    QMainWindow, QDialog {
        background-color: #0f172a;
    }

    /* --- PAINÉIS COM SOMBRA --- */
    #Sidebar, #ContentFrame, #LoginFrame, .CardFrame {
        background-color: #1e293b;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    
    /* --- TÍTULOS E TEXTOS --- */
    QLabel#Title { font-size: 24px; font-weight: 600; color: #ffffff; }
    QLabel#Subtitle { color: #94a3b8; font-size: 15px; }
    QLabel#ErrorMessage { color: #f87171; font-weight: 600; }
    .SectionHeader {
        color: #ffffff; 
        background-color: #334155;
        padding: 8px; 
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
    }

    /* --- SIDEBAR --- */
    #SidebarTitle { font-size: 20px; font-weight: 600; color: #ffffff; margin-bottom: 15px; padding-left: 10px; }
    #SidebarMenu { border: none; background-color: transparent; }
    #SidebarMenu::item { padding: 14px; border-radius: 8px; font-weight: 500; font-size: 15px; }
    #SidebarMenu::item:hover { background-color: #334155; }
    #SidebarMenu::item:selected { background-color: #535bf2; color: white; font-weight: bold; }
    
    /* --- TABELAS --- */
    QTableWidget { 
        background-color: #1e293b; border-radius: 10px; border: 1px solid #334155;
        font-size: 14px; color: #e2e8f0; gridline-color: #334155;
        alternate-background-color: #2b3a4a;
    }
    QHeaderView::section {
        background-color: #334155; color: #ffffff; padding: 12px;
        border: none; font-weight: 600;
    }
    QTableWidget::item { padding: 10px; border: none; } 
    QTableWidget::item:selected { background-color: #535bf2; color: white; }
    
    /* --- FORMULÁRIOS E FILTROS --- */
    QLineEdit, QComboBox, QDateEdit, QTextEdit, QTimeEdit, QDoubleSpinBox {
        border: 1px solid #334155; border-radius: 8px; padding: 10px;
        background-color: #0f172a; color: #e2e8f0;
        min-height: 20px;
    }
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus, QTimeEdit:focus, QDoubleSpinBox:focus {
        border-color: #535bf2;
    }
    QComboBox::drop-down { border: none; }
    QComboBox QAbstractItemView { background-color: #334155; selection-background-color: #535bf2; }
    
    /* --- BOTÕES --- */
    QPushButton {
        border: none; border-radius: 8px; padding: 10px 14px; font-weight: 600;
        min-height: 20px;
    }
    QPushButton[class="primary"] { background-color: #535bf2; color: #fff; }
    QPushButton[class="primary"]:hover { background-color: #4338ca; }
    QPushButton[class="success"] { background-color: #22c55e; color: #fff; }
    QPushButton[class="success"]:hover { background-color: #16a34a; }
    QPushButton[class="secondary"] { background-color: #475569; color: #fff; }
    QPushButton[class="secondary"]:hover { background-color: #52627a; }
    
    /* --- WIDGETS ESPECÍFICOS --- */
    QListWidget {
        background-color: #1e293b; border: 1px solid #334155; border-radius: 8px;
    }
    QListWidget::item:hover { background-color: #334155; }
    QListWidget::item:selected { background-color: #535bf2; color: #ffffff; }

    QProgressBar {
        border: none; background-color: #334155; height: 8px;
        border-radius: 4px; text-align: center;
    }
    QProgressBar::chunk { border-radius: 4px; }
"""