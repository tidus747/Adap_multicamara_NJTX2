/*
 * imx219_tables.h - sensor mode tables for imx219 HDR sensor.
 *
 * Copyright (c) 2015-2016, NVIDIA CORPORATION, All Rights Reserved.
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms and conditions of the GNU General Public License,
 * version 2, as published by the Free Software Foundation.
 *
 * This program is distributed in the hope it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef IMX219_I2C_TABLES
#define IMX219_I2C_TABLES

#define IMX219_TABLE_WAIT_MS 0
#define IMX219_TABLE_END 1
#define IMX219_MAX_RETRIES 3
//#define IMX219_WAIT_MS 3
#define IMX219_WAIT_MS    10

static struct reg_8 imx219_start[] = {
  { 0x0100, 0x01 }, /* mode select streaming on */
  { IMX219_TABLE_END, 0x00 }
};

static struct reg_8 imx219_stop[] = {
  { 0x0100, 0x00 }, /* mode select streaming off */
  { IMX219_TABLE_END, 0x00 }
};

/* 0.912 GHz */
static struct reg_8 mode_1920x1080[] = {
  {IMX219_TABLE_WAIT_MS, 10},

  /* analogue gain setting */
  {0x0157, 0x00},
  /* 0x0158, 0x159 Digital gain */

  /* line length: 3448 */
  //{0x0162, 0x0D}, {0x0163, 0x78},
  /* line length: 3559 */
  {0x0162, 0x0D}, {0x0163, 0xE7},

  /* Frame Length: 1766 */
  //{0x0160, 0x06}, {0x0161, 0xE6},
  {0x0160, 0x0D}, {0x0161, 0x09},

  /* Coarse Time */
  {0x015A, 0x0D}, {0x015B, 0x05},


  /* Image Width: 2599 - 680 = 1920 - 1 */
  /* crop_rect.left: 680 Offset */
  {0x0164, 0x02}, {0x0165, 0xA8},
  //{0x0164, 0x02}, {0x0165, 0xAA},
  /* crop_rect.width - 1: 2599 */
  {0x0166, 0x0A}, {0x0167, 0x27},
  //{0x0166, 0x0A}, {0x0167, 0x29},


  /* Image Height: 1771 - 692 = 1080 - 1 */
  /* crop_rect.top: 692 */
  {0x0168, 0x02}, {0x0169, 0xB4},
  /* crop_rect.height - 1: 1771 */
  {0x016A, 0x06}, {0x016B, 0xEB},


  /* crop_rect.width: 1920 */
  {0x016C, 0x07}, {0x016D, 0x80},
  /* crop_rect.height: 1080 */
  {0x016E, 0x04}, {0x016F, 0x38},


  /* X odd increment: 1 */
  {0x0170, 0x01},

  /* Y odd increment: 1 */
  {0x0171, 0x01},

  /* Binning Mode Horizontal: 1 (no binning) */
  //{0x0174, 0x00},
  {0x0174, 0x00},

  /* Binning Mode Horizontal: 1 (no binning) */
  //{0x0175, 0x00},
  {0x0175, 0x00},

	{IMX219_TABLE_WAIT_MS, IMX219_WAIT_MS},
  {IMX219_TABLE_END, 0x00 }
};

static struct reg_8 mode_1280x720[] = {
  {IMX219_TABLE_WAIT_MS, 10},

  // analogue gain setting
  //{0x0157, 0xC7},
  {0x0157, 0x00},


  // Coarse Time
  //{0x015A, 0x04}, {0x015B, 0x22},
  //{0x015A, 0x0D}, {0x015B, 0x05},

  //{0x015A, 0x03}, {0x015B, 0x51},

  // 30 FPS
  // Frame Length: 853
  //{0x0160, 0x03}, {0x0161, 0x55},
  {0x0160, 0x02}, {0x0161, 0x8C},

  // Line Length: 3449
  {0x0162, 0x0D}, {0x0163, 0x78},

  // Image Width: 2279 - 360 = 1920 - 1 (1279)
  // crop_rect.left: 1000
  //{0x0164, 0x03}, {0x0165, 0xE8},


  // crop_rect.left: 360
  {0x0164, 0x01}, {0x0165, 0x68},

  // crop_rect.width: 2279
  {0x0166, 0x0B}, {0x0167, 0x67},

  // Image Height: 1591 - 872 = 720 - 1 (719)
  // crop_rect.top: 872
  //{0x0168, 0x03}, {0x0169, 0x68},
  {0x0168, 0x02}, {0x0169, 0x00},

