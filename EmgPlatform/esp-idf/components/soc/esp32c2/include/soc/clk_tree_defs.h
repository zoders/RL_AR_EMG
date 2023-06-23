/*
 * SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#pragma once

#ifdef __cplusplus
extern "C" {
#endif

/**
 ************************ ESP32C2 Root Clock Source ***************************
 * 1) Internal 20MHz RC Oscillator: RC_FAST (usually referred as FOSC or CK8M/CLK8M in TRM and reg. description)
 *
 *    This RC oscillator generates a ~17.5MHz clock signal output as the RC_FAST_CLK.
 *    The ~17.5MHz signal output is also passed into a configurable divider, which by default divides the input clock
 *    frequency by 256, to generate a RC_FAST_D256_CLK (usually referred as 8md256 or simply d256 in reg. description).
 *
 *    The exact frequency of RC_FAST_CLK can be computed in runtime through calibration on the RC_FAST_D256_CLK.
 *
 * 2) External 40MHz Crystal Clock: XTAL
 *
 * 3) Internal 1500kHz RC Oscillator: RC_SLOW (usually referrred as RTC in TRM or reg. description)
 *
 *    This RC oscillator generates a ~150kHz clock signal output as the RC_SLOW_CLK. The exact frequency of this clock
 *    can be computed in runtime through calibration.
 *
 * 4) External Slow Clock (optional): XTAL32K
 *
 *    A clock signal generated by an external circuit can be connected to the 32K_XN pin to be the clock source for the
 *    RTC_SLOW_CLK. In such case, a 1nF capacitor should be placed between the 32K_XN pin and ground, so the 32K_XP pin
 *    cannot be used as a GPIO pin.
 *
 *    XTAL32K_CLK can also be calibrated to get its exact frequency.
 */

/* With the default value of CK8M_DFREQ = 100, RC_FAST clock frequency is 17.5 MHz +/- 7% */
#define SOC_CLK_RC_FAST_FREQ_APPROX         17500000
#define SOC_CLK_RC_SLOW_FREQ_APPROX         150000
#define SOC_CLK_RC_FAST_D256_FREQ_APPROX    (SOC_CLK_RC_FAST_FREQ_APPROX / 256)
#define SOC_CLK_XTAL32K_FREQ_APPROX         32768

/**
 * @brief Root clock
 * Naming convention: SOC_ROOT_CLK_{loc}_{type}_<attr>
 * {loc}: EXT, INT
 * {type}: XTAL, RC
 * <attr> - optional: <frequency>, FAST, SLOW
 */
typedef enum {
    SOC_ROOT_CLK_INT_RC_FAST,          /*!< Internal 8MHz RC oscillator */
    SOC_ROOT_CLK_INT_RC_SLOW,          /*!< Internal 150kHz RC oscillator */
    SOC_ROOT_CLK_EXT_XTAL,             /*!< External 40MHz crystal */
    SOC_ROOT_CLK_EXT_XTAL32K,          /*!< External ~32kHz clock signal */
} soc_root_clk_t;

/**
 * @brief CPU_CLK mux inputs, which are the supported clock sources for the CPU_CLK
 */
typedef enum {
    SOC_CPU_CLK_SRC_XTAL,              /*!< Select XTAL_CLK as CPU_CLK source */
    SOC_CPU_CLK_SRC_PLL,               /*!< Select PLL_CLK as CPU_CLK source (PLL_CLK is the output of 40MHz crystal oscillator frequency multiplier, 480MHz) */
    SOC_CPU_CLK_SRC_RC_FAST,           /*!< Select RC_FAST_CLK as CPU_CLK source */
} soc_cpu_clk_src_t;

/**
 * @brief RTC_SLOW_CLK mux inputs, which are the supported clock sources for the RTC_SLOW_CLK
 */
typedef enum {
    SOC_RTC_SLOW_CLK_SRC_RC_SLOW,      /*!< Select RC_SLOW_CLK as RTC_SLOW_CLK source */
    SOC_RTC_SLOW_CLK_SRC_XTAL32K,      /*!< Select XTAL32K_CLK as RTC_SLOW_CLK source */
    SOC_RTC_SLOW_CLK_SRC_RC_FAST_D256, /*!< Select RC_FAST_D256_CLK (referred as FOSC_DIV or 8m_d256/8md256 in TRM and reg. description) as RTC_SLOW_CLK source */
} soc_rtc_slow_clk_src_t;

/**
 * @brief RTC_FAST_CLK mux inputs, which are the supported clock sources for the RTC_FAST_CLK
 */
typedef enum {
    SOC_RTC_FAST_CLK_SRC_XTAL_D2,      /*!< Select XTAL_D2_CLK (may referred as XTAL_CLK_DIV_2) as RTC_FAST_CLK source */
    SOC_RTC_FAST_CLK_SRC_XTAL_DIV = SOC_RTC_FAST_CLK_SRC_XTAL_D2, /*!< Alias name for `SOC_RTC_FAST_CLK_SRC_XTAL_D2` */
    SOC_RTC_FAST_CLK_SRC_RC_FAST,      /*!< Select RC_FAST_CLK as RTC_FAST_CLK source */
} soc_rtc_fast_clk_src_t;

