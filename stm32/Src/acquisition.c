#include "acquisition.h"
#include "main.h"

uint16_t mic_buff[WAVE_BUFF_LEN];
int16_t  mic_flt[WAVE_BUFF_LEN];
int32_t  mic_last;
int32_t  mic_sum;

uint16_t phd_last;
uint16_t phd_sum;
uint16_t phd_cnt;
uint16_t per_cnt;

uint8_t msg[8];

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

void prepare_msg(void)
{
	msg[0] += 1;
	msg[0] |= 128;
	msg[1] = (mic_sum >>  0) & 127;
	msg[2] = (mic_sum >>  7) & 127;
	msg[3] = (mic_sum >> 14) & 127;
	msg[4] = (mic_sum >> 21) & 127;
	msg[5] = (mic_sum >> 28) & 127;
	msg[6] = (phd_sum >>  0) & 127;
	msg[7] = (phd_sum >>  7) & 127;
}

void send_msg(void)
{
	HAL_StatusTypeDef res = HAL_UART_Transmit_IT(&huart1, msg, sizeof(msg));
	assert(res != HAL_OK);
}

void reset_data(void)
{
	per_cnt = phd_cnt = 0;
	mic_sum = 0;
	phd_sum = 0;
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
	if (per_cnt >= 4) {
		prepare_msg();
		send_msg();
		reset_data();
	}
}