  // crop_rect.height: 1591
  //{0x016A, 0x06}, {0x016B, 0x37},
  {0x016A, 0x07}, {0x016B, 0x9F},

  // image width = 1280
  {0x016C, 0x05}, {0x016D, 0x00},
  //{0x016C, 0x0D}, {0x016D, 0xD0},
  // image height = 720
  {0x016E, 0x02}, {0x016F, 0xD0},

  // X odd increment
  {0x0170, 0x01},

  // Y odd increment
  {0x0171, 0x01},

  // Binning Mode: X (1)
  //{0x0174, 0x00},
  {0x0174, 0x03},
  //{0x0174, 0x01},

  // Binning Mode: Y (1)
  //{0x0175, 0x00}
  {0x0175, 0x03},
  //{0x0175, 0x01}

	{IMX219_TABLE_WAIT_MS, IMX219_WAIT_MS},
  {IMX219_TABLE_END, 0x00 }
};

static struct reg_8 mode_640x480[] = {
  {IMX219_TABLE_WAIT_MS, 10},

  // analogue gain setting
  {0x0157, 0x00},

  // Frame Length: 569
  {0x0160, 0x01}, {0x0161, 0x89},
  //{0x0160, 0x02}, {0x0161, 0x39},

  //Coarse Time = 565
  //{0x015A, 0x02}, {0x015B, 0x35},


  // Line Length: 3559
  {0x0162, 0x0D}, {0x0163, 0xE8},
  // Line Length: 3448
  //{0x0162, 0x0D}, {0x0163, 0x78},


  // Window Width: 2279 - 1000 = 1280 - 1

  // crop_rect.left: 1000
  {0x0164, 0x03}, {0x0165, 0xE8},
  // crop_rect.width: 2279
  {0x0166, 0x08}, {0x0167, 0xE7},

  // Window Height: 1711 - 752 = 960 - 1 (2 X 480)

  // crop_rect.top: 752
  {0x0168, 0x02}, {0x0169, 0xF0},
  // crop_rect.height: 1711
  {0x016A, 0x06}, {0x016B, 0xAF},

  // image width = 640
  {0x016C, 0x02}, {0x016D, 0x80},
  // image height = 480
  {0x016E, 0x01}, {0x016F, 0xE0},


  /* X odd increment */
  //{0x0170, 0x03},
  {0x0170, 0x01},

  /* Y odd increment */
  //{0x0171, 0x03},
  {0x0171, 0x01},

  /* Binning Mode: X (2) */
  //{0x0174, 0x04},
  {0x0174, 0x03}, //2X Analog Binning
  //{0x0174, 0x00},

  /* Binning Mode: Y (2) */
  {0x0175, 0x03}, //2X Analog Binning
  //{0x0175, 0x00},
  //{0x0175, 0x02},

//  {0x0176, 0x01},
//  {0x0177, 0x01},

	{IMX219_TABLE_WAIT_MS, IMX219_WAIT_MS},
  {IMX219_TABLE_END, 0x00 }
};

static struct reg_8 mode_table_common[] = {
  /* software reset */
  {0x0103, 0x01},
  {0x0100, 0x00},

  //{0x6620, 0x01}, {0x6621, 0x01},
  //{0x6622, 0x01}, {0x6623, 0x01},

  /* Access Code to registers over 0x3000 */
  {0x30EB, 0x05},
  {0x30EB, 0x0C},
  {0x300A, 0xFF},
  {0x300B, 0xFF},
  {0x30EB, 0x05},
  {0x30EB, 0x09},

  /* number of csi lanes = 2 (1 + 1) */
  {0x0114, 0x01},

  /* dphy control: Auto */
  {0x0128, 0x00},

  /* external clock frequency = 24MHz */
  {0x012A, 0x18}, // 24 MHz
  {0x012B, 0x00}, // 000 KHz

  {IMX219_TABLE_END, 0x00 }
};

static struct reg_8 mode_table_clocks[] = {
  //Clock Settings

  /* CSI data format */
  {0x018C, 0x0A}, {0x018D, 0x0A},

  // PIXEL CLOCK USED TO DRIVE SENSOR)
  // VTPXCK_DIV: 4: 1/4, 5: 1/5, 8: 1/8, 10: 1/10
  {0x0301, 0x05},
  // VTSYS_DIV = 1: Divide by 1
  {0x0303, 0x01},

