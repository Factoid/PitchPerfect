/* GStreamer
 * Copyright (C) 2020 Adrian Cheater <adrian.cheater@gmail.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 51 Franklin Street, Suite 500,
 * Boston, MA 02110-1335, USA.
 */
/**
 * SECTION:element-gstopusvis
 *
 * The opusvis element provides visual information about the encoded stream before passing it on to a decoder
 *
 * <refsect2>
 * <title>Example launch line</title>
 * |[
 * gst-launch-1.0 -v autoaudiosrc ! opusenc ! opusvis ! opusdec ! autoaudiosink
 * ]|
 * This takes the audio source, encodes it in opus, allows the visualizer to graph the encoded LPC and *THING* data
 * before passing it on to the decoder so it can be played back on the audio sink
 * </refsect2>
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gst/gst.h>
#include "gstopusvis.h"
#include <opus.h>

GST_DEBUG_CATEGORY_STATIC (gst_opusvis_debug_category);
#define GST_CAT_DEFAULT gst_opusvis_debug_category

/* prototypes */


static void gst_opusvis_set_property (GObject * object,
    guint property_id, const GValue * value, GParamSpec * pspec);
static void gst_opusvis_get_property (GObject * object,
    guint property_id, GValue * value, GParamSpec * pspec);
//static void gst_opusvis_dispose (GObject * object);
//static void gst_opusvis_finalize (GObject * object);

//static gboolean gst_opusvis_setup (GstAudioFilter * filter,
//    const GstAudioInfo * info);
//static GstFlowReturn gst_opusvis_transform (GstBaseTransform * trans,
//    GstBuffer * inbuf, GstBuffer * outbuf);
//static GstFlowReturn gst_opusvis_transform_ip (GstBaseTransform * trans,
//    GstBuffer * buf);

enum
{
  PROP_0
};

/* pad templates */

/* TODO: Eventually this plugin should only read/write opus data */

static GstStaticPadTemplate gst_opusvis_src_template =
GST_STATIC_PAD_TEMPLATE ("src",
    GST_PAD_SRC,
    GST_PAD_ALWAYS,
    GST_STATIC_CAPS ("ANY")
    );

static GstStaticPadTemplate gst_opusvis_sink_template =
GST_STATIC_PAD_TEMPLATE ("sink",
    GST_PAD_SINK,
    GST_PAD_ALWAYS,
    GST_STATIC_CAPS("ANY")
    );


/* class initialization */

G_DEFINE_TYPE( GstOpusvis, gst_opusvis, GST_TYPE_ELEMENT);

static void gst_opusvis_class_init (GstOpusvisClass * klass)
{
  GObjectClass *gobject_class = G_OBJECT_CLASS (klass);
  /* Setting up pads and setting metadata should be moved to
     base_class_init if you intend to subclass this class. */
  gst_element_class_add_static_pad_template (GST_ELEMENT_CLASS(klass),
      &gst_opusvis_src_template);
  gst_element_class_add_static_pad_template (GST_ELEMENT_CLASS(klass),
      &gst_opusvis_sink_template);

  gst_element_class_set_static_metadata (GST_ELEMENT_CLASS(klass),
      "Opus Audio Visualizer", "Generic",
      "This plugin renders a visual display of opus frames on their way to the decoder",
      "<adrian.cheater@gmail.com>");

  gobject_class->set_property = gst_opusvis_set_property;
  gobject_class->get_property = gst_opusvis_get_property;
}

void gst_opusvis_set_property (GObject * object, guint property_id, const GValue * value, GParamSpec * pspec)
{
  GstOpusvis *opusvis = GST_OPUSVIS (object);

  GST_DEBUG_OBJECT (opusvis, "set_property");

  switch (property_id) {
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
      break;
  }
}

void gst_opusvis_get_property (GObject * object, guint property_id, GValue * value, GParamSpec * pspec)
{
  GstOpusvis *opusvis = GST_OPUSVIS (object);

  GST_DEBUG_OBJECT (opusvis, "get_property");

  switch (property_id) {
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
      break;
  }
}

