# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"µTopia - Controller"), pos = wx.DefaultPosition, size = wx.Size( 420,590 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		self.main_sizer = wx.BoxSizer( wx.VERTICAL )

		self.main_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panels_sizer = wx.BoxSizer( wx.VERTICAL )


		self.main_panel.SetSizer( self.panels_sizer )
		self.main_panel.Layout()
		self.panels_sizer.Fit( self.main_panel )
		self.main_sizer.Add( self.main_panel, 1, wx.EXPAND, 5 )


		self.SetSizer( self.main_sizer )
		self.Layout()
		self.sb = self.CreateStatusBar( 2, wx.ST_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()


###########################################################################
## Class ViewerFrame
###########################################################################

class ViewerFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )

		main_sizer = wx.BoxSizer( wx.VERTICAL )

		self.slice = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		main_sizer.Add( self.slice, 0, 0, 0 )


		self.SetSizer( main_sizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CHAR, self.OnChar )
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_KEY_DOWN, self.OnKeyDown )
		self.Bind( wx.EVT_KEY_UP, self.OnKeyUp )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnChar( self, event ):
		event.Skip()

	def OnClose( self, event ):
		event.Skip()

	def OnKeyDown( self, event ):
		event.Skip()

	def OnKeyUp( self, event ):
		event.Skip()


###########################################################################
## Class PrinterPanel
###########################################################################

