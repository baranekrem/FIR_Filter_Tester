import sys
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from gui import Ui_Dialog
from numpy import sin, pi, linspace
from scipy import fft
import FIRFilter

freqs = [0] * 3
fcl = 0
fch = 0
sampleCount = 20000
order = 10
filtertype = FIRFilter.FilterType.LowPass

firfilter = FIRFilter.Filter(filtertype, sampleCount, order, fcl)

def TestFunction():
    T = 1.0 / sampleCount

    xt = linspace((-pi / 2), (pi / 2), sampleCount)

    yt = sin(2 * freqs[0] * xt) + sin(2 * freqs[1] * xt) + sin(2 * freqs[2] * xt)

    xf = linspace(0.0, 1.0 / (2.0 * T), int(sampleCount / 2))

    yf1 = fft.fft(yt)

    yf1 = (2.0 / sampleCount * abs(yf1[:sampleCount // 2]))

    yt = firfilter.FilterApply(yt)

    yf2 = fft.fft(yt)

    yf2 = (2.0 / sampleCount * abs(yf2[:sampleCount // 2]))

    return (xf, yf1, yf2)

class myDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(myDialog, self).__init__()
        self.setupUi(self)

        self.horizontalSlider1.sliderReleased.connect(self.sliderReleased_Event)
        self.horizontalSlider2.sliderReleased.connect(self.sliderReleased_Event)
        self.horizontalSlider3.sliderReleased.connect(self.sliderReleased_Event)

        list = ['Low Pass', 'High Pass', 'Band Pass', 'Band Stop']
        self.comboBoxFilterType.clear()
        self.comboBoxFilterType.addItems(list)
        self.comboBoxFilterType.currentIndexChanged.connect(self.comboBoxCurrentIndexChanged_Event)
        self.comboBoxFilterType.setCurrentIndex(0)
        self.buttonSet.clicked.connect(self.buttonClicked_Event)

        rx = QRegExp("\d+")
        self.textBoxFl.setValidator(QRegExpValidator(rx))
        self.textBoxFh.setValidator(QRegExpValidator(rx))

        self.textBoxFh.setEnabled(False)

        self.spinBoxOrder.valueChanged.connect(self.spinBoxValueChanged_Event)
        self.spinBoxOrder.setValue(order)

        self.fig1 = Figure()
        canvas = FigureCanvasQTAgg(self.fig1)
        toolbar = NavigationToolbar(canvas, self)

        layout1 = QVBoxLayout()
        layout1.addWidget(canvas)
        layout1.addWidget(toolbar)

        self.widget1.setLayout(layout1)
        self.widget1.show()

        self.fig2 = Figure()
        canvas = FigureCanvasQTAgg(self.fig2)
        toolbar = NavigationToolbar(canvas, self)

        layout2 = QVBoxLayout()
        layout2.addWidget(canvas)
        layout2.addWidget(toolbar)

        self.widget2.setLayout(layout2)
        self.widget2.show()

    def plot(self):
        xt, yt1, yt2 = TestFunction()

        self.fig1.clear()
        self.ax1 = self.fig1.add_subplot(1, 1, 1)
        self.ax1.plot(xt, yt1)
        self.ax1.grid(True)
        self.ax1.set_xlim((0, 5000))
        self.ax1.set_ylim((0, 1.1))
        self.ax1.set_title('Input (Hz)')
        k = self.ax1.set_ylabel('Magnitude')
        k.set_color(color='black')
        k.set_fontsize('large')
        self.fig1.canvas.draw()

        self.fig2.clear()
        self.ax2 = self.fig2.add_subplot(1, 1, 1)
        self.ax2.plot(xt, yt2)
        self.ax2.grid(True)
        self.ax2.set_xlim((0, 5000))
        self.ax2.set_ylim((0, 1.1))
        self.ax2.set_title('Output (Hz)')
        l = self.ax2.set_ylabel('Magnitude')
        l.set_color(color='black')
        l.set_fontsize('large')
        self.fig2.canvas.draw()

    def sliderReleased_Event(self):
        freqs[0] = self.horizontalSlider1.value()
        freqs[1] = self.horizontalSlider2.value()
        freqs[2] = self.horizontalSlider3.value()

        self.label1.setText(str(freqs[0]) + ' Hz')
        self.label2.setText(str(freqs[1]) + ' Hz')
        self.label3.setText(str(freqs[2]) + ' Hz')

        self.plot()

    def comboBoxCurrentIndexChanged_Event(self):
        filtertype = FIRFilter.FilterType(self.comboBoxFilterType.currentIndex())
        firfilter.SetType(filtertype)

        if filtertype == filtertype.LowPass or filtertype == filtertype.HighPass:
            self.textBoxFh.setEnabled(False)
        else:
            self.textBoxFh.setEnabled(True)

    def spinBoxValueChanged_Event(self):
        order = self.spinBoxOrder.value()
        firfilter.SetOrder(order)

    def buttonClicked_Event(self):
        type = firfilter.GetType()

        if type == FIRFilter.FilterType.LowPass or type == FIRFilter.FilterType.HighPass:
            self.fcl = int(self.textBoxFl.text())
            firfilter.SetFrequency(self.fcl)

        if type == FIRFilter.FilterType.BandPass or type == FIRFilter.FilterType.BandStop:
            self.fcl = int(self.textBoxFl.text())
            self.fch = int(self.textBoxFh.text())
            firfilter.SetLowFrequency(self.fcl)
            firfilter.SetHighFrequency(self.fch)
        print(firfilter.GetCoefficients())
        self.plot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = myDialog()
    myWindow.show()
    sys.exit(app.exec_())