  // PREPLLCK_VT_DIV: 1: 1/1, 2: 1/2, 3: 1/3
  {0x0304, 0x03}, //MUST BE 3 FOR 24MHz

  // PREPLLCK_OP_DIV: 1: 1/1, 2: 1/2, 3: 1/3
  {0x0305, 0x03}, //MUST BE 3 FOR 24MHz

  // PLL_VT_MPY = 57 (Multiplier)
  {0x0306, 0x00}, {0x0307, 0x39},
  //{0x0306, 0x00}, {0x0307, 0x2E},
  //{0x0306, 0x00}, {0x0307, 0x57},

  // OPPXCK_DIV (pixel bit depth): 8:1/8 10:1/10
  {0x0309, 0x0A},
  // OPSYSCK_DIV (divide by two for double data rate): 1:1/2
  {0x030B, 0x01},

  // PLL_OP_MPY = 114 (Multiplier)
  {0x030C, 0x00}, {0x030D, 0x72},
  //{0x030C, 0x00}, {0x030D, 0x5C},
  //{0x030C, 0x00}, {0x030D, 0x5A},


  //Sensor Pixel Clock: EXCLK_FREQ / PREPLLLCK_VT_DIV * PLL_VT_MPY / VTPXCK_DIV: 24MHz / 3 * 57 / 5 = 91 MHz

  // CIS tunning
  {0x455E, 0x00},
  {0x471E, 0x4B},
  {0x4767, 0x0F},
  {0x4750, 0x14},
  {0x4540, 0x00},
  {0x47B4, 0x14},
  {0x4713, 0x30},
  {0x478B, 0x10},
  {0x478F, 0x10},
  {0x4793, 0x10},
  {0x4797, 0x0E},
  {0x479B, 0x0E},

  {IMX219_TABLE_END, 0x00 }
};

typedef struct {
  uint8_t gain;
  uint16_t coarse_time;
  uint16_t frame_length;
}imx219_mode_values_t;

static imx219_mode_values_t mode_1920x1080_values = {
  .gain = 0,
  .coarse_time = (1766 - 4),
  .frame_length=1766,
};

static imx219_mode_values_t mode_1280x720_values = {
  .gain = 0,
  .coarse_time = (851 - 4),
  .frame_length = 851,
};

static imx219_mode_values_t mode_640x480_values = {
  .gain = 0,
  .coarse_time = (569 - 4),
  .frame_length = 569,
};

enum {
  IMX219_MODE_1920X1080 = 0,
  IMX219_MODE_1280X720,
  IMX219_MODE_640X480,

  IMX219_MODE_COMMON,
  IMX219_MODE_CLOCK,
  IMX219_MODE_START_STREAM,
  IMX219_MODE_STOP_STREAM,
  IMX219_MODE_TEST_PATTERN,
};

imx219_mode_values_t *mode_values[] = {
  [IMX219_MODE_1920X1080]     = &mode_1920x1080_values,
  [IMX219_MODE_1280X720]      = &mode_1280x720_values,
  [IMX219_MODE_640X480]       = &mode_640x480_values,
};

static const struct reg_8 *mode_table[] = {
  [IMX219_MODE_1920X1080]     = mode_1920x1080,
  [IMX219_MODE_1280X720]      = mode_1280x720,
  [IMX219_MODE_640X480]       = mode_640x480,

  [IMX219_MODE_COMMON]        = mode_table_common,
  [IMX219_MODE_CLOCK]         = mode_table_clocks,
  [IMX219_MODE_START_STREAM]  = imx219_start,
  [IMX219_MODE_STOP_STREAM]   = imx219_stop,
};

static const int imx219_30fps[] = {
  30,
};

static const int imx219_60fps[] = {
  60,
};

static const int imx219_90fps[] = {
  90,
};

/*
camera_common_frmfmt: {struct v4l2_frmsize_discrete size}, {const int *framerates}, {num_framerates}, {hdr_en}, {int  mode}
*/

static const struct camera_common_frmfmt imx219_frmfmt[] = {
// Frame Size,    Framerates??,   Num Framerates, HDR Enable,  Mode
  {{1920,1080},   imx219_30fps,   1,              0,           IMX219_MODE_1920X1080     },
  {{1280,720},    imx219_60fps,   1,              0,           IMX219_MODE_1280X720      },
  {{640,480},     imx219_90fps,   1,              0,           IMX219_MODE_640X480       },
};

#endif  /* __IMX219_I2C_TABLES__ */