class PrinterPanel ( wx.Panel ):

	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )

		main_sizer = wx.BoxSizer( wx.VERTICAL )

		printer_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.printers_label = wx.StaticText( self, wx.ID_ANY, _(u"Printer"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.printers_label.Wrap( -1 )
		printer_sizer.Add( self.printers_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		printersChoices = []
		self.printers = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, printersChoices, 0 )
		self.printers.SetSelection( 0 )
		self.printers.SetToolTipString( _(u"Printers list (serial ports)") )

		printer_sizer.Add( self.printers, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT, 5 )
		
		self.refresh = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"./assets/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.refresh.SetToolTipString( _(u"Refresh printers list") )

		printer_sizer.Add( self.refresh, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.printer_on_off = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"./assets/power-off.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )

		self.printer_on_off.SetBitmapSelected( wx.NullBitmap )
		self.printer_on_off.SetToolTipString( _(u"Connect") )

		printer_sizer.Add( self.printer_on_off, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT, 5 )


		main_sizer.Add( printer_sizer, 0, wx.EXPAND, 5 )

		controls_sizer = wx.BoxSizer( wx.HORIZONTAL )

		buttons_sizer_group1 = wx.BoxSizer( wx.VERTICAL )

		self.motor_on_off = wx.Button( self, wx.ID_ANY, _(u"Turn motor ON"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.motor_on_off.SetToolTipString( _(u"Turn motor ON") )

		buttons_sizer_group1.Add( self.motor_on_off, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.light_on_off = wx.Button( self, wx.ID_ANY, _(u"Turn light ON"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.light_on_off.SetToolTipString( _(u"Turn light ON") )

		buttons_sizer_group1.Add( self.light_on_off, 0, wx.EXPAND|wx.ALL, 5 )


		controls_sizer.Add( buttons_sizer_group1, 1, 0, 5 )

		buttons_sizer_group2 = wx.BoxSizer( wx.VERTICAL )

		self.lift_up = wx.Button( self, wx.ID_ANY, _(u"Lift up (+10)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lift_up.SetToolTipString( _(u"Move Z axis up (10mm)") )

		buttons_sizer_group2.Add( self.lift_up, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5 )

		self.lift_down = wx.Button( self, wx.ID_ANY, _(u"Lift down (-10)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lift_down.SetToolTipString( _(u"Move Z axis down (10mm)") )

		buttons_sizer_group2.Add( self.lift_down, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )


		controls_sizer.Add( buttons_sizer_group2, 1, 0, 5 )


		main_sizer.Add( controls_sizer, 0, wx.EXPAND, 5 )


		self.SetSizer( main_sizer )
		self.Layout()
		main_sizer.Fit( self )

		# Connect Events
		self.printers.Bind( wx.EVT_CHOICE, self.OnPrinterChange )
		self.refresh.Bind( wx.EVT_BUTTON, self.OnRefreshClick )
		self.printer_on_off.Bind( wx.EVT_BUTTON, self.OnPrinterOnOffClick )
		self.motor_on_off.Bind( wx.EVT_BUTTON, self.OnMotorOnOffClick )
		self.light_on_off.Bind( wx.EVT_BUTTON, self.OnLightOnOffClick )
		self.lift_up.Bind( wx.EVT_BUTTON, self.OnLiftUpClick )
		self.lift_down.Bind( wx.EVT_BUTTON, self.OnLiftDownClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnPrinterChange( self, event ):
		event.Skip()

	def OnRefreshClick( self, event ):
		event.Skip()

	def OnPrinterOnOffClick( self, event ):
		event.Skip()

	def OnMotorOnOffClick( self, event ):
		event.Skip()

	def OnLightOnOffClick( self, event ):
		event.Skip()

	def OnLiftUpClick( self, event ):
		event.Skip()

	def OnLiftDownClick( self, event ):
		event.Skip()


###########################################################################
## Class DisplayPanel
###########################################################################

class DisplayPanel ( wx.Panel ):

	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )

		main_sizer = wx.BoxSizer( wx.VERTICAL )

		display_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.printers_label = wx.StaticText( self, wx.ID_ANY, _(u"Display"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.printers_label.Wrap( -1 )
		display_sizer.Add( self.printers_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		displaysChoices = []
		self.displays = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, displaysChoices, 0 )
		self.displays.SetSelection( 0 )
		self.displays.SetToolTipString( _(u"Displays list") )

		display_sizer.Add( self.displays, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.refresh = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"./assets/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.refresh.SetToolTipString( _(u"Refresh displays list") )

		display_sizer.Add( self.refresh, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.open_close = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"./assets/expand.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.open_close.SetToolTipString( _(u"Open viewer") )

		display_sizer.Add( self.open_close, 0, wx.TOP|wx.BOTTOM|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )


		main_sizer.Add( display_sizer, 0, wx.EXPAND, 5 )


		self.SetSizer( main_sizer )
		self.Layout()
		main_sizer.Fit( self )

		# Connect Events
		self.displays.Bind( wx.EVT_CHOICE, self.OnDisplayChange )
		self.refresh.Bind( wx.EVT_BUTTON, self.OnRefreshClick )
		self.open_close.Bind( wx.EVT_BUTTON, self.OnOpenCloseClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnDisplayChange( self, event ):
		event.Skip()

	def OnRefreshClick( self, event ):
		event.Skip()

	def OnOpenCloseClick( self, event ):
		event.Skip()


###########################################################################
## Class ProjectPanel
###########################################################################

class ProjectPanel ( wx.Panel ):

	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )

		main_sizer = wx.BoxSizer( wx.VERTICAL )

		project_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.project_label = wx.StaticText( self, wx.ID_ANY, _(u"Project"), wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self.project_label.Wrap( -1 )
		project_sizer.Add( self.project_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.project_path = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,25 ), wx.TE_READONLY )
		project_sizer.Add( self.project_path, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.open_zip = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, _(u"Select a file"), u"SLAcer ZIP (*.zip)|*.zip", wx.DefaultPosition, wx.Size( -1,27 ), wx.FLP_FILE_MUST_EXIST )
		project_sizer.Add( self.open_zip, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )

		self.open_folder = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.Size( -1,27 ), wx.DIRP_DIR_MUST_EXIST )
		project_sizer.Add( self.open_folder, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )


		main_sizer.Add( project_sizer, 0, wx.EXPAND, 5 )

		slider_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText76 = wx.StaticText( self, wx.ID_ANY, _(u"Preview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText76.Wrap( -1 )
		slider_sizer.Add( self.m_staticText76, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.slice = wx.Slider( self, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		slider_sizer.Add( self.slice, 1, wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )


		main_sizer.Add( slider_sizer, 0, wx.EXPAND, 5 )

		settings_sizer = wx.BoxSizer( wx.HORIZONTAL )

		settings_sizer_group1 = wx.BoxSizer( wx.VERTICAL )

		layers_number_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, _(u"Layers number"), wx.DefaultPosition, wx.Size( 105,-1 ), 0 )
		self.m_staticText4.Wrap( -1 )
		layers_number_sizer.Add( self.m_staticText4, 0, wx.BOTTOM|wx.LEFT, 5 )

		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		layers_number_sizer.Add( self.m_staticText16, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		self.layers_number = wx.StaticText( self, wx.ID_ANY, _(u"n/a"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.layers_number.Wrap( -1 )
		layers_number_sizer.Add( self.layers_number, 1, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		settings_sizer_group1.Add( layers_number_sizer, 0, wx.EXPAND, 5 )

		layers_height_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, _(u"Layers height (mm)"), wx.DefaultPosition, wx.Size( 105,-1 ), 0 )
		self.m_staticText41.Wrap( -1 )
		self.m_staticText41.SetToolTipString( _(u"millimeters") )

		layers_height_sizer.Add( self.m_staticText41, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		layers_height_sizer.Add( self.m_staticText17, 0, wx.ALL, 5 )

		self.layers_height = wx.StaticText( self, wx.ID_ANY, _(u"n/a"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.layers_height.Wrap( -1 )
		self.layers_height.SetToolTipString( _(u"millimeters") )

		layers_height_sizer.Add( self.layers_height, 1, wx.ALL, 5 )


		settings_sizer_group1.Add( layers_height_sizer, 0, wx.EXPAND, 5 )

		total_height_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText411 = wx.StaticText( self, wx.ID_ANY, _(u"Total height (cm)"), wx.DefaultPosition, wx.Size( 105,-1 ), 0 )
		self.m_staticText411.Wrap( -1 )
		self.m_staticText411.SetToolTipString( _(u"centimeters") )

		total_height_sizer.Add( self.m_staticText411, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		total_height_sizer.Add( self.m_staticText18, 0, wx.ALL, 5 )

		self.total_height = wx.StaticText( self, wx.ID_ANY, _(u"n/a"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.total_height.Wrap( -1 )
		self.total_height.SetToolTipString( _(u"centimeters") )

		total_height_sizer.Add( self.total_height, 1, wx.ALL, 5 )


		settings_sizer_group1.Add( total_height_sizer, 0, wx.EXPAND, 5 )


		settings_sizer.Add( settings_sizer_group1, 0, wx.RIGHT, 5 )

		self.m_staticline6 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		settings_sizer.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )

		settings_sizer_group2 = wx.BoxSizer( wx.VERTICAL )

		exposure_time_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText421 = wx.StaticText( self, wx.ID_ANY, _(u"Exposure time (ms)"), wx.DefaultPosition, wx.Size( 130,-1 ), 0 )
		self.m_staticText421.Wrap( -1 )
		self.m_staticText421.SetToolTipString( _(u"milliseconds") )

		exposure_time_sizer.Add( self.m_staticText421, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

		self.m_staticText191 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText191.Wrap( -1 )
		exposure_time_sizer.Add( self.m_staticText191, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		self.exposure_time = wx.SpinCtrl( self, wx.ID_ANY, u"n/a", wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 500, 60000, 0 )
		self.exposure_time.SetToolTipString( _(u"milliseconds") )

		exposure_time_sizer.Add( self.exposure_time, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		settings_sizer_group2.Add( exposure_time_sizer, 0, wx.EXPAND, 5 )

		lifting_time_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4121 = wx.StaticText( self, wx.ID_ANY, _(u"Lifting speed (mm/min)"), wx.DefaultPosition, wx.Size( 130,-1 ), 0 )
		self.m_staticText4121.Wrap( -1 )
		self.m_staticText4121.SetToolTipString( _(u"millimeters/minute") )

		lifting_time_sizer.Add( self.m_staticText4121, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

		self.m_staticText201 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText201.Wrap( -1 )
		lifting_time_sizer.Add( self.m_staticText201, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lifting_speed = wx.SpinCtrl( self, wx.ID_ANY, u"n/a", wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 5, 500, 0 )
		self.lifting_speed.SetToolTipString( _(u"millimeters/minute") )

		lifting_time_sizer.Add( self.lifting_speed, 1, wx.ALIGN_CENTER_VERTICAL, 5 )


		settings_sizer_group2.Add( lifting_time_sizer, 0, wx.EXPAND, 5 )

		lifting_height_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText41111 = wx.StaticText( self, wx.ID_ANY, _(u"Lifting height (mm)"), wx.DefaultPosition, wx.Size( 130,-1 ), 0 )
		self.m_staticText41111.Wrap( -1 )
		self.m_staticText41111.SetToolTipString( _(u"millimeters") )

		lifting_height_sizer.Add( self.m_staticText41111, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.LEFT, 5 )

		self.m_staticText2111 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2111.Wrap( -1 )
		lifting_height_sizer.Add( self.m_staticText2111, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		self.lifting_height = wx.SpinCtrl( self, wx.ID_ANY, u"n/a", wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.lifting_height.SetToolTipString( _(u"millimeters") )

		lifting_height_sizer.Add( self.lifting_height, 1, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5 )


		settings_sizer_group2.Add( lifting_height_sizer, 0, wx.EXPAND, 5 )


		settings_sizer.Add( settings_sizer_group2, 1, wx.RIGHT|wx.LEFT, 5 )


		main_sizer.Add( settings_sizer, 1, wx.EXPAND, 5 )


		self.SetSizer( main_sizer )
		self.Layout()
		main_sizer.Fit( self )

		# Connect Events
		self.open_zip.Bind( wx.EVT_FILEPICKER_CHANGED, self.OnProjectChanged )
		self.open_folder.Bind( wx.EVT_DIRPICKER_CHANGED, self.OnProjectChanged )
		self.slice.Bind( wx.EVT_SCROLL, self.OnSliceSlide )
		self.exposure_time.Bind( wx.EVT_SPINCTRL, self.OnSettingsChange )
		self.exposure_time.Bind( wx.EVT_TEXT, self.OnSettingsChange )
		self.lifting_speed.Bind( wx.EVT_SPINCTRL, self.OnSettingsChange )
		self.lifting_speed.Bind( wx.EVT_TEXT, self.OnSettingsChange )
		self.lifting_height.Bind( wx.EVT_SPINCTRL, self.OnSettingsChange )
		self.lifting_height.Bind( wx.EVT_TEXT, self.OnSettingsChange )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnProjectChanged( self, event ):
		event.Skip()


	def OnSliceSlide( self, event ):
		event.Skip()

	def OnSettingsChange( self, event ):
		event.Skip()







###########################################################################
## Class SettingsPanel
###########################################################################

class SettingsPanel ( wx.Panel ):

	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )

		main_sizer = wx.BoxSizer( wx.VERTICAL )

		bSizer36 = wx.BoxSizer( wx.HORIZONTAL )

		self.main_label = wx.StaticText( self, wx.ID_ANY, _(u"Settings presets :"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.main_label.Wrap( -1 )
		self.main_label.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )

		bSizer36.Add( self.main_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		presetsChoices = []
		self.presets = wx.ComboBox( self, wx.ID_ANY, _(u"Defaults"), wx.DefaultPosition, wx.DefaultSize, presetsChoices, 0 )
		bSizer36.Add( self.presets, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.save = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"./assets/save.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.save.SetToolTipString( _(u"Save presets") )

		bSizer36.Add( self.save, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )

		self.delete = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"./assets/trash.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.delete.SetToolTipString( _(u"Delete presets") )

		bSizer36.Add( self.delete, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )


		main_sizer.Add( bSizer36, 0, wx.EXPAND, 5 )

		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText32 = wx.StaticText( self, wx.ID_ANY, _(u"Groupe 1 :"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText32.Wrap( -1 )
		bSizer28.Add( self.m_staticText32, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.layers_group_1_count = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.layers_group_1_count.SetToolTipString( _(u"Number of layers") )

		bSizer28.Add( self.layers_group_1_count, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText34 = wx.StaticText( self, wx.ID_ANY, _(u"Exposure time (ms) :"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText34.Wrap( -1 )
		self.m_staticText34.SetToolTipString( _(u"milliseconds") )

		bSizer28.Add( self.m_staticText34, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.layers_group_1_time = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 500, 500000, 0 )
		self.layers_group_1_time.Enable( False )
		self.layers_group_1_time.SetToolTipString( _(u"milliseconds") )

		bSizer28.Add( self.layers_group_1_time, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )


		main_sizer.Add( bSizer28, 0, wx.EXPAND, 5 )

		bSizer281 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText321 = wx.StaticText( self, wx.ID_ANY, _(u"Groupe 2 :"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText321.Wrap( -1 )
		bSizer281.Add( self.m_staticText321, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.layers_group_2_count = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.layers_group_2_count.Enable( False )
		self.layers_group_2_count.SetToolTipString( _(u"Number of layers") )

		bSizer281.Add( self.layers_group_2_count, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText341 = wx.StaticText( self, wx.ID_ANY, _(u"Exposure time (ms) :"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText341.Wrap( -1 )
		self.m_staticText341.SetToolTipString( _(u"milliseconds") )

		bSizer281.Add( self.m_staticText341, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.layers_group_2_time = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 500, 500000, 0 )
		self.layers_group_2_time.Enable( False )
		self.layers_group_2_time.SetToolTipString( _(u"milliseconds") )

		bSizer281.Add( self.layers_group_2_time, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )


		main_sizer.Add( bSizer281, 0, wx.EXPAND, 5 )

		bSizer282 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText322 = wx.StaticText( self, wx.ID_ANY, _(u"Groupe 3 :"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText322.Wrap( -1 )
		bSizer282.Add( self.m_staticText322, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.layers_group_3_count = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.layers_group_3_count.Enable( False )
		self.layers_group_3_count.SetToolTipString( _(u"Number of layers") )

		bSizer282.Add( self.layers_group_3_count, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText342 = wx.StaticText( self, wx.ID_ANY, _(u"Exposure time (ms) :"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText342.Wrap( -1 )
		self.m_staticText342.SetToolTipString( _(u"milliseconds") )

		bSizer282.Add( self.m_staticText342, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.layers_group_3_time = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 500, 500000, 0 )
		self.layers_group_3_time.Enable( False )
		self.layers_group_3_time.SetToolTipString( _(u"milliseconds") )

		bSizer282.Add( self.layers_group_3_time, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		main_sizer.Add( bSizer282, 0, wx.EXPAND, 5 )


		self.SetSizer( main_sizer )
		self.Layout()
		main_sizer.Fit( self )

		# Connect Events
		self.presets.Bind( wx.EVT_COMBOBOX, self.OnPresetsSelected )
		self.save.Bind( wx.EVT_BUTTON, self.OnSaveClick )
		self.delete.Bind( wx.EVT_BUTTON, self.OnDeleteClick )
		self.layers_group_1_count.Bind( wx.EVT_SPINCTRL, self.OnSettingsChange )
		self.layers_group_1_count.Bind( wx.EVT_TEXT, self.OnSettingsChange )
		self.layers_group_1_time.Bind( wx.EVT_SPINCTRL, self.OnSettingsChange )
		self.layers_group_1_time.Bind( wx.EVT_TEXT, self.OnSettingsChange )
		self.layers_group_2_count.Bind( wx.EVT_SPINCTRL, self.OnSettingsChange )
		self.layers_group_2_count.Bind( wx.EVT_TEXT, self.OnSettingsChange )
		self.layers_group_2_time.Bind( wx.EVT_SPINCTRL, self.OnSettingsChange )
		self.layers_group_2_time.Bind( wx.EVT_TEXT, self.OnSettingsChange )
		self.layers_group_3_count.Bind( wx.EVT_SPINCTRL, self.OnSettingsChange )
		self.layers_group_3_count.Bind( wx.EVT_TEXT, self.OnSettingsChange )
		self.layers_group_3_time.Bind( wx.EVT_SPINCTRL, self.OnSettingsChange )
		self.layers_group_3_time.Bind( wx.EVT_TEXT, self.OnSettingsChange )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnPresetsSelected( self, event ):
		event.Skip()

	def OnSaveClick( self, event ):
		event.Skip()

	def OnDeleteClick( self, event ):
		event.Skip()

	def OnSettingsChange( self, event ):
		event.Skip()













###########################################################################
## Class PrintPanel
###########################################################################

class PrintPanel ( wx.Panel ):

	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )

		main_sizer = wx.BoxSizer( wx.VERTICAL )

		buttons_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.start_stop = wx.Button( self, wx.ID_ANY, _(u"Start"), wx.DefaultPosition, wx.DefaultSize, 0 )
		buttons_sizer.Add( self.start_stop, 1, wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.pause_resume = wx.Button( self, wx.ID_ANY, _(u"Pause"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pause_resume.Enable( False )

		buttons_sizer.Add( self.pause_resume, 1, wx.ALL, 5 )


		main_sizer.Add( buttons_sizer, 0, wx.EXPAND, 5 )

		self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		main_sizer.Add( self.m_staticline5, 0, wx.EXPAND, 5 )

		timers_sizer = wx.BoxSizer( wx.HORIZONTAL )

		bSizer70 = wx.BoxSizer( wx.VERTICAL )

		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, _(u"Start time"), wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_staticText27.Wrap( -1 )
		bSizer20.Add( self.m_staticText27, 0, wx.TOP|wx.LEFT, 5 )

		self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )
		bSizer20.Add( self.m_staticText28, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.start_time = wx.StaticText( self, wx.ID_ANY, _(u"n/a"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.start_time.Wrap( -1 )
		bSizer20.Add( self.start_time, 1, wx.TOP|wx.RIGHT|wx.LEFT, 5 )


		bSizer70.Add( bSizer20, 0, wx.EXPAND|wx.BOTTOM, 5 )

		bSizer201 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText271 = wx.StaticText( self, wx.ID_ANY, _(u"End time"), wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_staticText271.Wrap( -1 )
		bSizer201.Add( self.m_staticText271, 0, wx.BOTTOM|wx.LEFT, 5 )

		self.m_staticText281 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText281.Wrap( -1 )
		bSizer201.Add( self.m_staticText281, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		self.end_time = wx.StaticText( self, wx.ID_ANY, _(u"n/a"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.end_time.Wrap( -1 )
		bSizer201.Add( self.end_time, 1, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		bSizer70.Add( bSizer201, 0, wx.EXPAND, 5 )


		timers_sizer.Add( bSizer70, 1, 0, 5 )

		self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		timers_sizer.Add( self.m_staticline4, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		bSizer71 = wx.BoxSizer( wx.VERTICAL )

		bSizer202 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText272 = wx.StaticText( self, wx.ID_ANY, _(u"Estimated time"), wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText272.Wrap( -1 )
		bSizer202.Add( self.m_staticText272, 0, wx.TOP|wx.LEFT, 5 )

		self.m_staticText282 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText282.Wrap( -1 )
		bSizer202.Add( self.m_staticText282, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.estimated_time = wx.StaticText( self, wx.ID_ANY, _(u"n/a"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.estimated_time.Wrap( -1 )
		bSizer202.Add( self.estimated_time, 1, wx.TOP|wx.RIGHT|wx.LEFT, 5 )


		bSizer71.Add( bSizer202, 0, wx.ALIGN_RIGHT|wx.EXPAND|wx.BOTTOM, 5 )

		bSizer2011 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2711 = wx.StaticText( self, wx.ID_ANY, _(u"Elapsed time"), wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText2711.Wrap( -1 )
		bSizer2011.Add( self.m_staticText2711, 0, wx.BOTTOM|wx.LEFT, 5 )

		self.m_staticText2811 = wx.StaticText( self, wx.ID_ANY, _(u":"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2811.Wrap( -1 )
		bSizer2011.Add( self.m_staticText2811, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		self.elapsed_time = wx.StaticText( self, wx.ID_ANY, _(u"n/a"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.elapsed_time.Wrap( -1 )
		bSizer2011.Add( self.elapsed_time, 1, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		bSizer71.Add( bSizer2011, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )


		timers_sizer.Add( bSizer71, 1, 0, 5 )


		main_sizer.Add( timers_sizer, 0, wx.EXPAND, 5 )


		self.SetSizer( main_sizer )
		self.Layout()
		main_sizer.Fit( self )

		# Connect Events
		self.start_stop.Bind( wx.EVT_BUTTON, self.OnStartStopClick )
		self.pause_resume.Bind( wx.EVT_BUTTON, self.OnPauseResumeClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnStartStopClick( self, event ):
		event.Skip()

	def OnPauseResumeClick( self, event ):
		event.Skip()
