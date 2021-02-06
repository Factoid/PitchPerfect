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
 * Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 */

#ifndef _GST_OPUSVIS_H_
#define _GST_OPUSVIS_H_

#include <gst/gst.h>
#include <opus.h>

G_BEGIN_DECLS

#define GST_TYPE_OPUSVIS   (gst_opusvis_get_type())
//#define GST_OPUSVIS(obj)   (G_TYPE_CHECK_INSTANCE_CAST((obj),GST_TYPE_OPUSVIS,GstOpusvis))
//#define GST_OPUSVIS_CLASS(klass)   (G_TYPE_CHECK_CLASS_CAST((klass),GST_TYPE_OPUSVIS,GstOpusvisClass))
//#define GST_IS_OPUSVIS(obj)   (G_TYPE_CHECK_INSTANCE_TYPE((obj),GST_TYPE_OPUSVIS))
//#define GST_IS_OPUSVIS_CLASS(obj)   (G_TYPE_CHECK_CLASS_TYPE((klass),GST_TYPE_OPUSVIS))

G_DECLARE_FINAL_TYPE( GstOpusvis, gst_opusvis, GST, OPUSVIS, GstElement );

//typedef struct _GstOpusvis GstOpusvis;
//typedef struct _GstOpusvisClass GstOpusvisClass;

struct _GstOpusvis
{
  GstElement element;
  GstPad *sinkpad, *srcpad;

  OpusDecoder* decoder;
};


G_END_DECLS

#endif