static gboolean plugin_init (GstPlugin * plugin)
{

  /* FIXME Remember to set the rank if it's an element that is meant
     to be autoplugged by decodebin. */
  return gst_element_register (plugin, "opusvis", GST_RANK_NONE,
      GST_TYPE_OPUSVIS);
}

/**** INSTANCE CODE BEGINS *****/
static GstFlowReturn gst_opusvis_chain(GstPad *pad, GstObject* parent, GstBuffer *buf) {
  GstOpusvis* opusvis = GST_OPUSVIS(parent);
//  if( !gst_pad_set_caps(pad,caps) ) {
//    GST_ELEMENT_ERROR(opusvis, CORE, NEGOTIATION, (NULL), ("Couldn't set caps"));
//    return GST_FLOW_ERROR;
//  }

  GstMapInfo info;
  gst_buffer_map( buf, &info, GST_MAP_READ );

  switch( opus_packet_get_bandwidth(info.data) ) {
    case OPUS_BANDWIDTH_NARROWBAND:
      g_print( "Narrow band\n" );
      break;
    case OPUS_BANDWIDTH_MEDIUMBAND:
      g_print( "Medium band\n" );
      break;
    case OPUS_BANDWIDTH_WIDEBAND:
      g_print( "Wide band\n" );
      break;
    case OPUS_BANDWIDTH_SUPERWIDEBAND:
      g_print( "Super wide band\n" );
      break;
    case OPUS_BANDWIDTH_FULLBAND:
      g_print( "Full band\n" );
      break;
    case OPUS_INVALID_PACKET:
      g_print( "Invalid packer" );
      break;
   }

  g_print( "Number of frames %i\n", opus_packet_get_nb_frames(info.data, info.size) );

  gst_buffer_unmap(buf, &info);

  return gst_pad_push(opusvis->srcpad,buf);
}

static gboolean gst_opusvis_sink_event( GstPad *pad, GstObject* parent, GstEvent* event) {
//  GstOpusvis* opusvis = GST_OPUSVIS(parent);

  switch( GST_EVENT_TYPE(event) ) {
    default:
      return gst_pad_event_default( pad, parent, event );
  }
}

static gboolean gst_opusvis_src_query( GstPad* pad, GstObject *parent, GstQuery* query) {
  return gst_pad_query_default(pad,parent,query);
}

static void
gst_opusvis_init (GstOpusvis *opusvis)
{
  opusvis->sinkpad = gst_pad_new_from_static_template(&gst_opusvis_sink_template,"sink");
//  gst_pad_use_fixed_caps(opusvis->sinkpad);
  GST_PAD_SET_PROXY_CAPS(opusvis->sinkpad);

  gst_element_add_pad(GST_ELEMENT(opusvis), opusvis->sinkpad);

  opusvis->srcpad = gst_pad_new_from_static_template(&gst_opusvis_src_template,"src");
//  gst_pad_use_fixed_caps(opusvis->srcpad);
  GST_PAD_SET_PROXY_CAPS(opusvis->srcpad);

  gst_element_add_pad(GST_ELEMENT(opusvis), opusvis->srcpad);

  gst_pad_set_chain_function(opusvis->sinkpad,gst_opusvis_chain);
  gst_pad_set_event_function(opusvis->sinkpad,gst_opusvis_sink_event);
  gst_pad_set_query_function(opusvis->srcpad,gst_opusvis_src_query);
}
/**** INSTANCE CODE ENDS *****/


/* FIXME: these are normally defined by the GStreamer build system.
   If you are creating an element to be included in gst-plugins-*,
   remove these, as they're always defined.  Otherwise, edit as
   appropriate for your external plugin package. */
#ifndef VERSION
#define VERSION "0.0.1"
#endif
#ifndef PACKAGE
#define PACKAGE "opusvis"
#endif
#ifndef PACKAGE_NAME
#define PACKAGE_NAME "Opus Visualizer"
#endif
#ifndef GST_PACKAGE_ORIGIN
#define GST_PACKAGE_ORIGIN "http://FIXME.org/"
#endif

GST_PLUGIN_DEFINE (GST_VERSION_MAJOR,
    GST_VERSION_MINOR,
    opusvis,
    "Opus Audio Visualizer",
    plugin_init, VERSION, "LGPL", PACKAGE_NAME, GST_PACKAGE_ORIGIN)

