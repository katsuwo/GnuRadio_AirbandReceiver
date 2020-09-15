#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: air band receiver
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class AM_Receiver(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="air band receiver")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 1
        self.sql = sql = 0
        self.samp_rate = samp_rate = 2.4e6
        self.rfgain = rfgain = 50
        self.frq_corr = frq_corr = 30
        self.base_freq = base_freq = 120.5e6

        ##################################################
        # Blocks
        ##################################################
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label='Volume',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=0,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_volume_sizer)
        _sql_sizer = wx.BoxSizer(wx.VERTICAL)
        self._sql_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_sql_sizer,
        	value=self.sql,
        	callback=self.set_sql,
        	label='Squelch',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._sql_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_sql_sizer,
        	value=self.sql,
        	callback=self.set_sql,
        	minimum=-100,
        	maximum=100,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_sql_sizer)
        _rfgain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rfgain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rfgain_sizer,
        	value=self.rfgain,
        	callback=self.set_rfgain,
        	label='RF_Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rfgain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rfgain_sizer,
        	value=self.rfgain,
        	callback=self.set_rfgain,
        	minimum=0,
        	maximum=50,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_rfgain_sizer)
        _frq_corr_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frq_corr_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_frq_corr_sizer,
        	value=self.frq_corr,
        	callback=self.set_frq_corr,
        	label='freq_correction(ppm)',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._frq_corr_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_frq_corr_sizer,
        	value=self.frq_corr,
        	callback=self.set_frq_corr,
        	minimum=-127,
        	maximum=127,
        	num_steps=254,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_frq_corr_sizer)
        self.wxgui_fftsink2_0_0_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate /50,
        	fft_size=512,
        	fft_rate=5,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0_0_0.win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'rtl_tcp=192.168.10.109:1235' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(base_freq, 0)
        self.osmosdr_source_0.set_freq_corr(frq_corr, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(rfgain, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna('RX', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(50, (firdes.low_pass_2(1,samp_rate,25e3,10e3,40)), 0, samp_rate)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, '192.168.10.30', 8082, 1472, True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(sql, 1e-4, 0, False)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=48e3,
        	audio_decim=1,
        	audio_pass=5000,
        	audio_stop=5500,
        )
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-3, 1e-5, 1.0, 0)
        self.analog_agc2_xx_0.set_max_gain(5)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.wxgui_fftsink2_0_0_0, 0))
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)
        self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

    def get_sql(self):
        return self.sql

    def set_sql(self, sql):
        self.sql = sql
        self._sql_slider.set_value(self.sql)
        self._sql_text_box.set_value(self.sql)
        self.analog_pwr_squelch_xx_0.set_threshold(self.sql)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0_0_0.set_sample_rate(self.samp_rate /50)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass_2(1,self.samp_rate,25e3,10e3,40)))

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self._rfgain_slider.set_value(self.rfgain)
        self._rfgain_text_box.set_value(self.rfgain)
        self.osmosdr_source_0.set_gain(self.rfgain, 0)

    def get_frq_corr(self):
        return self.frq_corr

    def set_frq_corr(self, frq_corr):
        self.frq_corr = frq_corr
        self._frq_corr_slider.set_value(self.frq_corr)
        self._frq_corr_text_box.set_value(self.frq_corr)
        self.osmosdr_source_0.set_freq_corr(self.frq_corr, 0)

    def get_base_freq(self):
        return self.base_freq

    def set_base_freq(self, base_freq):
        self.base_freq = base_freq
        self.osmosdr_source_0.set_center_freq(self.base_freq, 0)


def main(top_block_cls=AM_Receiver, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
