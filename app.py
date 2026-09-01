import sys
import csv
import numpy as np
from scipy import signal as sp_signal
from scipy.stats import kurtosis

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QDoubleSpinBox, QComboBox, QGroupBox,
    QFrame, QSplitter, QScrollArea, QPushButton, QFileDialog, QMessageBox, QSpinBox
)
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# -------------------------------------------------------------------------
# UI Styling (Dark Industrial Diagnostic Theme)
# -------------------------------------------------------------------------
DARK_STYLE = """
QMainWindow {
    background-color: #090D11;
}
QWidget {
    color: #C9D1D9;
    font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 11px;
}
QGroupBox {
    border: 1px solid #1F2937;
    border-radius: 6px;
    margin-top: 10px;
    font-weight: bold;
    color: #38BDF8;
    background-color: #111827;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    background-color: #111827;
    border-radius: 3px;
}
QLabel {
    color: #9CA3AF;
}
QDoubleSpinBox, QSpinBox, QComboBox {
    background-color: #090D11;
    border: 1px solid #374151;
    border-radius: 4px;
    padding: 4px 6px;
    color: #38BDF8;
    font-weight: bold;
}
QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #38BDF8;
}
QPushButton {
    background-color: #1F2937;
    color: #38BDF8;
    border: 1px solid #374151;
    border-radius: 4px;
    padding: 6px 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #374151;
    border-color: #38BDF8;
}
QPushButton:pressed {
    background-color: #0284C7;
    color: #FFFFFF;
}
QFrame#metricCard {
    background-color: #090D11;
    border: 1px solid #1F2937;
    border-radius: 6px;
}
"""

CLASSES = ["Healthy machine", "Bearing defect", "Gear defect", "Misalignment", "Cavitation"]
FEATURE_NAMES = [
    "RMS", "Peak Amplitude", "Crest Factor", "Kurtosis",
    "Spectral Centroid", "Spectral Bandwidth", "Dominant Freq", "Spectral Energy"
]


class MachineFaultAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Machine Sound Fault Analyzer (Acoustic Condition Monitoring)")
        self.resize(1500, 940)
        self.setMinimumSize(1024, 720)

        self.fs = 8000  # Sampling Frequency
        self.duration = 1.0  # Sample duration in seconds
        
        # Dataset storage
        self.X_data = []
        self.y_data = []
        self.clf = None
        self.cm = None
        self.feature_importances = None

        # Current test sample data
        self.current_signal = None
        self.current_label = None
        self.current_pred = None
        self.current_probs = None

        self.init_ui()
        self.generate_dataset()
        self.train_model()
        self.generate_test_signal()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # -----------------------------------------------------------------
        # LEFT PANEL: Dataset Controls & Testing Interface
        # -----------------------------------------------------------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        ctrl_layout = QVBoxLayout(scroll_content)

        # 1. Dataset Generation Controls
        group_ds = QGroupBox("1. DATASET SYNTHESIS CONFIG")
        grid_ds = QGridLayout(group_ds)
        grid_ds.setSpacing(6)

        grid_ds.addWidget(QLabel("Samples per Class:"), 0, 0)
        self.spin_samples = QSpinBox()
        self.spin_samples.setRange(100, 500)
        self.spin_samples.setValue(100)
        self.spin_samples.setSingleStep(50)
        grid_ds.addWidget(self.spin_samples, 0, 1)

        grid_ds.addWidget(QLabel("Noise Level:"), 1, 0)
        self.spin_noise = QDoubleSpinBox()
        self.spin_noise.setRange(0.01, 0.5)
        self.spin_noise.setValue(0.05)
        self.spin_noise.setSingleStep(0.01)
        grid_ds.addWidget(self.spin_noise, 1, 1)

        btn_gen_ds = QPushButton("Generate Dataset")
        btn_gen_ds.clicked.connect(self.on_generate_dataset_clicked)
        grid_ds.addWidget(btn_gen_ds, 2, 0, 1, 2)

        ctrl_layout.addWidget(group_ds)

        # 2. Machine Learning Training
        group_ml = QGroupBox("2. MODEL TRAINING (RANDOM FOREST)")
        vbox_ml = QVBoxLayout(group_ml)

        btn_train = QPushButton("Train Random Forest Model")
        btn_train.clicked.connect(self.train_model)
        vbox_ml.addWidget(btn_train)

        btn_export = QPushButton("Export Features to CSV")
        btn_export.clicked.connect(self.export_csv)
        vbox_ml.addWidget(btn_export)

        ctrl_layout.addWidget(group_ml)

        # 3. Test Signal Generation & Real-Time Diagnosis
        group_test = QGroupBox("3. REAL-TIME DIAGNOSIS & TEST SIGNAL")
        grid_test = QGridLayout(group_test)
        grid_test.setSpacing(6)

        grid_test.addWidget(QLabel("Select Machine Class:"), 0, 0)
        self.combo_test_class = QComboBox()
        self.combo_test_class.addItems(CLASSES)
        grid_test.addWidget(self.combo_test_class, 0, 1)

        btn_gen_test = QPushButton("Generate Test Signal")
        btn_gen_test.clicked.connect(self.generate_test_signal)
        grid_test.addWidget(btn_gen_test, 1, 0, 1, 2)

        ctrl_layout.addWidget(group_test)
        ctrl_layout.addStretch()

        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)

        # -----------------------------------------------------------------
        # RIGHT PANEL: Readout Cards & Visual Diagnostic Displays
        # -----------------------------------------------------------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Real-time Prediction Metric Cards
        metrics_group = QGroupBox("ACOUSTIC FAULT DIAGNOSIS READOUTS")
        grid_metrics = QGridLayout(metrics_group)
        grid_metrics.setSpacing(6)

        self.lbl_true_class = self.create_metric_card("True Input Class", "--", grid_metrics, 0, 0)
        self.lbl_pred_class = self.create_metric_card("Predicted Fault Class", "--", grid_metrics, 0, 1)
        self.lbl_confidence = self.create_metric_card("Prediction Confidence", "0.0 %", grid_metrics, 0, 2)
        self.lbl_rms = self.create_metric_card("Signal RMS Level", "0.00 V", grid_metrics, 1, 0)
        self.lbl_crest = self.create_metric_card("Crest Factor", "0.00", grid_metrics, 1, 1)
        self.lbl_dom_freq = self.create_metric_card("Dominant Peak Freq", "0.0 Hz", grid_metrics, 1, 2)

        right_layout.addWidget(metrics_group)

        # Visual Grid Subplots
        plots_group = QGroupBox("DIAGNOSTIC VISUALIZATIONS & ML METRICS")
        layout_plots = QVBoxLayout(plots_group)

        self.fig = Figure(figsize=(9, 7), facecolor='#05080A')
        self.canvas = FigureCanvas(self.fig)
        layout_plots.addWidget(self.canvas)

        right_layout.addWidget(plots_group, stretch=1)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([360, 1140])

    def create_metric_card(self, title, default_val, layout, row, col):
        card = QFrame()
        card.setObjectName("metricCard")
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(6, 4, 6, 4)

        lbl_title = QLabel(title.upper())
        lbl_title.setStyleSheet("color: #9CA3AF; font-size: 10px; font-weight: bold;")
        lbl_val = QLabel(default_val)
        lbl_val.setStyleSheet("color: #38BDF8; font-size: 12px; font-weight: bold;")

        vbox.addWidget(lbl_title)
        vbox.addWidget(lbl_val)
        layout.addWidget(card, row, col)
        return lbl_val

    # -------------------------------------------------------------------------
    # Physically Inspired Acoustic Signal Generation & Feature Extraction
    # -------------------------------------------------------------------------
    def generate_acoustic_sample(self, class_idx, noise_level):
        t = np.linspace(0, self.duration, int(self.fs * self.duration), endpoint=False)
        f_rot = 30.0  # Fundamental shaft rotational speed (30 Hz = 1800 RPM)
        sig = np.zeros_like(t)

        if class_idx == 0:  # Healthy Machine
            # Baseline rotational frequency + faint 2nd & 3rd harmonics + low noise
            sig = 0.5 * np.sin(2 * np.pi * f_rot * t) + \
                  0.15 * np.sin(2 * np.pi * 2 * f_rot * t) + \
                  0.05 * np.sin(2 * np.pi * 3 * f_rot * t)

        elif class_idx == 1:  # Bearing Defect
            # High-frequency structural resonance excited by periodic sharp impacts (BPFI/BPFO)
            sig = 0.4 * np.sin(2 * np.pi * f_rot * t)
            f_impact = 140.0  # Impact repetition rate (Hz)
            f_res = 2200.0    # Bearing ring structural resonance (Hz)
            impulses = sp_signal.square(2 * np.pi * f_impact * t, duty=0.03)
            impulses = np.clip(impulses, 0, 1)
            # Transient decay envelope
            decay = np.exp(-1500.0 * (t % (1.0 / f_impact)))
            sig += 1.2 * impulses * decay * np.sin(2 * np.pi * f_res * t)

        elif class_idx == 2:  # Gear Defect
            # Gear Mesh Frequency (GMF = f_rot * teeth) with sidebands caused by local tooth damage
            teeth = 25
            f_gmf = f_rot * teeth  # 750 Hz
            sideband_mod = (1.0 + 0.8 * np.sin(2 * np.pi * f_rot * t))
            sig = 0.3 * np.sin(2 * np.pi * f_rot * t) + \
                  0.9 * sideband_mod * np.sin(2 * np.pi * f_gmf * t)

        elif class_idx == 3:  # Misalignment
            # Strong 2x and 3x shaft rotational harmonics dominating the spectrum
            sig = 0.4 * np.sin(2 * np.pi * f_rot * t) + \
                  1.1 * np.sin(2 * np.pi * 2 * f_rot * t) + \
                  0.7 * np.sin(2 * np.pi * 3 * f_rot * t)

        elif class_idx == 4:  # Cavitation
            # High-amplitude broadband fluid turbulence and random bubble implosion bursts
            np.random.seed()
            broadband_noise = np.random.normal(0, 0.8, len(t))
            # High-pass filter fluid noise
            b, a = sp_signal.butter(4, 1200.0 / (self.fs / 2.0), btype='high')
            cavitation_noise = sp_signal.filtfilt(b, a, broadband_noise)
            sig = 0.2 * np.sin(2 * np.pi * f_rot * t) + cavitation_noise

        # Add background Gaussian acoustic noise
        np.random.seed()
        sig += np.random.normal(0, noise_level, len(t))
        return sig

    def extract_features(self, sig):
        # 1. RMS
        rms_val = np.sqrt(np.mean(sig ** 2))

        # 2. Peak Amplitude
        peak_val = np.max(np.abs(sig))

        # 3. Crest Factor
        crest_factor = peak_val / (rms_val + 1e-12)

        # 4. Kurtosis
        kurt_val = kurtosis(sig)

        # Spectral Domain Features (FFT)
        N = len(sig)
        fft_vals = np.abs(np.fft.rfft(sig))
        fft_freqs = np.fft.rfftfreq(N, 1.0 / self.fs)

        # Power Spectrum
        psd = fft_vals ** 2
        sum_psd = np.sum(psd) + 1e-12

        # 5. Spectral Centroid
        centroid = np.sum(fft_freqs * psd) / sum_psd

        # 6. Spectral Bandwidth
        bandwidth = np.sqrt(np.sum(((fft_freqs - centroid) ** 2) * psd) / sum_psd)

        # 7. Dominant Frequency
        dom_freq = fft_freqs[np.argmax(fft_vals)]

        # 8. Spectral Energy
        spectral_energy = np.sum(psd)

        return [rms_val, peak_val, crest_factor, kurt_val, centroid, bandwidth, dom_freq, spectral_energy]

    # -------------------------------------------------------------------------
    # Dataset Synthesis & Machine Learning Training Pipeline
    # -------------------------------------------------------------------------
    def generate_dataset(self):
        n_samples = self.spin_samples.value()
        noise = self.spin_noise.value()

        self.X_data = []
        self.y_data = []

        for class_idx in range(len(CLASSES)):
            for _ in range(n_samples):
                sig = self.generate_acoustic_sample(class_idx, noise)
                feats = self.extract_features(sig)
                self.X_data.append(feats)
                self.y_data.append(class_idx)

        self.X_data = np.array(self.X_data)
        self.y_data = np.array(self.y_data)

    def on_generate_dataset_clicked(self):
        self.generate_dataset()
        self.train_model()
        QMessageBox.information(self, "Dataset Generated", f"Generated {len(self.X_data)} total synthetic samples ({self.spin_samples.value()} per class). Model retrained.")

    def train_model(self):
        if len(self.X_data) == 0:
            return

        X_train, X_test, y_train, y_test = train_test_split(
            self.X_data, self.y_data, test_size=0.25, random_state=42, stratify=self.y_data
        )

        self.clf = RandomForestClassifier(n_estimators=100, random_state=42)
        self.clf.fit(X_train, y_train)

        y_pred = self.clf.predict(X_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.feature_importances = self.clf.feature_importances_

        if self.current_signal is not None:
            self.predict_test_signal()

    def generate_test_signal(self):
        target_class_idx = self.combo_test_class.currentIndex()
        noise = self.spin_noise.value()
        self.current_signal = self.generate_acoustic_sample(target_class_idx, noise)
        self.current_label = target_class_idx
        self.predict_test_signal()

    def predict_test_signal(self):
        if self.clf is None or self.current_signal is None:
            return

        feats = np.array(self.extract_features(self.current_signal)).reshape(1, -1)
        self.current_pred = self.clf.predict(feats)[0]
        self.current_probs = self.clf.predict_proba(feats)[0]

        # Update Readouts
        true_str = CLASSES[self.current_label]
        pred_str = CLASSES[self.current_pred]
        conf_pct = self.current_probs[self.current_pred] * 100.0

        self.lbl_true_class.setText(true_str)
        self.lbl_pred_class.setText(pred_str)
        self.lbl_confidence.setText(f"{conf_pct:.1f} %")

        # Color-code prediction label card
        if self.current_pred == self.current_label:
            self.lbl_pred_class.setStyleSheet("color: #00FF66; font-size: 12px; font-weight: bold;")
        else:
            self.lbl_pred_class.setStyleSheet("color: #EF4444; font-size: 12px; font-weight: bold;")

        self.lbl_rms.setText(f"{feats[0][0]:.3f} V")
        self.lbl_crest.setText(f"{feats[0][2]:.2f}")
        self.lbl_dom_freq.setText(f"{feats[0][6]:.1f} Hz")

        self.plot_all_visuals()

    def export_csv(self):
        if len(self.X_data) == 0:
            QMessageBox.warning(self, "Export Error", "No feature dataset available to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Export Synthetic Features CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(FEATURE_NAMES + ["Class_Index", "Class_Name"])
                    for feats, label in zip(self.X_data, self.y_data):
                        writer.writerow(list(feats) + [label, CLASSES[label]])

                QMessageBox.information(self, "Export Success", f"Feature dataset successfully saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"An error occurred while saving file:\n{str(e)}")

    # -------------------------------------------------------------------------
    # Matplotlib Grid Visualizations
    # -------------------------------------------------------------------------
    def plot_all_visuals(self):
        self.fig.clear()

        bg_color = '#05080A'
        grid_color = '#13231B'
        cyan_color = '#38BDF8'
        green_color = '#00FF66'
        yellow_color = '#FFCC00'

        # 2x3 Grid Layout
        # Top-Left: Time Waveform | Top-Mid: FFT Spectrum | Top-Right: Prediction Probabilities
        # Bottom-Left: Confusion Matrix | Bottom-Mid/Right: Feature Importances
        gs = self.fig.add_gridspec(2, 3, width_ratios=[1, 1, 1])

        ax_wave = self.fig.add_subplot(gs[0, 0])
        ax_fft = self.fig.add_subplot(gs[0, 1])
        ax_prob = self.fig.add_subplot(gs[0, 2])
        ax_cm = self.fig.add_subplot(gs[1, 0])
        ax_imp = self.fig.add_subplot(gs[1, 1:])

        for ax in [ax_wave, ax_fft, ax_prob, ax_cm, ax_imp]:
            ax.set_facecolor(bg_color)
            ax.tick_params(colors='#9CA3AF', labelsize=7)
            for spine in ax.spines.values():
                spine.set_color('#1F2937')

        t = np.linspace(0, self.duration, int(self.fs * self.duration), endpoint=False)

        # 1. TIME WAVEFORM
        ax_wave.plot(t, self.current_signal, color=cyan_color, linewidth=0.8)
        ax_wave.set_title(f"TIME WAVEFORM ({CLASSES[self.current_label].upper()})", color=cyan_color, fontsize=7, fontweight='bold', loc='left')
        ax_wave.set_xlabel("Time (s)", color='#9CA3AF', fontsize=6)
        ax_wave.set_ylabel("Amp (V)", color='#9CA3AF', fontsize=6)
        ax_wave.grid(True, linestyle=':', linewidth=0.5, color=grid_color)
        ax_wave.set_xlim(0, 0.2)  # Zoom in on first 200 ms for fine structure

        # 2. FFT FREQUENCY SPECTRUM
        N = len(self.current_signal)
        fft_vals = np.abs(np.fft.rfft(self.current_signal))
        fft_freqs = np.fft.rfftfreq(N, 1.0 / self.fs)
        ax_fft.plot(fft_freqs, fft_vals, color=green_color, linewidth=0.9)
        ax_fft.set_title("FFT SPECTRUM (FREQUENCY DOMAIN)", color=green_color, fontsize=7, fontweight='bold', loc='left')
        ax_fft.set_xlabel("Frequency (Hz)", color='#9CA3AF', fontsize=6)
        ax_fft.set_ylabel("Magnitude", color='#9CA3AF', fontsize=6)
        ax_fft.grid(True, linestyle=':', linewidth=0.5, color=grid_color)
        ax_fft.set_xlim(0, 3500)

        # 3. PREDICTION PROBABILITY BARS
        y_pos = np.arange(len(CLASSES))
        bars = ax_prob.barh(y_pos, self.current_probs * 100.0, color='#1F2937', edgecolor=cyan_color, height=0.6)
        bars[self.current_pred].set_color('#0284C7')
        bars[self.current_pred].set_edgecolor(green_color)

        ax_prob.set_yticks(y_pos)
        ax_prob.set_yticklabels([c.split()[0] for c in CLASSES], fontsize=6, color='#9CA3AF')
        ax_prob.invert_yaxis()
        ax_prob.set_title("FAULT PROBABILITY DENSITY (%)", color=yellow_color, fontsize=7, fontweight='bold', loc='left')
        ax_prob.set_xlabel("Probability (%)", color='#9CA3AF', fontsize=6)
        ax_prob.set_xlim(0, 100)
        ax_prob.grid(True, linestyle=':', linewidth=0.5, color=grid_color)

        # 4. CONFUSION MATRIX HEATMAP
        if self.cm is not None:
            im = ax_cm.imshow(self.cm, interpolation='nearest', cmap='Blues')
            ax_cm.set_title("TEST CONFUSION MATRIX", color=cyan_color, fontsize=7, fontweight='bold', loc='left')
            tick_marks = np.arange(len(CLASSES))
            short_labels = ["Hlt", "Brg", "Ger", "Mis", "Cav"]
            ax_cm.set_xticks(tick_marks)
            ax_cm.set_xticklabels(short_labels, fontsize=6, color='#9CA3AF')
            ax_cm.set_yticks(tick_marks)
            ax_cm.set_yticklabels(short_labels, fontsize=6, color='#9CA3AF')

            for i in range(self.cm.shape[0]):
                for j in range(self.cm.shape[1]):
                    ax_cm.text(j, i, str(self.cm[i, j]), ha="center", va="center", color="white" if self.cm[i, j] > np.max(self.cm)/2 else "#9CA3AF", fontsize=7)

        # 5. RANDOM FOREST FEATURE IMPORTANCE BARS
        if self.feature_importances is not None:
            x_feat = np.arange(len(FEATURE_NAMES))
            ax_imp.bar(x_feat, self.feature_importances * 100.0, color='#38BDF8', width=0.5)
            ax_imp.set_xticks(x_feat)
            ax_imp.set_xticklabels([f.split()[0] for f in FEATURE_NAMES], rotation=25, ha='right', fontsize=6, color='#9CA3AF')
            ax_imp.set_title("RANDOM FOREST FEATURE IMPORTANCE RANKING (%)", color=green_color, fontsize=7, fontweight='bold', loc='left')
            ax_imp.set_ylabel("Importance (%)", color='#9CA3AF', fontsize=6)
            ax_imp.grid(True, linestyle=':', linewidth=0.5, color=grid_color)

        self.fig.tight_layout()
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(DARK_STYLE)

    window = MachineFaultAnalyzerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()