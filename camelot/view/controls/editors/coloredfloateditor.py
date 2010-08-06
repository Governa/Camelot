from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from customeditor import CustomEditor
from camelot.core import constants
from camelot.view.art import Icon

class ColoredFloatEditor(CustomEditor):
    """Widget for editing a float field, with a calculator"""
      
    def __init__(self,
                 parent,
                 precision=2,
                 reverse=False,
                 neutral=False,
                 **kwargs):
        CustomEditor.__init__(self, parent)
        action = QtGui.QAction(self)
        action.setShortcut(Qt.Key_F3)
        self.setFocusPolicy(Qt.StrongFocus)
        self.spinBox = QtGui.QDoubleSpinBox(parent)

        self.spinBox.setDecimals(precision)
        self.spinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.spinBox.setSingleStep(1.0)
        self.spinBox.addAction(action)
        self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.arrow = QtGui.QLabel()
        self.arrow.setPixmap(Icon('tango/16x16/actions/go-up.png').getQPixmap())
        self.arrow.setFixedHeight(self.get_height())
    
        self.arrow.setAutoFillBackground(False)
        self.arrow.setMaximumWidth(19)
    
        self.calculatorButton = QtGui.QToolButton()
        icon = Icon('tango/16x16/apps/accessories-calculator.png').getQIcon()
        self.calculatorButton.setIcon(icon)
        self.calculatorButton.setAutoRaise(True)
        self.calculatorButton.setFixedHeight(self.get_height())
    
        self.connect(self.calculatorButton,
                     QtCore.SIGNAL('clicked()'),
                     lambda:self.popupCalculator(self.spinBox.value()))
        self.connect(action,
                     QtCore.SIGNAL('triggered(bool)'),
                     lambda:self.popupCalculator(self.spinBox.value()))
        self.connect(self.spinBox,
                     QtCore.SIGNAL('editingFinished()'),
                     lambda:self.editingFinished(self.spinBox.value()))
    
        self.releaseKeyboard()
    
        layout = QtGui.QHBoxLayout()
        layout.setMargin(0)
        layout.setSpacing(0)
        layout.addSpacing(3.5)
        layout.addWidget(self.arrow)
        layout.addWidget(self.spinBox)
        layout.addWidget(self.calculatorButton)
        self.reverse = reverse
        self.neutral = neutral
        self.setFocusProxy(self.spinBox)
        self.setLayout(layout)
        if not self.reverse:
            if not self.neutral:
                self.icons = {
                    -1:Icon('tango/16x16/actions/go-down-red.png').getQPixmap(), 
                    1:Icon('tango/16x16/actions/go-up.png').getQPixmap(),
                    0:Icon('tango/16x16/actions/zero.png').getQPixmap()
                }
            else:
                self.icons = {
                    -1:Icon('tango/16x16/actions/go-down-blue.png').getQPixmap(), 
                    1:Icon('tango/16x16/actions/go-up-blue.png').getQPixmap(),
                    0:Icon('tango/16x16/actions/zero.png').getQPixmap()
                }
        else:
            self.icons = {
                1:Icon('tango/16x16/actions/go-down-red.png').getQPixmap(), 
                -1:Icon('tango/16x16/actions/go-up.png').getQPixmap(),
                0:Icon('tango/16x16/actions/zero.png').getQPixmap()
            }
            
    def set_field_attributes(self, 
                             editable=True, 
                             background_color=None, 
                             prefix='', 
                             suffix='',
                             minimum=constants.camelot_minfloat,
                             maximum=constants.camelot_maxfloat,  
                             **kwargs):
        self.set_enabled(editable)
        self.set_background_color(background_color)
        self.spinBox.setPrefix(u'%s '%(unicode(prefix).lstrip()))
        self.spinBox.setSuffix(u' %s'%(unicode(suffix).rstrip()))
        self.spinBox.setRange(minimum, maximum)
        
    def set_enabled(self, editable=True):
        self.spinBox.setReadOnly(not editable)
        self.spinBox.setEnabled(editable)
        self.calculatorButton.setShown(editable)
        if editable:
            self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        else:
            self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
            
    def set_value(self, value):
        value = CustomEditor.set_value(self, value) or 0.0
        self.spinBox.setValue(value)
        self.arrow.setPixmap(self.icons[cmp(value,0)])
            
    def get_value(self):
        self.spinBox.interpretText()
        value = self.spinBox.value()
        return CustomEditor.get_value(self) or value
      
    def popupCalculator(self, value):
        from camelot.view.controls.calculator import Calculator
        calculator = Calculator(self)
        calculator.setValue(value)
        self.connect(calculator,
                     QtCore.SIGNAL('calculationFinished'),
                     self.calculationFinished)
        calculator.exec_()
    
    def calculationFinished(self, value):
        self.spinBox.setValue(float(value))
        self.emit(QtCore.SIGNAL('editingFinished()'))
    
    def editingFinished(self, value):
        self.emit(QtCore.SIGNAL('editingFinished()'))