/**
 * @brief Supported clock sources for modules (CPU, peripherials, RTC, etc.)
 * Naming convention: SOC_MOD_CLK_{<upstream>clock_name}_<attr>
 * {<upstream>clock_name}: (BB)PLL etc.
 * <attr> - optional: FAST, SLOW, D<divider>, F<freq>
 * @note enum starts from 1, to save 0 for special purpose
 */
typedef enum {
    // For CPU domain
    SOC_MOD_CLK_CPU = 1,                       /*< CPU_CLK can be sourced from XTAL, PLL, or RC_FAST by configuring soc_cpu_clk_src_t */
    // For RTC domain
    SOC_MOD_CLK_RTC_FAST = 2,                  /*< RTC_FAST_CLK can be sourced from XTAL_D2 or RC_FAST by configuring soc_rtc_fast_clk_src_t */
    SOC_MOD_CLK_RTC_SLOW = 3,                  /*< RTC_SLOW_CLK can be sourced from RC_SLOW, XTAL32K, or RC_FAST_D256 by configuring soc_rtc_slow_clk_src_t */
    // For digital domain: peripherals, WIFI, BLE
    SOC_MOD_CLK_PLL_F40M = 4,                  /*< PLL_F40M_CLK is derived from PLL, and has a fixed frequency of 40MHz */
    SOC_MOD_CLK_PLL_F60M = 5,                  /*< PLL_F60M_CLK is derived from PLL, and has a fixed frequency of 60MHz */
    SOC_MOD_CLK_PLL_F80M = 6,                  /*< PLL_F80M_CLK is derived from PLL, and has a fixed frequency of 80MHz */
    SOC_MOD_CLK_XTAL32K = 7,                   /*< XTAL32K_CLK comes from the external 32kHz clock signal, passing a clock gating to the peripherals */
    SOC_MOD_CLK_RC_FAST = 8,                   /*< RC_FAST_CLK comes from the internal 20MHz rc oscillator, passing a clock gating to the peripherals */
    SOC_MOD_CLK_RC_FAST_D256 = 9,              /*< RC_FAST_D256_CLK comes from the internal 20MHz rc oscillator, divided by 256, and passing a clock gating to the peripherals */
    SOC_MOD_CLK_XTAL = 10,                     /*< XTAL_CLK comes from the external 40MHz crystal */
} soc_module_clk_t;


//////////////////////////////////////////////////GPTimer///////////////////////////////////////////////////////////////

/**
 * @brief Array initializer for all supported clock sources of GPTimer
 * The following code can be used to iterate all possible clocks:
 * @code{c}
 * soc_periph_gptimer_clk_src_t gptimer_clks[] = (soc_periph_gptimer_clk_src_t)SOC_GPTIMER_CLKS;
 * for (size_t i = 0; i< sizeof(gptimer_clks) / sizeof(gptimer_clks[0]); i++) {
 *     soc_periph_gptimer_clk_src_t clk = gptimer_clks[i];
 *     // Test GPTimer with the clock `clk`
 * }
 * @endcode
 */
#define SOC_GPTIMER_CLKS {SOC_MOD_CLK_PLL_F40M, SOC_MOD_CLK_XTAL}

/**
 * @brief Type of GPTimer clock source
 */
typedef enum {
    GPTIMER_CLK_SRC_PLL_F40M = SOC_MOD_CLK_PLL_F40M, /*!< Select PLL_F40M as the source clock */
    GPTIMER_CLK_SRC_XTAL = SOC_MOD_CLK_XTAL,         /*!< Select XTAL as the source clock */
    GPTIMER_CLK_SRC_DEFAULT = SOC_MOD_CLK_PLL_F40M,  /*!< Select PLL_F40M as the default choice */
} soc_periph_gptimer_clk_src_t;

/**
 * @brief Type of Timer Group clock source, reserved for the legacy timer group driver
 */
typedef enum {
    TIMER_SRC_CLK_PLL_F40M = SOC_MOD_CLK_PLL_F40M, /*!< Timer group clock source is PLL_F40M */
    TIMER_SRC_CLK_XTAL = SOC_MOD_CLK_XTAL,         /*!< Timer group clock source is XTAL */
    TIMER_SRC_CLK_DEFAULT = SOC_MOD_CLK_PLL_F40M,  /*!< Timer group clock source default choice is PLL_F40M */
} soc_periph_tg_clk_src_legacy_t;

//////////////////////////////////////////////////Temp Sensor///////////////////////////////////////////////////////////

/**
 * @brief Array initializer for all supported clock sources of Temperature Sensor
 */
#define SOC_TEMP_SENSOR_CLKS {SOC_MOD_CLK_XTAL, SOC_MOD_CLK_RC_FAST}

/**
 * @brief Type of Temp Sensor clock source
 */
typedef enum {
    TEMPERATURE_SENSOR_CLK_SRC_XTAL = SOC_MOD_CLK_XTAL,       /*!< Select XTAL as the source clock */
    TEMPERATURE_SENSOR_CLK_SRC_RC_FAST = SOC_MOD_CLK_RC_FAST, /*!< Select RC_FAST as the source clock */
    TEMPERATURE_SENSOR_CLK_SRC_DEFAULT = SOC_MOD_CLK_XTAL,    /*!< Select XTAL as the default choice */
} soc_periph_temperature_sensor_clk_src_t;

#ifdef __cplusplus
}
#endif
