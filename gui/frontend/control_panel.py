# control_panel.py

from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit

def create_control_panel(main_window):
    control_layout = QHBoxLayout()

    main_window.browse_button = QPushButton("Browse for Memory Dump", main_window)
    main_window.browse_button.clicked.connect(main_window.browse_memory_dump)
    control_layout.addWidget(main_window.browse_button)

    main_window.selected_file_label = QLabel("", main_window)
    control_layout.addWidget(main_window.selected_file_label)

    main_window.plugin_label = QLabel("Select Volatility Plugin:", main_window)
    control_layout.addWidget(main_window.plugin_label)

    main_window.plugin_combo = QComboBox(main_window)
    main_window.plugin_combo.currentIndexChanged.connect(main_window.update_scan_button_state)
    control_layout.addWidget(main_window.plugin_combo)

    main_window.scan_button = QPushButton("Scan", main_window)
    main_window.scan_button.setEnabled(False)
    main_window.scan_button.clicked.connect(main_window.scan_memory_dump)
    control_layout.addWidget(main_window.scan_button)

    main_window.theme_dropdown = QComboBox(main_window)
    main_window.theme_dropdown.addItems(["Light", "Dark", "Hacker", "Colorblind", "Midnight", "Summer Day", "LSD Trip", "Mnemonic"])
    main_window.theme_dropdown.currentIndexChanged.connect(main_window.change_theme)
    control_layout.addWidget(main_window.theme_dropdown)

    main_window.terminal_toggle_button = QPushButton("Toggle Terminal", main_window)
    main_window.terminal_toggle_button.clicked.connect(main_window.toggle_terminal)
    control_layout.addWidget(main_window.terminal_toggle_button)

    main_window.clear_terminal_button = QPushButton("Clear Terminal", main_window)
    main_window.clear_terminal_button.clicked.connect(main_window.clear_terminal)
    control_layout.addWidget(main_window.clear_terminal_button)

    return control_layout

def create_filter_input(main_window):
    filter_input = QLineEdit(main_window)
    filter_input.setPlaceholderText("Filter results")
    filter_input.textChanged.connect(main_window.filter_results)
    return filter_input
