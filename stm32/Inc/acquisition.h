#pragma once

#include "waveform.h"

void acquisition_init(void);
void acquire_phd(uint16_t v);
void acquire_period(void);

extern uint16_t mic_buff[WAVE_BUFF_LEN];
