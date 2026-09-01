# ⚙️ Machine Sound Fault Analyzer

> An interactive industrial acoustic-analysis laboratory for studying machine sounds, identifying frequency-domain characteristics, and exploring acoustic indicators of mechanical faults using digital signal processing.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt)
[![NumPy](https://img.shields.io/badge/Numerical-NumPy-orange?logo=numpy)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-orange?logo=matplotlib)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<img width="973" height="513" alt="image" src="https://github.com/user-attachments/assets/3ea22175-a325-4bd7-a8fb-71a44526aded" />


---

## 📌 Overview

**Machine Sound Fault Analyzer** is an interactive desktop application for exploring how **acoustic signals can be used to investigate machine condition and potential mechanical faults**.

Mechanical systems generate characteristic sounds during operation. Changes in these acoustic signatures can provide useful indicators of abnormal operating conditions, component degradation, friction, impacts, imbalance, or other mechanical phenomena.

The project provides a virtual laboratory for studying:

* Machine acoustic signatures
* Frequency-domain analysis
* FFT-based analysis
* Acoustic fault indicators
* Harmonics
* Noise
* Transient events
* Frequency peaks
* Signal amplitude
* Condition monitoring
* Predictive maintenance concepts

---

# ✨ Key Features

## 🔊 Machine Sound Simulation

The analyzer provides a controlled environment for studying simulated machine acoustic signals.

A simplified machine sound can contain:

```text
Machine Signal
      │
      ├── Fundamental Frequency
      │
      ├── Harmonics
      │
      ├── Noise
      │
      └── Fault-Related Components
```

Changes in these components can alter the acoustic signature of the machine.

---

# 📈 Time-Domain Analysis

A machine sound can first be represented as a waveform.

```text id="m7q3vx"
Amplitude
   │
   │     ╭──╮      ╭──╮
   │    ╱    ╲    ╱    ╲
───┼───╯──────╰──╯──────╰────────► Time
   │
```

Time-domain characteristics can provide information about:

* Periodicity
* Impacts
* Transients
* Amplitude variations
* Noise
* Irregular operation

---

# 📊 Frequency-Domain Analysis

The FFT transforms the acoustic waveform into its frequency representation.

```text id="c8n5rz"
Amplitude
   │
   │        █
   │        █
   │        █       █
   │        █       █
───┼────────█───────█─────────────► Frequency
           f₁      f₂
```

Frequency peaks may correspond to:

* Rotational frequency
* Harmonics
* Gear-mesh frequencies
* Bearing-related components
* Structural resonances
* Electrical excitation
* Fault-related frequencies

---

# 🧮 Fast Fourier Transform

The **Fast Fourier Transform (FFT)** provides an efficient method for converting a time-domain machine signal into its frequency-domain representation.

Conceptually:

```text id="v5k9mq"
Machine Sound
      │
      ▼
Time-Domain Signal
      │
      ▼
     FFT
      │
      ▼
Frequency Spectrum
      │
      ▼
Frequency Peak Analysis
```

This makes it possible to investigate frequency components that may not be obvious from the raw waveform.

---

# ⚙️ Rotational Frequency

Rotating machinery often produces a fundamental frequency associated with shaft speed.

For rotational speed in RPM:

```text id="q3m7cx"
fᵣ = RPM / 60
```

where:

* `fᵣ` = rotational frequency in Hz
* `RPM` = revolutions per minute

For example:

```text id="x8n2vp"
1800 RPM
   ↓
1800 / 60
   ↓
30 Hz
```

The corresponding fundamental component may appear in the acoustic spectrum.

---

# 🔁 Harmonic Analysis

Mechanical systems can generate harmonics of their fundamental rotational frequency.

```text id="k4r8zm"
fᵣ
2fᵣ
3fᵣ
4fᵣ
...
```

A simplified spectrum may look like:

```text id="p6v3xy"
Amplitude
   │
   │   █
   │   █       █
   │   █       █       █
   │   █       █       █       █
───┼───█───────█───────█───────█──► Frequency
      fᵣ     2fᵣ     3fᵣ     4fᵣ
```

Changes in harmonic content can provide useful clues about machine behavior.

---

# ⚠️ Fault Signature Concept

Mechanical faults can modify the acoustic spectrum.

A simplified conceptual workflow is:

```text id="r7c4mz"
Healthy Machine
      │
      ▼
Baseline Acoustic Signature
      │
      │
      ▼
Machine Degradation
      │
      ▼
New Frequency Components
      │
      ▼
Changed Acoustic Signature
      │
      ▼
Potential Fault Indicator
```

Possible fault-related acoustic phenomena include:

* Increased vibration-related noise
* Periodic impacts
* New harmonics
* Broadband noise
* Resonant peaks
* Amplitude modulation
* Repetitive impulses

---

# ⚙️ Bearing Fault Concept

Rolling-element bearings can generate characteristic repetitive impacts when damaged.

A simplified acoustic signature might contain:

```text id="n5m8qy"
Normal:
~~~~~ ~~~~~ ~~~~~ ~~~~~


Potential Fault:
~^~~~ ~^~~~ ~^~~~ ~^~~~
```

These repetitive events may introduce characteristic frequency components into the measured signal.

In real condition-monitoring systems, bearing analysis often combines acoustic, vibration, and other sensor data.

---

# ⚙️ Gear Fault Concept

Gear systems can generate strong periodic components related to gear meshing.

A simplified relationship is:

```text id="w3k7xn"
Gear Mesh Frequency
        =
Number of Teeth × Rotational Frequency
```

For example:

```text id="j8m4vc"
40 Teeth × 30 Hz
       ↓
1200 Hz
```

A gear-related spectral component may therefore appear near the corresponding gear-mesh frequency.

---

# ⚖️ Imbalance

Rotating imbalance can produce strong components related to the shaft rotational frequency.

```text id="c5r9mz"
Machine Speed
     ↓
Rotational Frequency
     ↓
Acoustic / Vibration Component
```

A dominant peak near the rotational frequency can be an indicator worth investigating, although it is not sufficient by itself to diagnose imbalance.

---

# 🔩 Misalignment

Shaft or coupling misalignment can produce additional harmonics and changes in the machine's acoustic signature.

Conceptually:

```text id="v4n7qp"
Healthy
   ↓
Dominant Fundamental


Potential Misalignment
   ↓
Fundamental + Additional Harmonics
```

Acoustic analysis can be used as one part of a broader machine-condition assessment.

---

# 🔊 Noise Analysis

Industrial environments often contain significant background noise.

```text id="m9c3xz"
Machine Signal
      +
Background Noise
      ↓
Measured Acoustic Signal
```

Noise can originate from:

* Nearby machines
* Fans
* Pumps
* Airflow
* Bearings
* Structural vibration
* Electrical systems
* Environmental sources

Separating machine-specific features from background noise is an important challenge in acoustic condition monitoring.

---

# 📉 Signal-to-Noise Ratio

Signal quality can be evaluated conceptually using SNR.

```text id="p4k8yw"
SNR(dB) = 10 log₁₀(Psignal / Pnoise)
```

Higher SNR generally makes machine-specific acoustic features easier to identify.

---

# 🌊 Spectrogram Analysis

Machine sounds can change over time.

A spectrogram provides a time-frequency representation:

```text id="x6m2vz"
Frequency
   │
   │ ███
   │ ███      ███
   │ ███      ████
   │    █████████
   │
   └────────────────────────► Time
```

This can help identify:

* Transient events
* Frequency changes
* Startup behavior
* Shutdown behavior
* Intermittent faults
* Changing operating conditions

---

# ⚡ Transient Fault Events

Some mechanical conditions produce short-duration impulses.

```text id="r8q5nk"
Amplitude
   │
   │        │
   │        │
───┼────────│─────────────────────► Time
   │        │
          Impact
```

Transient events may be easier to identify using time-frequency or envelope-based analysis rather than only a conventional FFT.

---

# 🔬 Machine Acoustic Analysis Pipeline

```text id="k7m3vx"
┌───────────────────────────────┐
│       Machine Sound           │
│                               │
│       Acoustic Signal         │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Preprocessing           │
│                               │
│ Filtering / Normalization     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Time-Domain Analysis     │
│                               │
│ Waveform / Amplitude          │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Frequency Analysis       │
│                               │
│ FFT / Spectrum                │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Feature Analysis        │
│                               │
│ Peaks / Harmonics / Noise     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Condition Assessment    │
│                               │
│ Baseline Comparison           │
└───────────────────────────────┘
```

---

# 🧪 Example Experiments

## Experiment 1 — Healthy Machine

Generate a baseline machine sound.

Observe:

* Fundamental frequency
* Harmonics
* Noise level
* Spectrum shape

---

## Experiment 2 — Increased Noise

Increase the background noise level.

Compare:

```text id="y5n8kc"
Clean Signal
     vs
Noisy Signal
```

Observe how fault-related frequency components become more difficult to identify.

---

## Experiment 3 — Rotational Speed

Change the simulated machine RPM.

Calculate:

```text id="q8m4zr"
f = RPM / 60
```

Observe how the fundamental frequency shifts.

---

## Experiment 4 — Harmonic Content

Introduce additional harmonic components.

Compare the frequency spectrum of:

```text id="p3v7mx"
Simple Machine
     vs
Complex Machine Signature
```

---

## Experiment 5 — Bearing-Like Impacts

Introduce repetitive transient events.

Observe the resulting time-domain and frequency-domain characteristics.

---

## Experiment 6 — Gear-Mesh Component

Introduce a frequency associated with gear-mesh operation.

Observe how the new spectral component appears in the frequency domain.

---

## Experiment 7 — Fault vs Baseline

Compare two acoustic signatures:

```text id="m6c9vy"
Baseline
   ↓
Reference Spectrum


Test Signal
   ↓
Measured Spectrum


Compare
   ↓
Identify Changes
```

This demonstrates the basic principle of condition-based monitoring.

---

# 🏭 Industrial Applications

Acoustic machine-condition monitoring can be relevant to:

### 🏭 Manufacturing

* Motors
* Pumps
* Compressors
* Gearboxes
* Fans
* Machine tools

### ⚙️ Rotating Machinery

* Bearings
* Shafts
* Couplings
* Gear systems
* Rotors

### 🚢 Marine

* Propulsion systems
* Pumps
* Motors
* Auxiliary machinery
* Rotating equipment

### ⚡ Power Generation

* Turbines
* Generators
* Pumps
* Fans
* Compressors

### 🛢️ Oil & Gas

* Pumps
* Compressors
* Rotating machinery
* Pipeline equipment

---

# 🔧 Predictive Maintenance Concept

The analyzer demonstrates the fundamental concept behind acoustic condition monitoring:

```text id="z4r8qn"
Healthy Machine
      │
      ▼
Baseline Signature
      │
      ▼
Continuous Monitoring
      │
      ▼
Signature Changes
      │
      ▼
Potential Anomaly
      │
      ▼
Maintenance Investigation
```

The objective is to identify changes early enough to support condition-based maintenance.

---

# 🤖 Future AI Integration

Acoustic machine monitoring can be extended using machine learning.

A possible pipeline:

```text id="n7c5xm"
Machine Audio
      │
      ▼
Signal Processing
      │
      ▼
Feature Extraction
      │
      ├── FFT Features
      ├── Spectral Features
      ├── RMS
      ├── Crest Factor
      └── Spectrogram
      │
      ▼
Machine Learning Model
      │
      ▼
Classification
      │
      ├── Normal
      ├── Bearing Fault
      ├── Gear Fault
      └── Other Anomaly
```

Potential models include:

* Random Forest
* Support Vector Machine
* Gradient Boosting
* Neural Networks
* CNN-based spectrogram classification
* Autoencoders for anomaly detection

---

# 🎓 Educational Applications

This project can be used to demonstrate:

* Machine Acoustics
* Condition Monitoring
* Predictive Maintenance
* FFT
* Frequency-Domain Analysis
* Harmonic Analysis
* Rotational Frequency
* Gear-Mesh Frequency
* Bearing Fault Concepts
* Imbalance
* Misalignment
* Noise Analysis
* Signal-to-Noise Ratio
* Spectrograms
* Transient Analysis
* Digital Signal Processing
* Industrial IoT Concepts

---

# 🛠️ Technology Stack

| Technology     | Purpose                                     |
| -------------- | ------------------------------------------- |
| **Python**     | Core application                            |
| **NumPy**      | Numerical computation and signal processing |
| **PyQt5**      | Desktop graphical interface                 |
| **Matplotlib** | Waveform and spectrum visualization         |

---

# 🚀 Installation

### 1. Clone the repository

```bash id="c7m4zx"
git clone https://github.com/vishwakiran712/Machine-Sound-Fault-Analyzer.git
cd Machine-Sound-Fault-Analyzer
```

### 2. Install dependencies

```bash id="v9k2qp"
pip install numpy matplotlib PyQt5
```

### 3. Run the application

```bash id="r5m8yc"
python app.py
```

---

# 📂 Project Structure

```text id="x3n7vz"
Machine-Sound-Fault-Analyzer/
│
├── app.py
├── README.md
└── LICENSE
```

---

# 🔭 Possible Future Enhancements

Potential extensions include:

* Real microphone input
* WAV file import
* Industrial audio dataset support
* Real-time acoustic monitoring
* FFT analysis
* STFT analysis
* Spectrogram generation
* Envelope analysis
* Band-pass filtering
* Notch filtering
* Automatic peak detection
* Rotational-speed tracking
* RPM input
* Bearing fault-frequency calculation
* Gear-mesh frequency calculation
* Sideband analysis
* Order tracking
* RMS calculation
* Crest factor
* Kurtosis
* Spectral centroid
* Spectral entropy
* Noise-floor estimation
* Baseline comparison
* Automated anomaly detection
* Machine-learning classification
* Fault severity estimation
* Predictive maintenance dashboard
* Historical trend analysis
* Database integration
* IoT sensor integration
* Edge-AI deployment
* Automated maintenance alerts
* PDF inspection reports

---

# ⚠️ Important Notice

This application is intended for **education, experimentation, and research in acoustic condition monitoring**.

A frequency peak or acoustic anomaly alone does **not** constitute a definitive machine-fault diagnosis. Real industrial condition monitoring requires appropriate sensors, controlled measurements, machine operating parameters, baseline data, calibration, signal processing, and validation by qualified personnel.

The simulated fault signatures in this project are simplified representations of real mechanical phenomena.

---

# 📜 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

# 👨‍💻 Author

**Vishwakiran B.V.S.**

Engineering • Sports Technology • Product Research • Marine Robotics • NDT • Hydrography • Acoustics • Signal Processing

GitHub: [@vishwakiran712](https://github.com/vishwakiran712)

---

# ⭐ Project

If you find this project useful for learning, industrial acoustics, predictive maintenance, condition monitoring, or digital signal processing, consider giving the repository a ⭐.

**Repository:**
https://github.com/vishwakiran712/Machine-Sound-Fault-Analyzer
