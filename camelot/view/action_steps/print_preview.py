#  ============================================================================
#
#  Copyright (C) 2007-2012 Conceptive Engineering bvba. All rights reserved.
#  www.conceptive.be / project-camelot@conceptive.be
#
#  This file is part of the Camelot Library.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file license.txt included in the packaging of
#  this file.  Please review this information to ensure GNU
#  General Public Licensing requirements will be met.
#
#  If you are unsure which license is appropriate for your use, please
#  visit www.python-camelot.com or contact project-camelot@conceptive.be
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#  For use of this library in commercial applications, please contact
#  project-camelot@conceptive.be
#
#  ============================================================================

from PyQt4 import QtCore, QtGui

from camelot.admin.action import ActionStep
from camelot.core.templates import environment
from camelot.view.action_steps.open_file import OpenFile
from camelot.view.utils import resize_widget_to_screen

class PrintPreview( ActionStep ):
    """
    Display a print preview dialog box.
    
    :param document: an instance of :class:`QtGui.QTextDocument` or 
        :class:`QtWebKit.QWebView` that has a :meth:`print_` method.  The
        thread affinity of this object will be changed to be able to use it
        in the GUI.
        
    the print preview can be customised using these attributes :
        
    .. attribute:: page_size
    
        the page size, by default :class:`QtGui.QPrinter.A4` is used
    
    .. attribute:: page_orientation
    
        the page orientation, by default :class:`QtGui.QPrinter.Portrait`
        is used.
    
    .. image:: /_static/simple_report.png
        """
    
    def __init__( self, document ):
        self.document = document
        self.document.moveToThread( QtCore.QCoreApplication.instance().thread() )
        self.printer = None
        self.page_size = None
        self.page_orientation = None

    def render( self ):
        """create the print preview widget. this method is used to unit test
        the action step."""
        if not self.printer:
            self.printer = QtGui.QPrinter()
        if not self.printer.isValid():
            self.printer.setOutputFormat( QtGui.QPrinter.PdfFormat )
        if self.page_size != None:
            self.printer.setPageSize( self.page_size )
        if self.page_orientation != None:
            self.printer.setOrientation( self.page_orientation )
        dialog = QtGui.QPrintPreviewDialog( self.printer, flags=QtCore.Qt.Window )
        dialog.paintRequested.connect( self.paint_on_printer )
        # show maximized seems to trigger a bug in qt which scrolls the page 
        # down dialog.showMaximized()
        resize_widget_to_screen( dialog )
        return dialog
    
    @QtCore.pyqtSlot( QtGui.QPrinter )
    def paint_on_printer( self, printer ):
        self.document.print_( printer )
     
    def gui_run( self, gui_context ):
        dialog = self.render()
        dialog.exec_()

class ChartDocument( QtCore.QObject ):
    """Helper class to print matplotlib charts

    :param chart: a :class:`camelot.container.chartcontainer.FigureContainer` object
        or a :class:`camelot.container.chartcontainer.AxesContainer` subclass

    """
    
    def __init__( self, chart ):
        from camelot.container.chartcontainer import structure_to_figure_container
        super( ChartDocument, self ).__init__()
        self.chart = structure_to_figure_container( chart )
        
    def print_( self, printer ):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
        rect = printer.pageRect( QtGui.QPrinter.Inch )
        dpi = printer.resolution()
        fig = Figure( facecolor='#ffffff')
        fig.set_size_inches( ( rect.width(), rect.height() ) )
        fig.set_dpi( dpi )
        self.chart.plot_on_figure( fig )
        canvas = FigureCanvas( fig )
        canvas.render( printer )   
        
class PrintChart( PrintPreview ):
    """
    Display a print preview dialog box for a matplotlib chart.
    
    :param chart: a :class:`camelot.container.chartcontainer.FigureContainer` object
        or a :class:`camelot.container.chartcontainer.AxesContainer` subclass
        
    Example use of this action step :
        
    .. literalinclude:: ../../../test/test_action.py
       :start-after: begin chart print
       :end-before: end chart print
    """

    def __init__( self, chart ):
        super( PrintChart, self ).__init__( ChartDocument( chart ) )
    
class PrintHtml( PrintPreview ):
    """
    Display a print preview dialog box for an html string.
    
    :param html: a string containing the html to render in the print
        preview.
        
    the rendering of the html can be customised using the same attributes
    as those of the :class:`PrintPreview` class.
        """
    
    def __init__( self, html ):
        document = QtGui.QTextDocument()
        document.setHtml( html )
        super( PrintHtml, self ).__init__( document )

class PrintJinjaTemplate( PrintHtml ):
    """Render a jinja template into a print preview dialog.
            
    :param template: the name of the template as it can be fetched from
        the Jinja environment.
        
    :param context: a dictionary with objects to be used when rendering
        the template
        
    :param environment: a :class:`jinja2.Environment` object to be used
        to load templates from.  This defaults to the `environment` object
        available in :mod:`camelot.core.templates`
    """
        
    def __init__( self,
                  template, 
                  context={},
                  environment = environment ):
        self.template = environment.get_template( template )
        self.html = self.template.render( context )
        self.context = context
        super( PrintJinjaTemplate, self).__init__( self.html )
    
    def get_pdf( self ):
        doc = QtGui.QTextDocument() 
        doc.setHtml(self.template.render( self.context ))
        printer = QtGui.QPrinter()
        printer.setOutputFormat( QtGui.QPrinter.PdfFormat )
        filepath = OpenFile.create_temporary_file('.pdf')
        printer.setOutputFileName(filepath)
        doc.print_(printer)
        return filepath
