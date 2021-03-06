#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: air band receiver
# Generated: Tue Sep 15 20:46:39 2020
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class AM_Receiver_NOGUI(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="air band receiver")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.udp_dest_port = udp_dest_port = 8082
        self.udp_dest_host = udp_dest_host = "192.168.10.30"
        self.sql = sql = -10.0
        self.samp_rate = samp_rate = 2.4e6
        self.rfgain = rfgain = 49.5
        self.frq_corr = frq_corr = 30.0
        self.device_arg = device_arg = "rtl_tcp=192.168.10.109:1235"
        self.base_freq = base_freq = 120.5e6

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + device_arg )
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
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, udp_dest_host, udp_dest_port, 1472, True)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)
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
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def get_udp_dest_port(self):
        return self.udp_dest_port

    def set_udp_dest_port(self, udp_dest_port):
        self.udp_dest_port = udp_dest_port

    def get_udp_dest_host(self):
        return self.udp_dest_host

    def set_udp_dest_host(self, udp_dest_host):
        self.udp_dest_host = udp_dest_host

    def get_sql(self):
        return self.sql

    def set_sql(self, sql):
        self.sql = sql
        self.analog_pwr_squelch_xx_0.set_threshold(self.sql)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass_2(1,self.samp_rate,25e3,10e3,40)))

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.osmosdr_source_0.set_gain(self.rfgain, 0)

    def get_frq_corr(self):
        return self.frq_corr

    def set_frq_corr(self, frq_corr):
        self.frq_corr = frq_corr
        self.osmosdr_source_0.set_freq_corr(self.frq_corr, 0)

    def get_device_arg(self):
        return self.device_arg

    def set_device_arg(self, device_arg):
        self.device_arg = device_arg

    def get_base_freq(self):
        return self.base_freq

    def set_base_freq(self, base_freq):
        self.base_freq = base_freq
        self.osmosdr_source_0.set_center_freq(self.base_freq, 0)


def main(top_block_cls=AM_Receiver_NOGUI, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
