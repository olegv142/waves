#pragma once

#include "stm32f4xx_hal.h"

#define assert assert_param
#define LED_ON  GPIO_PIN_RESET
#define LED_OFF GPIO_PIN_SET

extern ADC_HandleTypeDef hadc1;
extern ADC_HandleTypeDef hadc2;
extern DMA_HandleTypeDef hdma_adc1;

extern DAC_HandleTypeDef hdac;
extern DMA_HandleTypeDef hdma_dac1;

extern TIM_HandleTypeDef htim2;
extern TIM_HandleTypeDef htim3;

extern UART_HandleTypeDef huart1;
