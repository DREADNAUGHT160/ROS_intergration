#include "cy_pdl.h"
#include "cyhal.h"
#include "cybsp.h"
#include "cy_retarget_io.h"
#include <string.h>
#include <stdio.h>

char uart_buffer[64];
int uart_index = 0;

// Parsed command parts
char direction[16], steering[16];
int rpm = 0;
int recording = 0;

void blink_led() {
    cyhal_gpio_write(CYBSP_USER_LED, 0);  // LED ON
    cyhal_system_delay_ms(100);
    cyhal_gpio_write(CYBSP_USER_LED, 1);  // LED OFF
}

void process_command(const char* input) {
    if (sscanf(input, "%[^:]:%[^:]:%d:%d", direction, steering, &rpm, &recording) == 4) {
        blink_led();
        printf("ACK: %s %s %d Recording=%d\n", direction, steering, rpm, recording);
    } else {
        printf("ERROR: Invalid command\n");
    }
}

int main(void) {
    cy_rslt_t result;

    result = cybsp_init();
    if (result != CY_RSLT_SUCCESS) {
        CY_ASSERT(0);
    }

    __enable_irq();

    cy_retarget_io_init(CYBSP_DEBUG_UART_TX, CYBSP_DEBUG_UART_RX, 115200);
    printf("🟢 PSoC6 UART Receiver Ready\n");

    cyhal_gpio_init(CYBSP_USER_LED, CYHAL_GPIO_DIR_OUTPUT, CYHAL_GPIO_DRIVE_STRONG, 1);

    while (1) {
        if (cyhal_uart_readable(&cy_retarget_io_uart_obj)) {
            char c;
            cyhal_uart_getc(&cy_retarget_io_uart_obj, &c, 0);

            if (c == '\n' || c == '\r') {
                uart_buffer[uart_index] = '\0';
                if (uart_index > 0) {
                    process_command(uart_buffer);
                    uart_index = 0;
                }
            } else {
                if (uart_index < sizeof(uart_buffer) - 1) {
                    uart_buffer[uart_index++] = c;
                }
            }
        }
    }
}
