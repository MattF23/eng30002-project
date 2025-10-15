from time import sleep
import smbus

REG_INTR_STATUS_1 = 0x00
REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03
REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08
REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C
REG_LED2_PA = 0x0D

class MAX30102:
    def __init__(self, channel=1, address=0x57):
        self.bus = smbus.SMBus(channel)
        self.address = address
        self.reset()
        sleep(1)
        self.setup()

    def reset(self):
        self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [0x40])

    def shutdown(self):
        self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [0x80])

    def setup(self):
        self.bus.write_i2c_block_data(self.address, REG_INTR_ENABLE_1, [0xC0])
        self.bus.write_i2c_block_data(self.address, REG_INTR_ENABLE_2, [0x00])
        self.bus.write_i2c_block_data(self.address, REG_FIFO_WR_PTR, [0x00])
        self.bus.write_i2c_block_data(self.address, REG_OVF_COUNTER, [0x00])
        self.bus.write_i2c_block_data(self.address, REG_FIFO_RD_PTR, [0x00])
        self.bus.write_i2c_block_data(self.address, REG_FIFO_CONFIG, [0x4F])
        self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [0x03])
        self.bus.write_i2c_block_data(self.address, REG_SPO2_CONFIG, [0x27])
        self.bus.write_i2c_block_data(self.address, REG_LED1_PA, [0x24])
        self.bus.write_i2c_block_data(self.address, REG_LED2_PA, [0x24])

    def get_data_present(self):
        rd_ptr = self.bus.read_byte_data(self.address, REG_FIFO_RD_PTR)
        wr_ptr = self.bus.read_byte_data(self.address, REG_FIFO_WR_PTR)
        samples = wr_ptr - rd_ptr
        if samples < 0:
            samples += 32
        return samples

    def read_fifo(self):
        data = self.bus.read_i2c_block_data(self.address, REG_FIFO_DATA, 6)
        red = (data[0] << 16 | data[1] << 8 | data[2]) & 0x03FFFF
        ir = (data[3] << 16 | data[4] << 8 | data[5]) & 0x03FFFF
        return red, ir
