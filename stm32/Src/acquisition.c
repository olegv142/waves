#include "acquisition.h"

uint16_t mic_buff[WAVE_BUFF_LEN];
int16_t  mic_flt[WAVE_BUFF_LEN];
int32_t  mic_last;
int32_t  mic_sum;

uint16_t phd_last;
uint16_t phd_sum;
uint16_t phd_cnt;
uint16_t per_cnt;

void acquisition_init(void)
{
	int i;
	for (i = 0; i < WAVE_BUFF_LEN; ++i)
		mic_flt[i] = wave_buff[i] - WAVE_BASELINE;
}

void acquire_phd(uint16_t v)
{
	phd_last = v;
	phd_sum += v;
	++phd_cnt;
}

void acquire_period(void)
{
	int i;
	int32_t sum = 0;
	for (i = 0; i < WAVE_BUFF_LEN; ++i)
		sum += mic_flt[i] * mic_buff[i];
	mic_last = sum;
	mic_sum += sum;
	++per_cnt;
}
